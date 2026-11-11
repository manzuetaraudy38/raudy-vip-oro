import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TU_ID = os.environ.get("TU_ID")

# PRECIOS DE VENTA EN GINEBRA
PRECIOS = {
    "JABON": 5.00,
    "CREMA": 8.00,
    "DESODORANTE": 7.00,
    "PASTA": 6.00,
}

# STOCK QUE TIENES - TU LO CAMBIAS AQUI
STOCK = {
    "JABON": 20,
    "CREMA": 15,
    "DESODORANTE": 18,
    "PASTA": 20,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 HOLA! SOY LA TIENDA DE RAUDY VIP GINEBRA 🇨🇭\n\n"
        "Vendo Jabon, Crema, Desodorante y Pasta de Diente.\n\n"
        "Escribeme asi:\n"
        "👉 JABON 2 - para pedir 2 jabones\n"
        "👉 CREMA 1 - para pedir 1 crema\n"
        "👉 DESODORANTE 1\n"
        "👉 PASTA 2\n\n"
        "Precios:\n"
        "🧼 Jabon: 5 CHF\n"
        "🧴 Crema: 8 CHF\n"
        "🧴 Desodorante: 7 CHF\n"
        "🪥 Pasta: 6 CHF\n\n"
        "Escribe COMBO para ver el combo barato!"
    )

async def vender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.upper().strip()
    nombre = update.message.from_user.first_name

    if texto == "COMBO":
        await update.message.reply_text(
            "👑 COMBO RAUDY VIP - TODO JUNTO!\n\n"
            "🧼 1 Jabon + 🧴 1 Crema + 🧴 1 Desodorante + 🪥 1 Pasta\n"
            "Precio normal: 26 CHF\n"
            "Precio COMBO: 20 CHF\n"
            "Te ahorras 6 CHF!\n\n"
            "¿Lo quieres? Escribe COMBO SI"
        )
        return

    if texto == "COMBO SI":
        await update.message.reply_text(
            f"✅ ¡LISTO {nombre}!\n\n"
            f"Tu COMBO de 20 CHF esta pedido.\n"
            f"Raudy te va a escribir para el TWINT y la entrega en Ginebra.\n"
            f"Gracias por comprar con RAUDY VIP 👑"
        )
        if TU_ID:
            try:
                await context.bot.send_message(chat_id=int(TU_ID), text=f"🔔 NUEVA VENTA JEFE!\nCliente: {nombre}\nQuiere: COMBO COMPLETO 20 CHF\n¡Preparalo!")
            except:
                pass
        return

    if texto == "SI":
        await update.message.reply_text("Ya tu pedido esta hecho, jefe. Raudy te va a escribir ahora. Gracias!")
        return

    # SI ESCRIBE EJEMPLO: JABON 2
    try:
        for producto, precio in PRECIOS.items():
            if producto in texto or (producto == "DESODORANTE" and "DESO" in texto) or (producto == "PASTA" and "DIENTE" in texto):
                partes = texto.split()
                cantidad = 1
                for p in partes:
                    if p.isdigit():
                        cantidad = int(p)
                total = precio * cantidad
                stock_actual = STOCK.get(producto, 0)
                if cantidad > stock_actual:
                    await update.message.reply_text(f"Jefe, solo me quedan {stock_actual} de {producto}. Pide menos.")
                    return
                await update.message.reply_text(
                    f"👑 PEDIDO RAUDY VIP\n\n"
                    f"Producto: {producto}\n"
                    f"Cantidad: {cantidad}\n"
                    f"Precio: {precio} CHF cada uno\n"
                    f"Total a pagar: {total} CHF\n\n"
                    f"¿Lo quieres? Escribe SI"
                )
                context.user_data['pedido'] = f"{cantidad} x {producto} = {total} CHF"
                context.user_data['producto'] = producto
                context.user_data['cantidad'] = cantidad
                return
        await update.message.reply_text("Escribeme: JABON 1, CREMA 1, DESO 1, PASTA 1, o COMBO")
    except:
        await update.message.reply_text("Escribeme: JABON 1, CREMA 1, DESO 1, PASTA 1, o COMBO")

def main():
    print("Robot Tienda Raudy prendido!")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, vender))
    app.run_polling()

if __name__ == "__main__":
    main()
