import os, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# TUS ALERTAS - PUEDES CAMBIAR LOS NUMEROS
ALERTAS = {
    "XAU/USD": {"precio": 3890, "tipo": "abajo", "avisado": False},
    "EUR/USD": {"precio": 1.08, "tipo": "abajo", "avisado": False},
    "GBP/USD": {"precio": 1.27, "tipo": "abajo", "avisado": False},
    "USD/JPY": {"precio": 155, "tipo": "arriba", "avisado": False},
}

chat_id = None

def get_precio(simbolo):
    try:
        if "XAU" in simbolo:
            r = requests.get("https://api.gold-api.com/price/XAU", timeout=10)
            return float(r.json()['price'])
        else:
            base = simbolo.split("/")[0]
            quote = simbolo.split("/")[1]
            r = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base}", timeout=10)
            return float(r.json()['rates'][quote])
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    chat_id = update.effective_chat.id
    for k in ALERTAS: ALERTAS[k]["avisado"] = False
    txt = "✅ RAUDY VIP - ORO Y DIVISAS ACTIVO\n\n"
    for d,c in ALERTAS.items(): txt+=f"• {d} -> {c['tipo']} de {c['precio']}\n"
    txt+="\n/precio para ver precios\n/divisas para ver alertas"
    await update.message.reply_text(txt)

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt="💰 PRECIOS AHORA:\n\n"
    for d in ALERTAS:
        p=get_precio(d)
        txt+=f"{d}: {p:.4f}\n" if p else f"{d}: error\n"
    await update.message.reply_text(txt)

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt="📊 ALERTAS:\n\n"
    for d,c in ALERTAS.items():
        e="✅ avisado" if c["avisado"] else "⏳ esperando"
        txt+=f"{d} {c['precio']} {e}\n"
    await update.message.reply_text(txt)

async def check(context: ContextTypes.DEFAULT_TYPE):
    if not chat_id: return
    for divisa, cfg in ALERTAS.items():
        if cfg["avisado"]: continue
        p=get_precio(divisa)
        if not p: continue
        go=False
        if cfg["tipo"]=="abajo" and p<=cfg["precio"]: go=True
        if cfg["tipo"]=="arriba" and p>=cfg["precio"]: go=True
        if go:
            await context.bot.send_message(chat_id=chat_id, text=f"🚨 RAUDY ALERTA!\n\nDivisa: {divisa}\nAhora: {p:.4f}\nAlerta: {cfg['precio']}\n\n👉 COMPRA/VENTA AHORA!")
            ALERTAS[divisa]["avisado"]=True

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("divisas", lista))
    app.add_handler(CommandHandler("oro", precio))
    app.job_queue.run_repeating(check, interval=60, first=10)
    app.run_polling()
