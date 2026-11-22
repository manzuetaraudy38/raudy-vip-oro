import time
import pandas as pd
import ccxt
import requests
import matplotlib.pyplot as plt
from flask import Flask

app = Flask(__name__)

# ==============================
# CONFIGURACIÓN
# ==============================
MONEDA = 'BTC/USDT'
TIMEFRAME = '1m'
CANTIDAD_USDT = 20
TP = 0.002
SL = 0.0015
INTERVALO = 5

# ==============================
# EXCHANGE
# ==============================
exchange = ccxt.binance({
    'enableRateLimit': True,
})

def decir(mensaje):
    # Antes era voz, ahora es print porque Render no tiene bocina
    print(mensaje, flush=True)

def obtener_datos():
    try:
        ohlcv = exchange.fetch_ohlcv(MONEDA, timeframe=TIMEFRAME, limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error obteniendo datos: {e}", flush=True)
        return None

def calcular_ema(df, periodo=20):
    return df['close'].ewm(span=periodo, adjust=False).mean()

@app.route('/')
def inicio():
    return "Bot activo - Jefe, ya esta Live!"

@app.route('/status')
def status():
    df = obtener_datos()
    if df is None:
        return "Sin datos"
    ema = calcular_ema(df).iloc[-1]
    precio = df['close'].iloc[-1]
    return f"Precio: {precio} - EMA20: {ema}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
