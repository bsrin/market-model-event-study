# Event-Driven Market Impact Analysis (Market Model Event Study)

## Overview

This project implements a full Market Model event study framework to analyze how financial assets react to scheduled macroeconomic announcements.

Specifically, the framework evaluates the impact of US CPI releases on asset returns using abnormal return modeling, cumulative abnormal return aggregation, and statistical inference.

The project is fully modular, reproducible, and structured for research-grade analysis.

---

## Methodology

### 1. Data

- Assets:
  - SPY (Benchmark – Market Proxy)
  - GLD (Gold ETF)
  - TLT (Long-Term Treasury ETF)

- Data Source: Yahoo Finance
- Frequency: Daily Adjusted Prices
- Sample Period: 2020–2024
- Events: US CPI release dates (2022 sample)

---

### 2. Event Study Framework

The project uses the **Market Model** to estimate expected returns.

For each asset:

1. **Estimation Window (120 days prior to event window)**
   - Linear regression:
     
     Rᵢ = α + βRₘ + ε

2. **Event Window (−5 to +5 trading days)**

3. **Abnormal Return (AR)**

   ARₜ = Actual Return − Expected Return

4. **Cumulative Abnormal Return (CAR)**

   CARₜ = Σ AR

5. **Mean Cumulative Abnormal Return (MCAR)**

   Average CAR across all events.

6. **Statistical Testing**
   - One-sample t-test on Day 0 abnormal returns.
   - 95% confidence bands around MCAR.

---

## Outputs

The `analysis/` folder contains:

- Event summary statistics (CSV)
- Average path data (CSV)
- Visualization outputs (if enabled)

Console output includes:

- Event-day t-statistic
- Event-day p-value
- Statistical significance interpretation

---

## Project Structure

market-model-event-study/
│
├── src/
│   ├── data_loader.py        # Data retrieval & return computation
│   ├── event_study.py        # Market Model regression & abnormal returns
│   ├── metrics.py            # CAR, MCAR, statistical testing
│   └── visualization.py      # Plotting & confidence bands
│
├── analysis/                 # Generated research outputs
│   ├── event_summary.csv
│   ├── GLD_average_path.csv
│   ├── TLT_average_path.csv
│   ├── GLD_car_plot.png
│   └── TLT_car_plot.png
│
├── main.py                   # Orchestrates full event study pipeline
├── requirements.txt          # Project dependencies
├── .gitignore
└── README.md


---

## Key Findings (Sample)

- No statistically significant abnormal return detected on CPI release days at the 5% significance level.
- Confidence intervals indicate dispersion in event reactions across different releases.
- Results suggest limited systematic CPI-driven abnormal pricing during the sample window.

---

## Technologies Used

- Python
- pandas
- numpy
- scipy
- matplotlib
- yfinance

---

## Future Extensions

- Multi-factor models (Fama-French)
- Intraday event analysis
- Surprise magnitude classification
- Cross-asset spillover modeling
- Regime-based event clustering

---

## Author Note


This project was built to demonstrate applied quantitative finance methodology, financial econometrics implementation, and structured research analysis in Python.
