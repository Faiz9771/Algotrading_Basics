# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import numpy as np
import threading
import time

class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self) 
        self.data = {}
        
    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = [{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}]
        else:
            self.data[reqId].append({"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume})
        print("reqID:{}, date:{}, open:{}, high:{}, low:{}, close:{}, volume:{}".format(reqId,bar.date,bar.open,bar.high,bar.low,bar.close,bar.volume))
def usTechStk(symbol,sec_type="STK",currency="USD",exchange="ISLAND"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract 

def histData(req_num,contract,duration,candle_size):
    """extracts historical data"""
    app.reqHistoricalData(reqId=req_num, 
                          contract=contract,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=0,
                          chartOptions=[])	 # EClient function to request contract details

def websocket_con():
    app.run()
    
app = TradeApp()
app.connect(host='127.0.0.1', port=7497, clientId=23) #port 4002 for ib gateway paper trading/7497 for TWS paper trading
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) # some latency added to ensure that the connection is established

tickers = ["META","AMZN","INTC"]
for ticker in tickers:
    histData(tickers.index(ticker),usTechStk(ticker),'2 D', '30 mins')
    time.sleep(5)

def dataDataframe(symbols,TradeApp_obj):
    "returns extracted historical data in dataframe format"
    df_data = {}
    for symbol in symbols:
        df_data[symbol] = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
        df_data[symbol].set_index("Date",inplace=True)
    return df_data

def stochastic_oscillator(DF,n=20, b=3):
    "function to calculate stochastic oscillator"
    df = DF.copy()
    df['highest_high'] = df['High'].rolling(window=n,center=False).max()
    df['lowest_low'] = df['Low'].rolling(window=n,center=False).min()
    df['%K'] = 100*((df['Close']-df['lowest_low'])/(df['highest_high']-df['lowest_low']))
    df['%D'] = df['%K'].ewm(span=b,min_periods=b).mean()
    return df[['%K','%D']]

#extract and store historical data in dataframe
historicalData = dataDataframe(tickers,app)

#calculate and store stochastic oscillator values
stochastic_df = {}
for ticker in tickers:
    stochastic_df[ticker] = stochastic_oscillator(historicalData[ticker],14)