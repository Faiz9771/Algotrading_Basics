from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

api_key = "107TEN02XS8XK18R"

ts = TimeSeries(key=api_key, output_format='pandas')
data = ts.get_daily(symbol='EURUSD', outputsize='compact')[0]
print(data)

data.columns = ['open', 'high', 'low', 'close', 'volume']
all_tickers = ["AAPL","MSFT","INTC","GOOG","3988.HK","EURUSD"]

data = data.iloc[::-1]
print(data)

close_prices = pd.DataFrame()

api_call_count = 0

for ticker in all_tickers:
    start_time = time.time()
    close_prices[ticker] = ts.get_intraday(symbol=ticker, interval='1min', outputsize='compact')[0]['4. close']
    api_call_count += 1
    if api_call_count ==5:
        api_call_count = 0
        time.sleep(60- (time.time()-start_time))