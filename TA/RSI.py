import yfinance as yf
import numpy as np

tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data={}

for ticker in tickers:
    temp=yf.download(ticker, period="1mo", interval="15m")
    temp.index = (
        temp.index
        .tz_convert("Asia/Kolkata")
        .tz_localize(None)
    )
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker]=temp
    
def RSI(DF,n=14):
    df=DF.copy()
    df["Change"] = df["Close"] - df["Close"].shift(1)
    df["Gain"] = np.where(df["Change"]>=0,df["Change"],0)
    df["Loss"] = np.where(df["Change"]<0,df["Change"]*(-1),0)
    df["avgGain"] = df["Gain"].ewm(alpha=1/n,min_periods=n).mean()
    df["avgLoss"] = df["Loss"].ewm(alpha=1/n,min_periods=n).mean()
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["rsi"] = 100-(100/(1+df["rs"]))
    return df["rsi"]

for ticker in ohlcv_data:
    ohlcv_data[ticker]["rsi"] = RSI(ohlcv_data[ticker])
    