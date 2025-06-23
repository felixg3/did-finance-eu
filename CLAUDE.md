# Project Memory

## Project Components
- **analysis.ipynb** – a Jupyter notebook that
  • imports pandas, statsmodels, matplotlib  
  • reads the three local CSV files  
    ```
    IRLTLT01HUM156N.csv   # Hungary
    IRLTLT01CZM156N.csv   # Czechia
    IRLTLT01PLM156N.csv   # Poland
    ```  
    (use `parse_dates=["DATE"]`, rename the value column to `"yield"`, and add a `"country"` label)  
  • concatenates them, filters `DATE >= "2022-01-01"`, and creates  
    `treat = (country == "HU")` and `post = (DATE >= "2023-01-01")`  
  • estimates the two-way FE difference-in-differences model  
    ```python
    yield ~ treat*post + C(country) + C(DATE.dt.to_period('M'))
    ```  
    via `statsmodels` with HC1 robust errors  
  • prints the regression table, bold-highlights the `treat:post` coefficient and interprets it in a markdown cell (expect ≈ +1.3 pp).  
  • plots the three yield series on one chart with a dashed vertical line at 2022-12-22.  
  • saves the cleaned stacked dataframe to *data/panel.csv*.

- **requirements.txt** with:  
  `pandas\nstatsmodels\nmatplotlib\nnotebook`

- **README.md** (~400 words) covering  
  • research question & hypothesis  
  • data source (OECD long-term benchmark yields, already provided as CSV)  
  • quick-start (`pip install -r requirements.txt`, open notebook)  
  • two paragraphs on limitations / future extensions (daily data, CDS spreads, synthetic control).

## Project Development Notes
- Using cookie cutter data science (CCDS) template. Follow the structure. The goal has to be a GitHub publishable econometrics paper.