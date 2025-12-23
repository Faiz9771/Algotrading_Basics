from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading
import time
import pandas as pd


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        # dataframe to store positions
        self.pos_df = pd.DataFrame(columns=["Account","Symbol","SecType","Currency","Position","Avg cost"])
    
    def position(self, account, contract, position, avgCost):
        super().position(account, contract, position, avgCost)
        dictionary = {"Account":account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Currency": contract.currency, "Position": position, "Avg cost": avgCost}
        # append row without using deprecated DataFrame.append
        self.pos_df.loc[len(self.pos_df)] = dictionary

def websocket_con():
    app.run()

app = TradingApp()      
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) # some latency added to ensure that the connection is established


app.reqPositions()   # request positions for this account / client
time.sleep(3)        # give callbacks time to arrive
pos_df = app.pos_df
print(pos_df)