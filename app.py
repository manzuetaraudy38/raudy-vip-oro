import os, time, requests, threading
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHAT_ID = "7690119458"

# TUS NIVELES VIP
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
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=15)
        print(f"Enviado: {text[:50]}")
    except Exception as e:
        print(f"Error send_tg: {e}")

def get_prices():
    prices = {"oro": 0, "eurusd": 0, "gbpusd": 0}
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
    return f"RAUDY VIP LIVE ✅ ORO: ${p['oro']:.2f} | EURUSD: {p['eurusd']:.5f} | GBPUSD: {p['gbpusd']:.5f}"

@app.route('/todo')
def todo_web():
    p = get_prices()
    msg = f"🔥 RAUDY VIP MERCADO 🔥\n\n💰 ORO: ${p['oro']:.2f} (Compra: {ORO_BUY})\n💶 EURUSD: {p['eurusd']:.5f} (Compra: {EURUSD_BUY})\n💷 GBPUSD: {p['gbpusd']:.5f} (Compra: {GBPUSD_BUY})"
    send_tg(msg)
    return msg.replace("\n", "<br>")

def monitor_loop():
    print("Monitor iniciado - ORO + DIVISAS")
    while True:
        try:
            p = get_prices()
            now = time.time()
            # ORO
            if p["oro"] > 1000 and p["oro"] <= ORO_BUY and (now - last_alert["oro"] > 14400):
                send_tg(f"🔔 <b>VIP ORO COMPRA</b>\n💰 Precio: ${p['oro']:.2f}\n🎯 Nivel: {ORO_BUY}\n⏰ AHORA!")
                last_alert["oro"] = now
            # EURUSD
            if p["eurusd"] > 0.5 and p["eurusd"] <= EURUSD_BUY and (now - last_alert["eurusd"] > 14400):
                send_tg(f"💶 <b>EURUSD COMPRA</b>\nPrecio: {p['eurusd']:.5f}\nNivel: {EURUSD_BUY}")
                last_alert["eurusd"] = now
        except Exception as e:
            print(f"Error monitor: {e}")
        time.sleep(120)

# Iniciar monitor en hilo
threading.Thread(target=monitor_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
