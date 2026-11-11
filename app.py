import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TU_ID = os.environ.get("TU_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "HOLA! SOY LA TIENDA DE RAUDY VIP GINEBRA\n\n"
    texto = texto + "Vendo Jabon, Crema, Desodorante y Pasta.\n\n"
    texto = texto + "Escribeme asi:\n"
    texto = texto + "JABON 1\n"
    texto = texto + "CREMA 1\n"
    texto = texto + "DESO 1\n"
    texto = texto + "PASTA 1\n"
    texto = texto + "COMBO\n\n"
    texto = texto + "Precios: Jabon 5, Crema 8, Deso 7, Pasta 6, Combo 20"
    await update.message.reply_text(texto)

async def vender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.upper().strip()
    nombre = update.message.from_user.first_name
    pedido = ""
    total = 0

    if mensaje == "COMBO":
        await update.message.reply_text("COMBO RAUDY VIP: Jabon + Crema + Deso + Pasta = 20 CHF. Si lo quieres escribe COMBO SI")
        return

    if mensaje == "COMBO SI":
        await update.message.reply_text("LISTO! Tu COMBO de 20 CHF esta pedido. Raudy te escribe para el TWINT.")
        if TU_ID:
            try:
                await context.bot.send_message(chat_id=int(TU_ID), text="NUEVA VENTA: COMBO 20 CHF Cliente: " + nombre)
            except:
                pass
        return

    if "JABON" in mensaje:
        pedido = "JABON"
        total = 5
    elif "CREMA" in mensaje:
        pedido = "CREMA"
        total = 8
    elif "DESO" in mensaje:
        pedido = "DESODORANTE"
        total = 7
    elif "PASTA" in mensaje or "DIENTE" in mensaje:
        pedido = "PASTA"
        total = 6
    else:
        await update.message.reply_text("Escribeme: JABON 1, CREMA 1, DESO 1, PASTA 1, o COMBO")
        return

    cantidad = 1
    for parte in mensaje.split():
        if parte.isdigit():
            cantidad = int(parte)

    total_final = total * cantidad
    respuesta = "PEDIDO RAUDY VIP\nProducto: " + pedido + "\nCantidad: " + str(cantidad) + "\nTotal: " + str(total_final) + " CHF\n\nSi lo quieres escribe SI"
    await update.message.reply_text(respuesta)
    context.user_data["pedido"] = pedido
    context.user_data["total"] = total_final

    if mensaje == "SI":
        await update.message.reply_text("LISTO! Raudy te escribe ahora.")

async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.upper().strip()
    if mensaje == "SI":
        nombre = update.message.from_user.first_name
        pedido = context.user_data.get("pedido", "PEDIDO")
        total = context.user_data.get("total", 0)
        await update.message.reply_text("LISTO! Tu pedido esta hecho. Raudy te escribe para el TWINT. Gracias!")
        if TU_ID:
            try:
                await context.bot.send_message(chat_id=int(TU_ID), text="NUEVA VENTA Cliente: " + nombre + " Pedido: " + str(pedido) + " Total: " + str(total))
            except:
                pass
    else:
        await vender(update, context)

def main():
    print("Robot Tienda Raudy prendido!")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar))
    app.run_polling()

if __name__ == "__main__":
    main()
