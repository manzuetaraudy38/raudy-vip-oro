import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

COMPRA_EURO = 0.92
VENTA_EURO = 0.96

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 HOLA! SOY EL ROBOT DE RAUDY VIP GINEBRA 🇨🇭\n\n"
        "Yo cambio Euro y Franco solo.\n\n"
        "Escribeme asi:\n"
        "👉 100 CHF si tienes Francos y quieres Euros\n"
        "👉 100 EUR si tienes Euros y quieres Francos\n\n"
        "Ejemplo: Escribe 100 CHF"
    )

async def cambiar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.upper().replace(",", ".").strip()
    nombre = update.message.from_user.first_name

    if texto == "SI":
        monto = context.user_data.get('monto', 0)
        tipo = context.user_data.get('tipo', '')
        le_toca = context.user_data.get('le_toca', 0)
        ganancia = context.user_data.get('ganancia', 0)
        if monto == 0:
            await update.message.reply_text("Primero escribeme cuanto quieres cambiar. Ejemplo: 100 CHF")
            return
        await update.message.reply_text(
            f"✅ ¡LISTO {nombre}!\n\n"
            f"Raudy ya recibio tu pedido.\n"
            f"Cambio: {monto} ({tipo})\n"
            f"Te toca: {le_toca:.2f}\n\n"
            f"Raudy te va a escribir ahora para hacerte el TWINT.\n"
            f"Gracias por cambiar con RAUDY VIP 👑"
        )
        TU_ID = os.environ.get("TU_ID")
        if TU_ID:
            try:
                await context.bot.send_message(chat_id=int(TU_ID), text=f"🔔 NUEVO CAMBIO JEFE!\nCliente: {nombre}\nQuiere: {monto} {tipo}\nLe toca: {le_toca:.2f}\nTu ganas: {ganancia:.2f} CHF")
            except:
                pass
        return

    try:
        if "CHF" in texto:
            monto = float(texto.replace("CHF", "").replace("FRANCOS", "").strip())
            euros = monto / VENTA_EURO
            ganancia = monto - (euros * COMPRA_EURO)
            await update.message.reply_text(f"💱 CAMBIO FRANCO A EURO\n\nTu me das: {monto} CHF\nYo te doy: {euros:.2f} €\n\n¿Quieres hacerlo? Escribe SI\nTasa de hoy: 1€ = {VENTA_EURO} CHF")
            context.user_data['monto'] = monto
            context.user_data['tipo'] = 'CHF_A_EUR'
            context.user_data['le_toca'] = euros
            context.user_data['ganancia'] = ganancia
            return

        if "EUR" in texto or "€" in texto or "EURO" in texto:
            monto = float(texto.replace("EUR", "").replace("€", "").replace("EURO", "").replace("EUROS", "").strip())
            francos = monto * COMPRA_EURO
            ganancia = monto * (VENTA_EURO - COMPRA_EURO)
            await update.message.reply_text(f"💱 CAMBIO EURO A FRANCO\n\nTu me das: {monto} €\nYo te doy: {francos:.2f} CHF\n\n¿Quieres hacerlo? Escribe SI\nTasa de hoy: 1€ = {COMPRA_EURO} CHF")
            context.user_data['monto'] = monto
            context.user_data['tipo'] = 'EUR_A_CHF'
            context.user_data['le_toca'] = francos
            context.user_data['ganancia'] = ganancia
            return

        await update.message.reply_text("Escribeme asi: 100 CHF o 100 EUR")
    except:
        await update.message.reply_text("Escribeme asi: 100 CHF o 100 EUR  Ejemplo: 100 CHF")

def main():
    print("Robot prendido... Raudy VIP listo!")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cambiar))
    app.run_polling()

if __name__ == "__main__":
    main()
