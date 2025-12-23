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
    histData(tickers.index(ticker),usTechStk(ticker),'2 D', '5 mins')
    time.sleep(5)

def dataDataframe(symbols,TradeApp_obj):
    "returns extracted historical data in dataframe format"
    df_data = {}
    for symbol in symbols:
        df_data[symbol] = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
        df_data[symbol].set_index("Date",inplace=True)
    return df_data


def RSI(DF,n=20):
    df=DF.copy()
    df["Change"] = df["Close"] - df["Close"].shift(1)
    df["Gain"] = np.where(df["Change"]>=0,df["Change"],0)
    df["Loss"] = np.where(df["Change"]<0,df["Change"]*(-1),0)
    avg_gain=[]
    avg_loss=[]
    Gain = df["Gain"].tolist()
    Loss = df["Loss"].tolist()
    for i in range(len(df)):
        if i<n:
            avg_gain.append(np.nan)
            avg_loss.append(np.nan)
        elif i==n:
            avg_gain.append(df["Gain"].rolling(n).mean()[n])
            avg_loss.append(df["Loss"].rolling(n).mean()[n])
        elif i>n:
            avg_gain.append(((n-1)*avg_gain[i-1] + Gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + Loss[i])/n)
            
    df["avg_gain"] = np.array(avg_gain)
    df["avg_loss"] = np.array(avg_loss)
    df["rs"] = df["avg_gain"]/df["avg_loss"]
    df["rsi"] = 100-(100/(1+df["rs"]))
    return df["rsi"]

#extract and store historical data in dataframe
historicalData = dataDataframe(tickers,app)

#calculate and store MACD values
rsi_df = {}
for ticker in tickers:
    rsi_df[ticker] = RSI(historicalData[ticker],20)
