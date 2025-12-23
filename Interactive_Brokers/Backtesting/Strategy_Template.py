# ===================== IMPORTS =====================
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

import pandas as pd
import threading
import time
import itertools

# ===================== IB APP =====================
class TradeApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

        self.connected_flag = False
        self.next_order_id = None

        self.data = {}
        self.hist_complete = set()
        self.reqid_counter = itertools.count(1)

        self.pos_df = pd.DataFrame(
            columns=["Account", "Symbol", "SecType", "Currency", "Position", "AvgCost"]
        )

    # ---------- CONNECTION ----------
    def nextValidId(self, orderId):
        self.next_order_id = orderId
        self.connected_flag = True
        print(f"CONNECTED | nextOrderId = {orderId}")

    # ---------- HIST DATA ----------
    def historicalData(self, reqId, bar):
        row = {
            "Date": bar.date,
            "Open": bar.open,
            "High": bar.high,
            "Low": bar.low,
            "Close": bar.close,
            "Volume": bar.volume,
        }

        if reqId not in self.data:
            self.data[reqId] = pd.DataFrame([row])
        else:
            self.data[reqId] = pd.concat(
                [self.data[reqId], pd.DataFrame([row])], ignore_index=True
            )

    def historicalDataEnd(self, reqId, start, end):
        self.hist_complete.add(reqId)
        print(f"Historical data received for reqId {reqId}")

    # ---------- POSITIONS ----------
    def position(self, account, contract, position, avgCost):
        self.pos_df.loc[len(self.pos_df)] = [
            account,
            contract.symbol,
            contract.secType,
            contract.currency,
            position,
            avgCost,
        ]

    def positionEnd(self):
        pass


# ===================== CONTRACT =====================
def usStock(symbol):
    c = Contract()
    c.symbol = symbol
    c.secType = "STK"
    c.exchange = "SMART"
    c.primaryExchange = "NASDAQ"
    c.currency = "USD"
    return c


# ===================== ORDERS =====================
def marketOrder(side, qty):
    o = Order()
    o.action = side
    o.orderType = "MKT"
    o.totalQuantity = int(qty)
    o.tif = "DAY"
    return o


def stopOrder(side, qty, price):
    o = Order()
    o.action = side
    o.orderType = "STP"
    o.totalQuantity = int(qty)
    o.auxPrice = float(price)
    o.tif = "GTC"
    return o


# ===================== INDICATORS =====================
def MACD(df, a=12, b=26, c=9):
    df = df.copy()
    df["fast"] = df["Close"].ewm(span=a).mean()
    df["slow"] = df["Close"].ewm(span=b).mean()
    df["macd"] = df["fast"] - df["slow"]
    df["signal"] = df["macd"].ewm(span=c).mean()
    return df


def stochastic(df, n=20, d=3):
    low = df["Low"].rolling(n).min()
    high = df["High"].rolling(n).max()
    k = (df["Close"] - low) / (high - low) * 100
    return k.rolling(d).mean()


def atr(df, n=14):
    tr = pd.concat(
        [
            df["High"] - df["Low"],
            abs(df["High"] - df["Close"].shift()),
            abs(df["Low"] - df["Close"].shift()),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(span=n).mean()


# ===================== HIST FETCH =====================
def fetch_hist(app, contract):
    reqId = next(app.reqid_counter)

    app.reqHistoricalData(
        reqId=reqId,
        contract=contract,
        endDateTime="",
        durationStr="7 D",
        barSizeSetting="5 mins",
        whatToShow="ADJUSTED_LAST",
        useRTH=1,
        formatDate=1,
        keepUpToDate=0,
        chartOptions=[],
    )

    timeout = time.time() + 20
    while reqId not in app.hist_complete and time.time() < timeout:
        time.sleep(0.2)

    if reqId not in app.data:
        return None

    df = app.data[reqId].copy()
    df.set_index("Date", inplace=True)
    return df


# ===================== STRATEGY =====================
def run_strategy(app, tickers, capital):

    app.pos_df = app.pos_df.iloc[0:0]
    app.reqPositions()
    time.sleep(2)

    for ticker in tickers:
        print(f"\n--- Processing {ticker} ---")

        df = fetch_hist(app, usStock(ticker))
        if df is None or df.empty:
            print("No data")
            continue

        df["stoch"] = stochastic(df)
        macd_df = MACD(df)
        df["macd"] = macd_df["macd"]
        df["signal"] = macd_df["signal"]
        df["atr"] = atr(df)

        df.dropna(inplace=True)
        if df.empty:
            continue

        price = df["Close"].iloc[-1]
        qty = int(capital / price)

        if qty == 0:
            continue

        buy_signal = (
            df["macd"].iloc[-1] > df["signal"].iloc[-1]
            and df["stoch"].iloc[-1] > 30
            and df["stoch"].iloc[-1] > df["stoch"].iloc[-2]
        )

        print(
            f"Signal check | MACD={df['macd'].iloc[-1]:.3f} "
            f"Signal={df['signal'].iloc[-1]:.3f} "
            f"Stoch={df['stoch'].iloc[-1]:.1f}"
        )

        if buy_signal:
            print(f"BUY SIGNAL TRIGGERED for {ticker}")

            oid = app.next_order_id
            app.placeOrder(oid, usStock(ticker), marketOrder("BUY", qty))
            print(f"BUY order sent | orderId={oid}")
            app.next_order_id += 1

            time.sleep(1)

            sl_price = round(price - df["atr"].iloc[-1], 2)
            app.placeOrder(
                app.next_order_id,
                usStock(ticker),
                stopOrder("SELL", qty, sl_price),
            )
            print(f"STOP LOSS placed @ {sl_price}")
            app.next_order_id += 1


# ===================== RUN =====================
if __name__ == "__main__":

    tickers = ["AMZN", "INTC", "MSFT", "ADBE", "NFLX", "PYPL"]
    capital = 1000

    app = TradeApp()
    app.connect("127.0.0.1", 7497, clientId=24)

    threading.Thread(target=app.run, daemon=True).start()

    while not app.connected_flag:
        time.sleep(0.5)

    print("\n===== STARTING STRATEGY =====")

    start = time.time()
    while time.time() < start + 6 * 60 * 60:
        run_strategy(app, tickers, capital)
        time.sleep(300)
