import yfinance as yf

tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data={}

for ticker in tickers:
    temp=yf.download(ticker, period="1mo", interval="5m")
    temp.index = (
        temp.index
        .tz_convert("Asia/Kolkata")
        .tz_localize(None)
    )
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker]=temp

def ATR(DF, n=14):
    df=DF.copy()
    df["H-L"] = df["High"]-df["Low"]
    df["H-PC"] = df["High"]-df["Close"].shift(1).abs()
    df["L-PC"] = df["Low"]-df["Close"].shift(1).abs()
    df["TR"] = df[["H-L","H-PC","L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(alpha=1/n, adjust=False).mean()
    return df["ATR"]

for ticker in ohlcv_data:
    ohlcv_data[ticker]["ATR"] = ATR(ohlcv_data[ticker])
        