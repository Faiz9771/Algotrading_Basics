from ibapi.client import EClient
from ibapi.order import Order
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas as pd

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.nextOrderId = None
    
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextOrderId = orderId
        print("NextValidId:", orderId)

def websocket_con():
    app.run()

app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=2)

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

def limitOrder(action, qty, lmtPrice):
    order = Order()
    order.action = action
    order.orderType = "LMT"
    order.totalQuantity = qty
    order.lmtPrice = lmtPrice
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order

def marketOrder(action, qty):
    order = Order()
    order.action = action
    order.orderType = "MKT"
    order.totalQuantity = qty
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order

def stopOrder(action, qty, st_price):
    order = Order()
    order.action = action
    order.orderType = "STP"
    order.totalQuantity = qty
    order.auxPrice = st_price
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order

def trailstopOrder(action, qty, st_price, tr_step=1):
    order = Order()
    order.action = action
    order.orderType = "TRAIL"
    order.totalQuantity = qty
    order.auxPrice = tr_step
    order.trailStopPrice = st_price
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    return order

app.reqIds(-1)
time.sleep(2)
order_id = app.nextOrderId
app.placeOrder(order_id, usTechStk("TSLA"), trailstopOrder("BUY", 1, 1400,2))
time.sleep(5)
