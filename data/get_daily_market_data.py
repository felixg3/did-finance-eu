import io
import json
import re
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from did_finance_eu.config import PROCESSED_DATA_DIR

# ISO code -> slug mapping for EU-27 countries and the United Kingdom
COUNTRIES = {
    "AT": "austria",
    "BE": "belgium",
    "BG": "bulgaria",
    "HR": "croatia",
    "CY": "cyprus",
    "CZ": "czech-republic",
    "DK": "denmark",
    "EE": "estonia",
    "FI": "finland",
    "FR": "france",
    "DE": "germany",
    "GR": "greece",
    "HU": "hungary",
    "IE": "ireland",
    "IT": "italy",
    "LV": "latvia",
    "LT": "lithuania",
    "LU": "luxembourg",
    "MT": "malta",
    "NL": "netherlands",
    "PL": "poland",
    "PT": "portugal",
    "RO": "romania",
    "SK": "slovakia",
    "SI": "slovenia",
    "ES": "spain",
    "SE": "sweden",
    "UK": "united-kingdom",
}

START = "2021-01-01"
END = "2025-05-31"

ECB_URL = (
    "https://sdw.ecb.europa.eu/service/data/"
    "FM/D.{iso}.EUR.4F.BB.{iso}_10Y.YLD"
    "?startPeriod="
    + START
    + "&endPeriod="
    + END
    + "&format=csvdata"
)

CDS_PAGE = "https://www.worldgovernmentbonds.com/cds-historical-data/{slug}/5-years/"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "origin": "https://www.worldgovernmentbonds.com",
    "referer": "https://www.worldgovernmentbonds.com",
}


def fetch_bond_series(iso: str) -> pd.DataFrame:
    url = ECB_URL.format(iso=iso)
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text))
        df = df[["TIME_PERIOD", "OBS_VALUE"]]
        df.columns = ["date", "bond_yield"]
        df["date"] = pd.to_datetime(df["date"])
        df["bond_yield"] = pd.to_numeric(df["bond_yield"], errors="coerce")
    except Exception as exc:  # pragma: no cover - network issues
        dates = pd.date_range(START, END, freq="B")
        df = pd.DataFrame({"date": dates, "bond_yield": np.nan})
    df["country"] = iso
    return df


def fetch_cds_series(iso: str, slug: str) -> pd.DataFrame:
    url = CDS_PAGE.format(slug=slug)
    try:
        html = requests.get(url, timeout=30).text
        match = re.search(r"var jsGlobalVars = (\{.*?\})", html)
        if not match:
            raise ValueError("jsGlobalVars not found")
        js_vars = json.loads(match.group(1))
        endpoint = js_vars["ENDPOINT"]
        payload = {"GLOBALVAR": js_vars}
        resp = requests.post(endpoint, json=payload, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()["result"]["quote"]
        df = pd.DataFrame(data).T[["DATA_VAL", "CLOSE_VAL"]]
        df.columns = ["date", "cds_spread"]
        df["date"] = pd.to_datetime(df["date"])
        df["cds_spread"] = pd.to_numeric(df["cds_spread"], errors="coerce")
    except Exception as exc:  # pragma: no cover - network issues
        dates = pd.date_range(START, END, freq="B")
        df = pd.DataFrame({"date": dates, "cds_spread": np.nan})
    df["country"] = iso
    return df


def main() -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    bonds = []
    cds = []
    for iso, slug in tqdm(COUNTRIES.items()):
        bonds.append(fetch_bond_series(iso))
        cds.append(fetch_cds_series(iso, slug))
    bond_df = pd.concat(bonds).sort_values(["country", "date"])
    cds_df = pd.concat(cds).sort_values(["country", "date"])
    bond_df.to_parquet(PROCESSED_DATA_DIR / "bonds.parq")
    cds_df.to_parquet(PROCESSED_DATA_DIR / "cds.parq")


if __name__ == "__main__":
    main()
