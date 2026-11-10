# app.py - RAUDY VIP 1000 - CALIDAD TOTAL ARREGLADO - COPIA TODO HASTA EL FINAL
import os, json, urllib.request, threading, time, random, math
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")
USAR_TESTNET = os.getenv("USAR_TESTNET", "True") == "True"
LINK_PAYPAL = "https://paypal.me/RaudyManzueta/20"
LINK_WHATSAPP = "https://wa.me/41767574050"
LINK_TELEGRAM = "https://t.me/raudy_vip_oro_bot"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "") or os.getenv("BOT_TOKEN", "") or os.getenv("BOT_TOKE", "") or os.getenv("BOT_TO", "")
CHAT_ID_JEFE = os.getenv("CHAT_ID_JEFE", "")
YAHOO = {"ORO": "GC=F", "TESLA": "TSLA", "APPLE": "AAPL", "META": "META", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/CHF": "CHF=X", "SP500": "^GSPC"}
BYBIT_BASE = "https://api-testnet.bybit.com" if USAR_TESTNET else "https://api.bybit.com"
BOT_AUTO = {"activo": False, "balance": 1000.0, "balance_inicial": 1000.0, "posicion": None, "precio_entrada": 0, "tp_objetivo": 0, "sl_objetivo": 0, "activo_actual": "ORO", "historial": [], "ultima_operacion": "BOT APAGADO", "ganadas": 0, "perdidas": 0, "perdidas_seguidas": 0, "total_ganado": 0.0, "total_perdido": 0.0, "trailing_sl": 0, "operaciones_manana": 0, "ganadas_manana": 0, "operaciones_noche": 0, "ganadas_noche": 0, "peor_balance": 1000.0, "mejor_balance": 1000.0}
HISTORIAL_PRECIOS_ORO = []
HISTORIAL_PRECIOS = {"ORO": [], "BTC": [], "EUR/USD": []}
RIESGO_POR_OPERACION = 10.0
GANANCIA_OBJETIVO = 20.0

def get_precio_real(simbolo_yahoo):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{simbolo_yahoo}?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            meta = data["chart"]["result"][0]["meta"]
            precio = meta.get("regularMarketPrice")
            return float(precio) if precio else None
    except Exception as e:
        print("Error precio", simbolo_yahoo, e)
        return None

def get_precio_bybit(symbol):
    try:
        url = f"{BYBIT_BASE}/v5/market/tickers?category=spot&symbol={symbol}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            lista = data.get("result", {}).get("list", [])
            if lista:
                return float(lista[0].get("lastPrice", 0))
    except Exception as e:
        print("Error Bybit", symbol, e)
    return None

def get_precios_reales_pasado(simbolo="GC=F", intervalo="1h", rango="1mo"):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{simbolo}?interval={intervalo}&range={rango}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
            result = data["chart"]["result"][0]
            closes = result["indicators"]["quote"][0]["close"]
            precios = [float(x) for x in closes if x is not None]
            return precios
    except Exception as e:
        print("Error precios reales pasado", e)
        return []

def senal_bybit(precio, tp, sl):
    if precio <= sl + 15:
        return "COMPRAR - JEFE ESTA BARATO"
    if precio >= tp - 15:
        return "VENDER - JEFE YA ESTA CARO"
    return "ESPERA - JEFE TODAVIA NO"

def calcular_rsi(precios, periodo=14):
    if len(precios) < periodo + 1:
        return 50
    ganancias = 0
    perdidas = 0
    for i in range(1, periodo + 1):
        diff = precios[-i] - precios[-i-1]
        if diff > 0:
            ganancias += diff
        else:
            perdidas += abs(diff)
    if perdidas == 0:
        return 100
    rs = (ganancias / periodo) / (perdidas / periodo)
    return 100 - (100 / (1 + rs))

def calcular_tendencia(precios):
    if len(precios) < 10:
        return "SIN DATOS"
    ultimos_5 = sum(precios[-5:]) / 5
    anteriores_5 = sum(precios[-10:-5]) / 5
    if ultimos_5 > anteriores_5:
        return "SUBIENDO"
    if ultimos_5 < anteriores_5:
        return "BAJANDO"
    return "LADO"

def calcular_ema(precios, periodo):
    if len(precios) < periodo:
        return sum(precios) / len(precios) if precios else 0
    k = 2 / (periodo + 1)
    ema = sum(precios[:periodo]) / periodo
    for p in precios[periodo:]:
        ema = p * k + ema * (1 - k)
    return ema

def calcular_macd(precios):
    if len(precios) < 26:
        return {"macd": 0, "senal": 0, "histograma": 0, "texto": "SIN DATOS"}
    ema12 = calcular_ema(precios, 12)
    ema26 = calcular_ema(precios, 26)
    macd_linea = ema12 - ema26
    senal = macd_linea * 0.9
    hist = macd_linea - senal
    if hist > 0:
        texto = "FUERZA SUBIENDO"
    elif hist < 0:
        texto = "FUERZA
