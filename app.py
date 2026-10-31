import os, time, requests, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = "7690119458"

# CONFIGURA TUS NIVELES VIP
ORO_BUY = 3890
EURUSD_BUY = 1.0850
GBPUSD_BUY = 1.2650

app = Flask(__name__)
last_alerts = {"oro":0, "eurusd":0, "gbpusd":0}

def send_tg(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
    except: pass

def get_prices():
    prices = {"oro":0, "eurusd":0, "gbpusd":0}
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        prices["oro"] = float(r.get("price",0))
    except: pass
    try:
        f = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()
        rates = f.get("rates",{})
        if rates.get("EUR"): prices["eurusd"] = 1 / rates["EUR"]
        if rates.get("GBP"): prices["gbpusd"] = 1 / rates["GBP"]
    except: pass
    return prices

def monitor():
    while True:
        try:
            p = get_prices()
            now = time.time()
            if p["oro"] > 0 and p["oro"] <= ORO_BUY and (now - last_alerts["oro"] > 1800):
                send_tg(f"🔔 <b>ORO - ZONA COMPRA</b>\n💰 Precio: {p['oro']}\n🎯 Nivel: {ORO_BUY}")
                last_alerts["oro"] = now
            if p["eurusd"] > 0 and p["eurusd"] <= EURUSD_BUY and (now - last_alerts["eurusd"] > 1800):
                send_tg(f"💶 <b>EURUSD - COMPRA</b>\n💰 Precio: {p['eurusd']:.5f}\n🎯 Nivel: {EURUSD_BUY}")
                last_alerts["eurusd"] = now
            if p["gbpusd"] > 0 and p["gbpusd"] <= GBPUSD_BUY and (now - last_alerts["gbpusd"] > 1800):
                send_tg(f"💷 <b>GBPUSD - COMPRA</b>\n💰 Precio: {p['gbpusd']:.5f}\n🎯 Nivel: {GBPUSD_BUY}")
                last_alerts["gbpusd"] = now
        except: pass
        time.sleep(60)

@app.route('/')
def home():
    return "RAUDY VIP ORO + DIVISAS LIVE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 RAUDY VIP ORO + DIVISAS 🔥\n\nComandos:\n/oro - Precio Oro\n/divisas - EURUSD y GBPUSD\n/todo - Todo")

async def oro_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = get_prices()
    await update.message.reply_text(f"💰 ORO: ${p['oro']:.2f}\n🎯 Compra: {ORO_BUY}")

async def divisas_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = get_prices()
    await update.message.reply_text(f"💶 EURUSD: {p['eurusd']:.5f} (Compra: {EURUSD_BUY})\n💷 GBPUSD: {p['gbpusd']:.5f} (Compra: {GBPUSD_BUY})")

async def todo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = get_prices()
    await update.message.reply_text(f"🔥 MERCADO VIP 🔥\n\n💰 ORO: ${p['oro']:.2f}\n💶 EURUSD: {p['eurusd']:.5f}\n💷 GBPUSD: {p['gbpusd']:.5f}")

def run_bot():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("oro", oro_cmd))
    bot_app.add_handler(CommandHandler("divisas", divisas_cmd))
    bot_app.add_handler(CommandHandler("todo", todo_cmd))
    bot_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=monitor, daemon=True).start()
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
