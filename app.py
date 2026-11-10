# ============================================================
# RAUDY VIP PRO - TODO JUNTO - AUTOMATICO + TRADINGVIEW + TELEGRAM + VOZ
# Jefe: Raudy Manzueta - PayPal: paypal.me/RaudyManzueta/20
# Bot: @raudy_vip_oro_bot
# ============================================================
import os, random, threading, time, requests
try:
    import yfinance as yf
except:
    yf = None
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ============ CONFIGURACION - TUS LLAVES ============
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "767574050")
PAYPAL_LINK = "https://paypal.me/RaudyManzueta/20"
TELEGRAM_LINK = "https://t.me/raudy_vip_oro_bot"

# ============ DINERO DEMO Y REGLAS ============
dinero_demo = 1000.0
posicion_abierta = None
operaciones_hoy = 0
ganancia_hoy = 0.0
ultima_señal = "Robot encendido, esperando señal..."
ultima_voz = "Jefe, ya estoy encendido y trabajando solo."
historial = ["🤖 RAUDY VIP PRO ENCENDIDO - TODO JUNTO"]
precios = {}
senal_por_activo = {}

# ============ TUS 14 ACTIVOS ============
ACTIVOS = {
    "ORO": "GC=F", "BTC": "BTC-USD",
    "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "USDJPY=X",
    "USD/CHF": "USDCHF=X", "AUD/USD": "AUDUSD=X", "USD/CAD": "USDCAD=X",
    "TESLA": "TSLA", "META": "META", "APPLE": "AAPL", "AMAZON": "AMZN", "NVIDIA": "NVDA",
    "SP500": "^GSPC"
}

# ============ TELEGRAM ============
def mandar_telegram(mensaje):
    if not TELEGRAM_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "
