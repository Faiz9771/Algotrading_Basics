import datetime as dt
from turtle import title
import pandas as pd
import yfinance as yf

stocks = ["AMZN","MSFT","INTC","GOOG","INFY.NS","3988.HK"]
start = dt.datetime.today() - dt.timedelta(days=3600)
end = dt.datetime.today()
cl_price=pd.DataFrame()
ohlcv_data={}

for ticker in stocks:
    cl_price[ticker]=yf.download(ticker, start=start, end=end)["Close"]

cl_price.dropna(axis=0, how='any',inplace=True)
daily_return =cl_price.pct_change()


cl_price.plot(subplots=True, layout=(3,2),title="Stock price")

daily_return.plot(subplots=True,layout=(3,2),title="Daily returns")


#Compoounded retruns cumulative

(1+daily_return).cumprod().plot()