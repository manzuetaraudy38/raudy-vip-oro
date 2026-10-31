import os, time, requests, threading
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = "7690119458"
app = Flask(__name__)

# CONFIGURACION TUYA RAUDY
ORO_BUY = 3890
last_alerts = {"oro":0, "eurusd":0, "gbpusd":0}

def send_tg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def get_prices():
    prices = {}
    try:
        # ORO
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=8).json()
        prices["oro"] = float(r.get("price",0))
    except: prices["oro"] = 0
    try:
        # FOREX - gratis
        r = requests.get("https://api.gold-api.com/price/EUR", timeout=8).json()
        # usamos forex de exchangerate
        f = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8).json()
        rates = f.get("rates",{})
        prices["eurusd"] = 1 / rates.get("EUR",1) if rates.get("EUR") else 0
        prices["gbpusd"] = 1 / rates.get("GBP",1) if rates.get("GBP") else 0
        prices["usdjpy"] = rates.get("JPY",0)
    except: 
        prices["eurusd"]=0
        prices["gbpusd"]=0
    return prices

@app.route("/")
def home():
    p=get_prices()
    return f"<h1>RAUDY VIP: ORO + FOREX LIVE</h1> Oro:${p.get('oro')} | EUR/USD:{p.get('eurusd')} | GBP/USD:{p.get('gbpusd')}"

def loop():
    while True:
        try:
            p=get_prices()
            now=time.time()
            # ORO
            if p["oro"]>0 and p["oro"]<ORO_BUY and now-last_alerts["oro"]>14400:
                send_tg(f"🔥 RAUDY ORO: ${p['oro']:.2f} DEBAJO DE ${ORO_BUY} - COMPRAR!")
                last_alerts["oro"]=now
            # FOREX EURUSD bajo 1.08 por ejemplo
            if p["eurusd"]>0 and p["eurusd"]<1.08 and now-last_alerts["eurusd"]>14400:
                send_tg(f"💵 FOREX EUR/USD: {p['eurusd']:.4f} OPORTUNIDAD!")
                last_alerts["eurusd"]=now
            time.sleep(300)
        except: time.sleep(60)

threading.Thread(target=loop, daemon=True).start()
app.run(host="0.0.0.0", port=10000)
