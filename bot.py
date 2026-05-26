import requests
import pandas as pd


# -----------------------------
# OBTENER DATOS BINANCE
# -----------------------------
def get_data(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1h",
        "limit": 100
    }

    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "trades", "tbbav", "tbqav", "ignore"
    ])

    df["close"] = df["close"].astype(float)
    return df


# -----------------------------
# INDICADORES SIMPLES
# -----------------------------
def calculate_indicators(df):
    df["return"] = df["close"].pct_change()
    df["ema"] = df["close"].ewm(span=20).mean()
    df["rsi"] = 50  # simplificado (puedes mejorar luego)

    return df


# -----------------------------
# SCORING SIMPLE (SIN ML)
# -----------------------------
def calculate_signal(df):
    last = df.iloc[-1]

    price = last["close"]
    ema = last["ema"]
    rsi = last["rsi"]

    score = 50

    if price > ema:
        score += 20
    else:
        score -= 20

    if rsi < 30:
        score += 15
    elif rsi > 70:
        score -= 15

    probability = max(0, min(100, score))

    return {
        "symbol": "BTCUSDT",
        "price": round(price, 2),
        "probability": round(probability, 1),
        "stop_loss": round(price * 0.98, 2),
        "take_profit": round(price * 1.04, 2),
        "score": score
    }


# -----------------------------
# FUNCIÓN PRINCIPAL
# -----------------------------
def analyze(symbol="BTCUSDT"):
    df = get_data(symbol)
    df = calculate_indicators(df)

    signal = calculate_signal(df)

    return signal