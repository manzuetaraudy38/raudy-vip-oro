import os
import pandas as pd
import ccxt
import requests
from flask import Flask

app = Flask(__name__)

# --- TU CONFIGURACION JEFE ---
SYMBOL = 'PAXG/USDT'  # ORO - TU QUERIAS ORO JEFE, ANTES ERA BTC
TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h']
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', 'TU_TOKEN_DE_TELEGRAM')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'TU_CHAT_ID')

exchange = ccxt.binance({'enableRateLimit': True})

def get_velas(symbol, timeframe, limit=250):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['time','open','high','low','close','volume'])
    return df

def calcular(df):
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def analizar():
    senales = {}
    datos = {}
    for tf in TIMEFRAMES:
        try:
            df = calcular(get_velas(SYMBOL, tf))
            u = df.iloc[-1]
            senal = "NEUTRO ⏳"
            if u['close'] > u['EMA50'] > u['EMA200'] and 50 < u['RSI'] < 70:
                senal = "SUBE 🟢"
            elif u['close'] < u['EMA50'] < u['EMA200'] and 30 < u['RSI'] < 50:
                senal = "BAJA 🔴"
            senales[tf] = senal
            datos[tf] = {"precio": round(float(u['close']),2), "ema50": round(float(u['EMA50']),2), "ema200": round(float(u['EMA200']),2), "rsi": round(float(u['RSI']),1), "senal": senal}
        except Exception as e:
            senales[tf] = "ERROR"
            datos[tf] = {"precio":0,"ema50":0,"ema200":0,"rsi":0,"senal":"ERROR"}
    return senales, datos

@app.route('/')
def inicio():
    senales, datos = analizar()
    # AVISO FUERTE JEFE - TU LOGICA
    if senales.get('4h')=="SUBE 🟢" and senales.get('1h')=="SUBE 🟢" and senales.get('15m')=="SUBE 🟢":
        aviso = "🚀 JEFE VA A SUBIR! ENTRA AHORA JEFE"
        color_aviso = "#00ff00"
    elif senales.get('4h')=="BAJA 🔴" and senales.get('1h')=="BAJA 🔴" and senales.get('15m')=="BAJA 🔴":
        aviso = "📉 JEFE VA A BAJAR! CUIDADO JEFE - NO ENTRES"
        color_aviso = "#ff4444"
    else:
        aviso = "⏳ ESPERANDO JEFE... NO HAY ACUERDO"
        color_aviso = "#FFD700"

    filas = ""
    for tf in TIMEFRAMES:
        d = datos[tf]
        filas += f"<tr><td><b>{tf}</b></td><td>${d['precio']}</td><td>{d['rsi']}</td><td>{d['senal']}</td></tr>"

    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#0a0a0a;color:#fff;font-family:Arial;text-align:center;padding:15px}}
    .card{{background:#111;border:2px solid #FFD700;border-radius:20px;padding:20px;max-width:480px;margin:auto;box-shadow:0 0 30px #FFD70055}}
    h1{{color:#FFD700;margin:0;font-size:30px}} .live{{color:#00ff00;font-weight:bold}}
    .aviso{{background:{color_aviso};color:#000;padding:14px;border-radius:12px;font-weight:bold;font-size:18px;margin:15px 0}}
    table{{width:100%;border-collapse:collapse;margin-top:10px}} td,th{{padding:10px;border-bottom:1px solid #333}} th{{color:#FFD700}}
    button{{background:#FFD700;border:none;padding:12px 25px;border-radius:10px;font-weight:bold;margin-top:15px}}
    </style></head><body><div class="card">
    <p class="live">● LIVE</p><h1>👑 RAUDY ORO</h1><p>JEFE - EMA 50 + EMA 200 + RSI</p>
    <div class="aviso">{aviso}</div>
    <table><tr><th>TF</th><th>PRECIO</th><th>RSI</th><th>SEÑAL</th></tr>{filas}</table>
    <button onclick="location.reload()">🔄 ACTUALIZAR</button>
    <p style="color:#888;font-size:12px">ORO / PAXG - 1m 5m 15m 1h 4h</p>
    </div></body></html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
