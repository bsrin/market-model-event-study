import yfinance as yf
import pandas as pd
import numpy as np


def fetch_price_data(tickers, start_date, end_date):
    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        progress=False,
        threads=True,
        auto_adjust=True
    )

    if isinstance(data.columns, pd.MultiIndex):
        price_data = data["Close"]
    else:
        price_data = data["Close"].to_frame(name=tickers[0])

    return price_data.dropna()


def compute_log_returns(price_df):
    return np.log(price_df / price_df.shift(1)).dropna()