import os, time, requests, threading
from flask import Flask
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = "7690119458"
app = Flask(__name__)
ORO_BUY = 3890
last_alerts = {"oro":0,"eurusd":0}
def send_tg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except: pass
def get_prices():
    prices={"oro":0,"eurusd":0,"gbpusd":0}
    try:
        r=requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        prices["oro"]=float(r.get("price",0))
    except: pass
    try:
        f=requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
        rates=f.get("rates",{})
        if rates.get("EUR"): prices["eurusd"]=1/rates["EUR"]
        if rates.get("GBP"): prices["gbpusd"]=1/rates["GBP"]
    except: pass
    return prices
@app.route("/")
def home():
    p=get_prices()
    return f"RAUDY VIP ORO+FOREX LIVE - Oro: ${p['oro']:.2f} | EUR/USD: {p['eurusd']:.4f}"
def loop():
    while True:
        try:
            p=get_prices()
            now=time.time()
            if p["oro"]>0 and p["oro"]<ORO_BUY and now-last_alerts["oro"]>14400:
                send_tg(f"🔥 ORO: ${p['oro']:.2f} DEBAJO DE ${ORO_BUY} - COMPRA RAUDY!")
                last_alerts["oro"]=now
            if p["eurusd"]>0 and p["eurusd"]<1.08 and now-last_alerts["eurusd"]>14400:
                send_tg(f"💵 FOREX EUR/USD: {p['eurusd']:.4f} OPORTUNIDAD!")
                last_alerts["eurusd"]=now
            time.sleep(300)
        except: time.sleep(60)
threading.Thread(target=loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
