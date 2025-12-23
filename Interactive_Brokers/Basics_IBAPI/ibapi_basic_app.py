from ibapi import contract
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

#Either event or daemon can be used for multithreading

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
    
    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId, errorCode, errorString))
        
    def contractDetails(self, reqId, contractDetails):
        print("Reqid: {} contract: {}".format(reqId,contractDetails))


def websocket_con():
    app.run()
    event.wait()
    if(event.is_set()):
        app.close()


#Either event or daemon can be used for multithreading
event = threading.Event()

app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)

con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)



#Getting the contract info
contract = Contract()
contract.symbol="AAPL"
contract.secType = "STK"
contract.currency = "USD"
contract.exchange="SMART"

app.reqContractDetails(10004, contract)
time.sleep(5)
event.set()





