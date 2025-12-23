import matplotlib.pyplot as plt
import datetime as dt
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

plt.style.use('ggplot')
fig,ax = plt.subplots()
ax.set(title="Mean daily return of Stocks", xlabel="Stocks", ylabel="Mean Return")
plt.bar(x=daily_return.columns,height=daily_return.mean())
plt.bar(x=daily_return.columns,height=daily_return.std())