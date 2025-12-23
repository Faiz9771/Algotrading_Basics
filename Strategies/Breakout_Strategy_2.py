import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import copy
import matplotlib.pyplot as plt

def ATR(DF, n):
    df = DF.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    return df['ATR']


def CAGR(DF):
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df) / (252 * 78)
    return df["cum_return"].iloc[-1]**(1/n) - 1


def volatility(DF):
    return DF["ret"].std() * np.sqrt(252 * 78)


def sharpe(DF, rf):
    return (CAGR(DF) - rf) / volatility(DF)


def max_dd(DF):
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
    return df["drawdown_pct"].max()

tickers = ["MSFT","AAPL","META","AMZN","INTC","CSCO","VZ","IBM","TSLA","AMD"]

ohlc_intraday = {}

for ticker in tickers:
    print("Downloading", ticker)

    df = yf.download(
        ticker,
        period="60d",           # yfinance intraday limit
        interval="5m",
        prepost=False,
        auto_adjust=False,
        progress=False
    )

    df = df.loc[:, ~df.columns.duplicated()]
    df.dropna(inplace=True)

    # Convert to US market hours
    df.index = df.index.tz_convert("America/New_York")
    df = df.between_time("09:35", "16:00")

    ohlc_intraday[ticker] = df

ohlc_dict = copy.deepcopy(ohlc_intraday)
tickers_signal = {}
tickers_ret = {}


for ticker in tickers:
    print("Preparing indicators for", ticker)

    df = ohlc_dict[ticker]
    df["ATR"] = ATR(df, 20)
    df["roll_max_cp"] = df["High"].rolling(20).max()
    df["roll_min_cp"] = df["Low"].rolling(20).min()
    df["roll_max_vol"] = df["Volume"].rolling(20).max()
    df.dropna(inplace=True)

    tickers_signal[ticker] = ""
    tickers_ret[ticker] = [0]
    
high = df["High"].values
low = df["Low"].values
close = df["Close"].values
volume = df["Volume"].values
atr = df["ATR"].values
roll_max_cp = df["roll_max_cp"].values
roll_min_cp = df["roll_min_cp"].values
roll_max_vol = df["roll_max_vol"].values

for ticker in tickers:
    print("Backtesting", ticker)
    df = ohlc_dict[ticker]
    returns = np.zeros(len(df))

    # ---- FIX (ONLY THIS PART IS NEW) ----
    high = df["High"].values
    low = df["Low"].values
    close = df["Close"].values
    volume = df["Volume"].values
    atr = df["ATR"].values
    roll_max_cp = df["roll_max_cp"].values
    roll_min_cp = df["roll_min_cp"].values
    roll_max_vol = df["roll_max_vol"].values
    # ------------------------------------

    for i in range(1, len(df)):
        if tickers_signal[ticker] == "":
            returns[i] = 0

            if (
                high[i] >= roll_max_cp[i] and
                volume[i] > 1.5 * roll_max_vol[i-1]
            ):
                tickers_signal[ticker] = "Buy"

            elif (
                low[i] <= roll_min_cp[i] and
                volume[i] > 1.5 * roll_max_vol[i-1]
            ):
                tickers_signal[ticker] = "Sell"

        elif tickers_signal[ticker] == "Buy":
            if low[i] < close[i-1] - atr[i-1]:
                tickers_signal[ticker] = ""
                returns[i] = ((close[i-1] - atr[i-1]) / close[i-1]) - 1

            elif (
                low[i] <= roll_min_cp[i] and
                volume[i] > 1.5 * roll_max_vol[i-1]
            ):
                tickers_signal[ticker] = "Sell"
                returns[i] = (close[i] / close[i-1]) - 1

            else:
                returns[i] = (close[i] / close[i-1]) - 1

        elif tickers_signal[ticker] == "Sell":
            if high[i] > close[i-1] + atr[i-1]:
                tickers_signal[ticker] = ""
                returns[i] = (close[i-1] / (close[i-1] + atr[i-1])) - 1

            elif (
                high[i] >= roll_max_cp[i] and
                volume[i] > 1.5 * roll_max_vol[i-1]
            ):
                tickers_signal[ticker] = "Buy"
                returns[i] = (close[i-1] / close[i]) - 1

            else:
                returns[i] = (close[i-1] / close[i]) - 1

    # ensure returns align 1:1 with df rows and stay numeric
    df["ret"] = returns



strategy_df = pd.DataFrame()
for ticker in tickers:
    strategy_df[ticker] = ohlc_dict[ticker]["ret"]

strategy_df["ret"] = strategy_df.mean(axis=1)

print("CAGR:", CAGR(strategy_df))
print("Sharpe:", sharpe(strategy_df, 0.025))
print("Max DD:", max_dd(strategy_df))

(1 + strategy_df["ret"]).cumprod().plot(
    title="Intraday Resistance Breakout Strategy",
    figsize=(10,5)
)
plt.show()


