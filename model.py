import pandas as pd
import numpy as np
import requests
import joblib

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from sklearn.ensemble import RandomForestClassifier


def get_data():

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 500
    }

    data = requests.get(url, params=params, timeout=10).json()

    df = pd.DataFrame(data)

    df = df.iloc[:, :6]

    df.columns = ["t","o","h","l","c","v"]

    df["c"] = df["c"].astype(float)

    return df


def indicators(df):

    df["rsi"] = RSIIndicator(df["c"]).rsi()

    df["ema50"] = EMAIndicator(df["c"],50).ema_indicator()

    df["ema200"] = EMAIndicator(df["c"],200).ema_indicator()

    macd = MACD(df["c"])

    df["macd"] = macd.macd()

    df["signal"] = macd.macd_signal()

    df["target"] = (df["c"].shift(-1) > df["c"]).astype(int)

    df.dropna(inplace=True)

    return df


df = indicators(get_data())

X = df[["rsi","ema50","ema200","macd","signal"]]
y = df["target"]

model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Modelo listo ✔️")