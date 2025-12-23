import yfinance as yf

# -----------------------------
# CONFIG
# -----------------------------
tickers = ["AMZN", "GOOG", "MSFT"]
ohlcv_data = {}

# -----------------------------
# DATA DOWNLOAD + CLEANING
# -----------------------------
for ticker in tickers:
    temp = yf.download(
        ticker,
        period="1mo",
        interval="5m",
        prepost=False,
        progress=False
    )

    # 🔑 FIX 1: Remove duplicate columns (yfinance bug)
    temp = temp.loc[:, ~temp.columns.duplicated()]

    # 🔑 FIX 2: Convert US market time → IST
    if temp.index.tz is not None:
        temp.index = (
            temp.index
            .tz_convert("Asia/Kolkata")
            .tz_localize(None)
        )

    temp.dropna(inplace=True)
    ohlcv_data[ticker] = temp


# -----------------------------
# BOLLINGER BANDS (TradingView accurate)
# -----------------------------
def Bollinger_Band(DF, n=20):
    df = DF.copy()

    # Force Series (avoids DataFrame assignment bug)
    close = df["Close"].astype(float)

    mb = close.rolling(window=n, min_periods=n).mean()
    sd = close.rolling(window=n, min_periods=n).std(ddof=0)  # TradingView uses ddof=0

    df["MB"] = mb
    df["UB"] = mb + 2 * sd
    df["LB"] = mb - 2 * sd
    df["BB_Width"] = df["UB"] - df["LB"]

    return df[["MB", "UB", "LB", "BB_Width"]]


# -----------------------------
# APPLY INDICATOR
# -----------------------------
for ticker in ohlcv_data:
    bb = Bollinger_Band(ohlcv_data[ticker])
    ohlcv_data[ticker] = ohlcv_data[ticker].join(bb)
