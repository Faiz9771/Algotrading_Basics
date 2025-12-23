import yfinance as yf
from stocktrends import Renko
import pandas as pd
# -----------------------------
# CONFIG
# -----------------------------
tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}
hour_data = {}
renko_data = {}

# -----------------------------
# DOWNLOAD DATA
# -----------------------------
for ticker in tickers:
    # 5-minute data
    temp_5m = yf.download(
        ticker,
        period="1mo",
        interval="5m",
        prepost=False,
        progress=False
    )

    temp_5m = temp_5m.loc[:, ~temp_5m.columns.duplicated()]
    temp_5m.dropna(inplace=True)
    ohlcv_data[ticker] = temp_5m

    # 1-hour data (for ATR)
    temp_1h = yf.download(
        ticker,
        period="1y",
        interval="1h",
        prepost=False,
        progress=False
    )

    temp_1h = temp_1h.loc[:, ~temp_1h.columns.duplicated()]
    temp_1h.dropna(inplace=True)
    hour_data[ticker] = temp_1h


# -----------------------------
# ATR (Wilder – TradingView accurate)
# -----------------------------
def ATR(DF, n=14):
    df = DF.copy()

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)

    atr = tr.ewm(alpha=1/n, adjust=False).mean()
    return atr


# -----------------------------
# RENKO FUNCTION (FIXED)
# -----------------------------
def renko_DF(DF, hourly_df):
    df = DF.copy()

    # Keep only required columns
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    # Reset index → date column
    df.reset_index(inplace=True)

    # Rename EXACTLY as Renko expects
    df.columns = ["date", "open", "high", "low", "close", "volume"]

    # Create Renko object
    renko = Renko(df)

    # Brick size = 3 × ATR(120) from hourly data
    brick_size = round(ATR(hourly_df, 120).iloc[-1], 2)
    renko.brick_size = 3 * brick_size

    renko_df = renko.get_ohlc_data()
    return renko_df


# -----------------------------
# BUILD RENKO DATA
# -----------------------------
for ticker in ohlcv_data:
    renko_data[ticker] = renko_DF(
        ohlcv_data[ticker],
        hour_data[ticker]
    )
