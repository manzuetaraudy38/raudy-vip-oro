import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TU_ID = os.environ.get("TU_ID")

PRECIOS = {
    "JABON": 5.00,
    "CREMA": 8.00,
    "DESODORANTE": 7.00,
    "PASTA": 6.00,
}

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
            f"Gracias por comprar con RAUDY
