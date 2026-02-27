import pandas as pd
from src.data_loader import fetch_price_data, compute_log_returns
from src.event_study import extract_abnormal_returns
from src.metrics import (
    compute_cumulative_abnormal_returns,
    compute_average_path,
    test_event_day_significance
)
from src.visualization import plot_average_path
import os

OUTPUT_DIR = "analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)
import matplotlib.pyplot as plt

# CONFIGURATION
BENCHMARK = "SPY"
TARGET_TICKERS = ["GLD", "TLT"]  # Removed SPY from targets since it's the benchmark
ALL_TICKERS = [BENCHMARK] + TARGET_TICKERS

START_DATE = "2020-01-01"  # Pulled back to allow for estimation windows in early 2022
END_DATE = "2024-12-31"
EVENT_WINDOW = 5
ESTIMATION_WINDOW = 120

cpi_dates = pd.to_datetime([
    "2022-01-12", "2022-02-10", "2022-03-10",
    "2022-04-12", "2022-05-11", "2022-06-10",
    "2022-07-13", "2022-08-10", "2022-09-13",
    "2022-10-13", "2022-11-10", "2022-12-13"
])

# 1. Load Data
print("Fetching data...")
prices = fetch_price_data(ALL_TICKERS, START_DATE, END_DATE)
returns = compute_log_returns(prices)

# 2. Process Each Target Asset
for ticker in TARGET_TICKERS:
    # Calculate Abnormal Returns using Market Model
    event_df = extract_abnormal_returns(
        returns,
        cpi_dates,
        target_ticker=ticker,
        benchmark_ticker=BENCHMARK,
        event_window=EVENT_WINDOW,
        est_window=ESTIMATION_WINDOW
    )

    if event_df.empty:
        print(f"Not enough data to process {ticker}. Skipping.")
        continue

    # Calculate Metrics
    event_df = compute_cumulative_abnormal_returns(event_df)
    avg_df = compute_average_path(event_df)
    avg_df.to_csv(f"analysis/{ticker}_average_path.csv")
    t_stat, p_value = test_event_day_significance(event_df)
    # Save statistical summary
    summary_df = pd.DataFrame({
        "Ticker": [ticker],
        "Event_Day_t_stat": [t_stat],
        "Event_Day_p_value": [p_value]
    })

    summary_path = os.path.join(OUTPUT_DIR, "event_summary.csv")

    if not os.path.exists(summary_path):
        summary_df.to_csv(summary_path, index=False)
    else:
        summary_df.to_csv(summary_path, mode="a", header=False, index=False)
    # Output Results
    print(f"\n===== {ticker} Impact Analysis =====")
    print(f"Event Day (Day 0) Abnormal Return t-stat: {t_stat:.4f}")
    print(f"Event Day (Day 0) p-value: {p_value:.4f}")
    if p_value < 0.05:
        print("Result: STATISTICALLY SIGNIFICANT impact on Day 0.")
    else:
        print("Result: No statistically significant impact on Day 0.")

    # Visualize
    plot_average_path(avg_df, ticker, event_name="CPI Releases")