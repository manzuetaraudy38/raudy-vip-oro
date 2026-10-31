import os, time, requests, threading
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHAT_ID = "7690119458"

ORO_BUY = 3890
EURUSD_BUY = 1.0850
GBPUSD_BUY = 1.2650

last_alert = {"oro":0, "eurusd":0, "gbpusd":0}

def send_tg(text):
    if not BOT_TOKEN or len(BOT_TOKEN) < 10:
        print("BOT_TOKEN no configurado")
        return
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
        print(f"Enviado: {text[:60]}")
    except Exception as e:
        print(f"Error send_tg: {e}")

def get_prices():
    prices = {"oro":0, "eurusd":0, "gbpusd":0}
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        prices["oro"] = float(r.get("price", 0))
    except Exception as e:
        print(f"Error oro: {e}")
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
        rates = r.get("rates", {})
        if rates.get("EUR"):
            prices["eurusd"] = 1.0 / rates["EUR"]
        if rates.get("GBP"):
            prices["gbpusd"] = 1.0 / rates["GBP"]
    except Exception as e:
        print(f"Error divisas: {e}")
    return prices

@app.route('/')
def home():
    p = get_prices()
    html = f"""
    <!DOCTYPE html>
    <html><head><title>RAUDY VIP ORO LIVE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#0a0a0a;color:gold;font-family:Arial;text-align:center;padding:15px}}
    .card{{background:#1a1a1a;border:2px solid gold;border-radius:15px;padding:20px;margin:15px auto;max-width:400px}}
    .price{{font-size:32px;font-weight:bold}} .live{{color:#00ff00}}
    .btn{{background:gold;color:#000;padding:15px 30px;border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;margin:10px}}
    </style></head><body>
    <h1>👑 RAUDY VIP ORO 👑</h1><div class="live">● LIVE ✅</div>
    <div class="card"><h2>ORO: ${p['oro']:.2f}</h2><p>Nivel compra VIP: {ORO_BUY}</p></div>
    <div class="card"><p>EURUSD: {p['eurusd']:.5f} | GBPUSD: {p['gbpusd']:.5f}</p></div>
    <div class="card"><p>BOT ACTIVO 24/7 - Alertas a Telegram</p></div>
    <a class="btn" href="/todo">VER MERCADO COMPLETO</a>
    </body></html>
    """
    return html

@app.route('/todo')
def todo_web():
    p = get_prices()
    msg = f"🔥 RAUDY VIP MERCADO 🔥\n\n💰 ORO: ${p['oro']:.2f}\nEURUSD: {p['eurusd']:.5f}\nGBPUSD: {p['gbpusd']:.5f}"
    send_tg(msg)
    return msg.replace("\n", "<br>")

def monitor_loop():
    print("Monitor iniciado - ORO + DIVISAS")
    while True:
        try:
            p = get_prices()
            now = time.time()
            if p["oro"] > 1000 and p["oro"] <= ORO_BUY:
                if now - last_alert["oro"] > 3600:
                    send_tg(f"🔔 <b>VIP ORO COMPRA</b> ORO: ${p['oro']:.2f} cerca de {ORO_BUY}")
                    last_alert["oro"] = now
            print(f"Chequeo: ORO {p['oro']}")
            time.sleep(300)
        except Exception as e:
            print(f"Error loop: {e}")
            time.sleep(60)

threading.Thread(target=monitor_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)))
