import datetime as dt
import pandas as pd
import yfinance as yf

stocks = ["AMZN","MSFT","INTC","GOOG","INFY.NS","3988.HK"]
start = dt.datetime.today() - dt.timedelta(days=360)
end = dt.datetime.today()
cl_price=pd.DataFrame()
ohlcv_data={}



for ticker in stocks:
    cl_price[ticker]=yf.download(ticker, start=start, end=end)["Close"]

cl_price.dropna(axis=0, how='any',inplace=True)
cl_price.describe()
cl_price.mean()
cl_price.std()
cl_price.head()
cl_price.median()

daily_return =cl_price.pct_change()
daily_return.mean()*100
daily_return.std()*100


#rolling operations
rm = daily_return.rolling(window=10).mean()
daily_return.rolling(window=10).max()
daily_return.rolling(window=10).std()
daily_return.rolling(window=10).median()


#assigning weights according to recent 
em = daily_return.ewm(com=10,min_periods=10).mean()


for ticker in stocks:
    ohlcv_data[ticker]=yf.download(ticker, start=start, end=end)

print(ohlcv_data["MSFT"]["Open"])



