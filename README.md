# Difference-in-Differences Analysis of Central European Bond Yields

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This project implements a difference-in-differences econometric analysis to examine the causal effect of policy changes on government bond yields in Central Europe, focusing on Hungary as the treatment group and Czech Republic and Poland as control countries.

## Research Question & Hypothesis

**Research Question**: What was the causal impact of Hungary's policy change (effective January 1, 2023) on long-term government bond yields relative to comparable Central European countries?

**Hypothesis**: We hypothesize that the policy change led to increased sovereign risk perception, resulting in higher borrowing costs for the Hungarian government. Specifically, we expect to observe an increase of approximately 1.3 percentage points in Hungarian 10-year government bond yields relative to the counterfactual scenario.

**Empirical Strategy**: We employ a two-way fixed effects difference-in-differences design, comparing Hungary (treatment) to Czech Republic and Poland (controls) before and after January 1, 2023. The model controls for country-specific time-invariant factors and common time trends through fixed effects.

## Data Source

The analysis uses **OECD long-term government bond yield data** (10-year benchmark yields) for three Central European countries:

- **Hungary** (HU): `IRLTLT01HUM156N.csv`
- **Czech Republic** (CZ): `IRLTLT01CZM156N.csv`  
- **Poland** (PL): `IRLTLT01PLM156N.csv`

The data covers the period from 2022-01-01 onwards, with the treatment period beginning on 2023-01-01. The treatment date is marked as December 22, 2022, representing the policy announcement date.

**Data Preprocessing**: 
- Date parsing and yield variable standardization
- Country identifier creation and panel data stacking
- Treatment and post-treatment indicator construction
- Monthly time period aggregation for fixed effects

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Analysis**:
   ```bash
   cd notebooks/
   jupyter notebook analysis.ipynb
   ```

3. **Key Outputs**:
   - Regression results with difference-in-differences coefficient
   - Time series visualization of bond yields
   - Cleaned panel dataset saved to `data/processed/panel.csv`

## Methodology

The analysis employs a **two-way fixed effects difference-in-differences model**:

```
yield_it = α + β₁(treat_i × post_t) + γ_i + δ_t + ε_it
```

Where:
- `yield_it` = 10-year government bond yield for country i at time t
- `treat_i` = 1 if Hungary, 0 if Czech Republic or Poland
- `post_t` = 1 if date ≥ 2023-01-01, 0 otherwise
- `γ_i` = Country fixed effects
- `δ_t` = Monthly time fixed effects
- `β₁` = Difference-in-differences coefficient (parameter of interest)

**Standard Errors**: HC1 heteroskedasticity-robust standard errors are used to account for potential heteroskedasticity in the error terms.

## Limitations & Future Extensions

This analysis is preliminary. It uses monthly benchmark yields which smooth over short-term market dynamics. Daily or intraday data would allow for sharper inference around the announcement window. The control group is limited to Czechia and Poland; a broader synthetic control with weighted donors may produce a more credible counterfactual. We also abstract from other measures of sovereign risk. Incorporating credit default swap (CDS) spreads would provide a purer gauge of market perceptions and could be used in a panel with more granular frequency. Finally, we ignore potential spillover effects across countries and assume parallel trends. Further work should test the robustness of these assumptions and explore alternative specifications such as local projections or dynamic DiD models. Additional predictors like inflation or exchange rates might help account for macroeconomic shocks that differentially affect yields. Overall, this notebook offers a minimal working example to estimate the average treatment effect, serving as a foundation for richer empirical analyses.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         did_finance_eu and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── did_finance_eu   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes did_finance_eu a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

