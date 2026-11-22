import requests
import time

# === PON AQUI TUS DATOS REALES, JEFE ===
TOKEN = "PON_AQUI_TU_TOKEN_DE_BOTFATHER"
CHAT_ID = "PON_AQUI_TU_ID_DE_USERINFOBOT"
# =========================================

# Precio que quieres que te avise - si el oro sube de esto, te avisa
PRECIO_AVISO_USD_POR_ONZA = 2600

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    datos = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        r = requests.post(url, data=datos, timeout=10)
        print("Telegram:", r.status_code)
    except Exception as e:
        print("Error Telegram:", e)

def precio_oro():
    try:
        # API gratis, sin clave
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD", timeout=10)
        data = r.json()
        # Precio por onza en USD
        precio_onza = data["items"][0]["curr"]
        return precio_onza
    except Exception as e:
        print("Error precio:", e)
        return None

print("RAUDY ORO BOT ENCENDIDO - esperando precio...")
enviar_telegram("✅ Raudy Oro Bot encendido jefe. Te aviso cuando el oro suba.")

while True:
    precio = precio_oro()
    if precio:
        # Convertir onza a gramo
        precio_gramo_usd = precio / 31.1035
        # 18K es 75% oro puro
        precio_18k_gramo = precio_gramo_usd * 0.75

        print(f"Oro: {precio} USD/onza | 18K por gramo: {precio_18k_gramo:.2f} USD")

        if precio >= PRECIO_AVISO_USD_POR_ONZA:
            enviar_telegram(f"🔥 JEFE EL ORO SUBIÓ!\nOnza: {precio} USD\n18K por gramo: {precio_18k_gramo:.2f} USD\n¡Es momento de vender!")
            # Espera 1 hora para no spamearte
            time.sleep(3600)
    
    # Revisa cada 5 minutos
    time.sleep(300)
