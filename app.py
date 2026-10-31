import os, time, requests, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = "7690119458"
ORO_BUY = 3890
app = Flask(__name__)
last_alerts = {"oro":0,"eurusd":0}

def send_tg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
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
        if rates.get("EUR"): prices["eurusd"]=1/rates.get("EUR")
        if rates.get("GBP"): prices["gbpusd"]=1/rates.get("GBP")
    except: pass
    return prices

def monitor_oro():
    while True:
        try:
            p=get_prices()
            oro=p["oro"]
            if oro>0 and oro>=ORO_BUY:
                # evita spam cada 1 hora
                if time.time()-last_alerts["oro"]>3600:
                    send_tg(f"🚨 *ORO ALERTA VIP* 🚨\n\n💰 Precio actual: ${oro}\n📈 Ya llegó a tu compra: ${ORO_BUY}\n\n¡ATENTO RAUDY!")
                    last_alerts["oro"]=time.time()
        except: pass
        time.sleep(60)

@app.route('/')
def home():
    return "Raudy ORO Bot LIVE!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔥 BOT ORO VIP ACTIVO 🔥\n\nPrecio compra ORO: ${ORO_BUY}\nTu ID: {CHAT_ID}\n\nUsa /precio para ver precio actual")

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p=get_prices()
    await update.message.reply_text(f"💰 ORO: ${p['oro']}\n💵 EURUSD: {p['eurusd']}\n💷 GBPUSD: {p['gbpusd']}")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("precio", precio))
    application.run_polling()

# Iniciar hilos
threading.Thread(target=monitor_oro, daemon=True).start()
if BOT_TOKEN:
    threading.Thread(target=run_bot, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
