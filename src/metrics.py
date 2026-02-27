import numpy as np
import pandas as pd
from scipy.stats import ttest_1samp


def compute_cumulative_abnormal_returns(event_df):
    # Calculate CAR for each event
    event_df["car"] = event_df.groupby("event_date")["abnormal_return"].cumsum()

    # Baseline to Day -1 (Make Day -1 exactly 0)
    # Vectorized approach avoids Pandas groupby.apply() dropping the event_date column
    baselines = event_df[event_df["relative_day"] == -1].set_index("event_date")["car"]
    event_df["car"] = event_df["car"] - event_df["event_date"].map(baselines).fillna(0)

    return event_df


def compute_average_path(event_df):
    # Mean Cumulative Abnormal Return (MCAR) across all events
    avg_path = event_df.groupby("relative_day")["car"].mean()

    # Calculate Cross-Sectional Standard Error for confidence bands
    std_error = event_df.groupby("relative_day")["car"].std() / np.sqrt(event_df["event_date"].nunique())

    return pd.DataFrame({"mcar": avg_path, "std_error": std_error})


def test_event_day_significance(event_df):
    # Test if Abnormal Return on Day 0 is significantly different from 0
    event_returns = event_df[event_df["relative_day"] == 0]["abnormal_return"]
    t_stat, p_value = ttest_1samp(event_returns, 0)
    return t_stat, p_value