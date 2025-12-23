from datetime import date
from tracemalloc import start
from ibapi import contract
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas as pd

#Either event or daemon can be used for multithreading

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.data = {}
    
    def historicalData(self, reqId: int, bar):
        if reqId not in self.data:
            self.data[reqId] = [{"date":bar.date, "Open":bar.open, "High":bar.high, "Low":bar.low, "Close":bar.close}]
        if reqId in self.data:
            self.data[reqId].append({"date":bar.date, "Open":bar.open, "High":bar.high, "Low":bar.low, "Close":bar.close})
        print("reqId:{}, date:{}, open:{}, high:{}, low:{}, close:{}, volume:{}".format(reqId, bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume))


def websocket_con():
    app.run()

app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)

con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)

def usTechStk(symbol, secType="STK",currency="USD", exchange="NASDAQ"):
    contract = Contract()
    contract.symbol=symbol
    contract.secType = secType
    contract.currency = currency
    contract.exchange=exchange
    return contract

def histData(req_num, contract, duration, candle_size):
    app.reqHistoricalData(reqId=req_num, 
                        contract=contract,
                        endDateTime='',
                        durationStr=duration,
                        barSizeSetting=candle_size,
                        whatToShow='ADJUSTED_LAST',
                        useRTH=1,
                        formatDate=1,
                        keepUpToDate=0,
                        chartOptions=[])	



def dataDataframe(tradeapp_obj, tickers):
    df_dict = {}
    for ticker in tickers:
        df_dict[ticker] = pd.DataFrame(tradeapp_obj.data[tickers.index(ticker)])
        df_dict[ticker].set_index("date", inplace=True)
    return df_dict

starttime = time.time()
timeout = starttime + 60*5
tickers = ["META","AMZN","INTC"]

while time.time()<=timeout:
    for ticker in tickers:
        histData(tickers.index(ticker), contract=usTechStk(ticker), duration="3600 S", candle_size="30 secs")
        time.sleep(3)
    historical_data = dataDataframe(app, tickers)
    time.sleep(30 - (time.time()-starttime)%30)

ohlcv = dataDataframe(app, tickers)