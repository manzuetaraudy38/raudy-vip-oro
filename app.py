# ROBOT CAMBIA MONEDA - RAUDY VIP GINEBRA
# Este robot cambia Euro y Franco solo por Telegram
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# TUS TASAS - TU LAS CAMBIAS AQUI
COMPRA_EURO = 0.92  # Tu compras Euro a 0.92
VENTA_EURO = 0.96   # Tu vendes Euro a 0.96

# Tu numero de Telegram para que te avise
TU_ID = 123456789  # Aqui pones tu ID de Telegram

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 HOLA! SOY EL ROBOT DE RAUDY VIP GINEBRA 🇨🇭\n\n"
        "Yo cambio Euro y Franco solo.\n\n"
        "Escribeme asi:\n"
        "👉 *100 CHF* si tienes 100 Francos y quieres Euros\n"
        "👉 *100 EUR* si tienes 100 Euros y quieres Francos\n\n"
        "Ejemplo: Escribe *100 CHF* y te digo cuanto te doy."
    )

async def cambiar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.upper().replace(",", ".")
    nombre = update.message.from_user.first_name

    try:
        if "CHF" in texto:
            monto = float(texto.replace("CHF", "").strip())
            euros = monto / VENTA_EURO
            ganancia = monto - (euros * COMPRA_EURO)
            await update.message.reply_text(
                f"💱 CAMBIO FRANCO A EURO\n\n"
                f"Tu me das: {monto} CHF\n"
                f"Yo te doy: {euros:.2f} €\n\n"
                f"¿Quieres hacerlo? Escribe SI\n"
                f"Tasa de hoy: 1€ = {VENTA_EURO} CHF"
            )
            # Guardamos para cuando diga SI
            context.user_data['monto'] = monto
            context.user_data['tipo'] = 'CHF_A_EUR'
            context.user_data['le_toca'] = euros
            context.user_data['ganancia'] = ganancia

        elif "EUR" in texto or "€" in texto:
            monto = float(texto.replace("EUR", "").replace("€", "").strip())
            francos = monto * COMPRA_EURO
            ganancia = monto * (VENTA_EURO - COMPRA_EURO)
            await update.message.reply_text(
                f"💱 CAMBIO EURO A FRANCO\n\n"
                f"Tu me das: {monto} €\n"
                f"Yo te doy: {francos:.2f} CHF\n\n"
                f"¿Quieres hacerlo? Escribe SI\n"
                f"Tasa de hoy: 1€ = {COMPRA_EURO} CHF"
            )
            context.user_data['monto'] = monto
            context.user_data['tipo'] = 'EUR_A_CHF'
            context.user_data['le_toca'] = francos
            context.user_data['ganancia'] = ganancia

        elif texto.strip() == "SI":
            monto = context.user_data.get('monto', 0)
            tipo = context.user_data.get('tipo', '')
            le_toca = context.user_data.get('le_toca', 0)
            ganancia = context.user_data.get('ganancia', 0)
            await update.message.reply_text(
                f"✅ ¡LISTO {nombre}!\n\n"
                f"Raudy ya recibio tu pedido.\n"
                f"Cambio: {monto} ({tipo})\n"
                f"Te toca: {le_toca:.2f}\n\n"
                f"Raudy te va a escribir ahora para hacerte el TWINT.\n"
                f"Gracias por cambiar con RAUDY VIP 👑"
            )
            # Te avisa a ti
            try:
                await context.bot.send_message(chat_id=TU_ID, text=f"🔔 NUEVO CAMBIO JEFE!\nCliente: {nombre}\nQuiere: {monto} {tipo}\nLe toca: {le_toca:.2f}\nTu ganas: {ganancia:.2f} CHF")
            except:
                pass
        else:
            await update.message.reply_text("Escribeme asi: *100 CHF* o *100 EUR*")
    except:
        await update.message.reply_text("Escribeme asi: *100 CHF* o *100 EUR*  Ejemplo: 100 CHF")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cambiar))
    print("Robot prendido...")
    app.run_polling()

if __name__ == "__main__":
    main()
