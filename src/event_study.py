import pandas as pd
import numpy as np
from scipy.stats import linregress


def extract_abnormal_returns(returns_df, event_dates, target_ticker, benchmark_ticker="SPY", event_window=5,
                             est_window=120):
    all_events = []

    for event in event_dates:
        if event not in returns_df.index:
            continue

        loc = returns_df.index.get_loc(event)

        # Ensure we have enough historical data for the estimation window and event window
        if loc - est_window - event_window < 0 or loc + event_window >= len(returns_df):
            continue

        # 1. Estimation Window (to calculate Alpha and Beta)
        est_start = loc - event_window - est_window
        est_end = loc - event_window - 1

        y_est = returns_df.iloc[est_start:est_end + 1][target_ticker].values
        x_est = returns_df.iloc[est_start:est_end + 1][benchmark_ticker].values

        slope, intercept, r_value, p_value, std_err = linregress(x_est, y_est)

        # 2. Event Window (to calculate Abnormal Returns)
        evt_start = loc - event_window
        evt_end = loc + event_window

        actual_returns = returns_df.iloc[evt_start:evt_end + 1][target_ticker].values
        market_returns = returns_df.iloc[evt_start:evt_end + 1][benchmark_ticker].values

        # Expected return based on Market Model
        expected_returns = intercept + (slope * market_returns)

        # Abnormal Return (AR) = Actual - Expected
        abnormal_returns = actual_returns - expected_returns

        # Standard Error of the estimation window regression (used for confidence intervals later)
        regression_residuals = y_est - (intercept + slope * x_est)
        rmse = np.std(regression_residuals, ddof=2)

        df = pd.DataFrame({
            "relative_day": range(-event_window, event_window + 1),
            "actual_return": actual_returns,
            "abnormal_return": abnormal_returns,
            "event_date": event,
            "rmse": rmse
        })

        all_events.append(df)

    if not all_events:
        return pd.DataFrame()

    return pd.concat(all_events, ignore_index=True)