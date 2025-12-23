import yfinance as yf

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
    


def MACD(DF, a=12 ,b=26, c=9):
    """function to calculate MACD
       typical values a(fast moving average) = 12; 
                      b(slow moving average) =26; 
                      c(signal line ma window) =9"""
    df = DF.copy()
    df["ma_fast"] = df["Close"].ewm(span=a, min_periods=a, adjust=False).mean()
    df["ma_slow"] = df["Close"].ewm(span=b, min_periods=b, adjust=False).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["macd"].ewm(span=c, min_periods=c, adjust=False).mean()
    return df.loc[:,["macd","signal"]]

for ticker in ohlcv_data:
    ohlcv_data[ticker][["MACD","SIGNAL"]] = MACD(ohlcv_data[ticker], a=12 ,b=26, c=9)