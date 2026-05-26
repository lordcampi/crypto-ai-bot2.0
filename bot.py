import requests
import numpy as np
import pandas as pd
import joblib

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange

model = joblib.load("model.pkl")

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]


def get_data(symbol):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": "1h",
        "limit": 200
    }

    data = requests.get(url, params=params, timeout=10).json()

    df = pd.DataFrame(data)

    df = df.iloc[:, :6]

    df.columns = ["t","o","h","l","c","v"]

    for col in ["o","h","l","c","v"]:
        df[col] = df[col].astype(float)

    return df


def indicators(df):

    df["rsi"] = RSIIndicator(df["c"]).rsi()

    df["ema50"] = EMAIndicator(df["c"], 50).ema_indicator()

    df["ema200"] = EMAIndicator(df["c"], 200).ema_indicator()

    macd = MACD(df["c"])

    df["macd"] = macd.macd()

    df["signal"] = macd.macd_signal()

    atr = AverageTrueRange(df["h"], df["l"], df["c"])

    df["atr"] = atr.average_true_range()

    df.dropna(inplace=True)

    return df


def analyze():

    best = None
    best_score = -999

    for s in SYMBOLS:

        df = get_data(s)
        df = indicators(df)

        last = df.iloc[-1]

        X = np.array([[
            last["rsi"],
            last["ema50"],
            last["ema200"],
            last["macd"],
            last["signal"]
        ]])

        prob = model.predict_proba(X)[0][1]

        price = last["c"]

        score = prob

        # hedge fund scoring suave
        if 45 < last["rsi"] < 55:
            score -= 0.05

        if last["ema50"] < last["ema200"]:
            score -= 0.10
        else:
            score += 0.10

        if last["atr"] < price * 0.002:
            score -= 0.05

        signal = {
            "symbol": s,
            "price": price,
            "probability": round(prob * 100, 2),
            "score": round(score, 3),
            "stop_loss": round(price * 0.98, 2),
            "take_profit": round(price * 1.04, 2)
        }

        if score > best_score:
            best_score = score
            best = signal

    return best