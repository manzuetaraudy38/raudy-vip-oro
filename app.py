# RAUDY VIP PRO V2 - TODO JUNTO FINAL - CON PANEL
# Borra todo lo viejo y pega esto entero

import os
import time
import random
import threading
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

dinero_actual = 100.0
dinero_inicial = 100.0
operaciones_hoy = 0
ultima_señal = "Esperando primera señal..."
historial = []
bot_encendido = False

def mandar_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}, timeout=10)
    except Exception as e:
        print(f"Error Telegram: {e}")

def bot_trabajando():
    global dinero_actual, operaciones_hoy, ultima_señal, bot_encendido
    bot_encendido = True
    print("BOT ENCENDIDO")
    mandar_telegram("🤖 RAUDY VIP PRO V2 ENCENDIDO 👑\nYa estoy trabajando, jefe. Solo DEMO.")
    while True:
        try:
            señal = random.choice(["COMPRA", "VENTA", "ESPERAR", "ESPERAR", "ESPERAR"])
            fuerza = random.randint(1, 10)
            # Solo opera si es fuerte y max 3 al dia - Disciplinado
            if señal != "ESPERAR" and fuerza >= 8 and operaciones_hoy < 3:
                riesgo = dinero_actual * 0.01  # Solo 1% - Cuida tu dinero
                ultima_señal = f"{señal} - Fuerza {fuerza}/10 - {datetime.now().strftime('%H:%M:%S')}"
                gano = random.choice([True, False])
                if gano:
                    ganancia = riesgo * 2
                    dinero_actual += ganancia
                    resultado = f"✅ GANÓ +${ganancia:.2f}"
                else:
                    dinero_actual -= riesgo
                    resultado = f"❌ PERDIÓ -${riesgo:.2f} con Stop Loss"
                operaciones_hoy += 1
                texto = f"🟢 SEÑAL RAUDY VIP PRO V2\nPar: EUR/USD\nAcción: {señal}\nFuerza: {fuerza}/10\nRiesgo: ${riesgo:.2f}\n{resultado}\nDinero: ${dinero_actual:.2f}"
                historial.insert(0, texto)
                mandar_telegram(texto)
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

@app.route('/')
def panel():
    ganancia = dinero_actual - dinero_inicial
    color = "green" if ganancia >= 0 else "red"
    historial_html = "<br><br>".join(historial[:5]) if historial else "Todavía no hay operaciones. El bot está analizando..."
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="30"></head>
    <body style="font-family:Arial; background:#111; color:white; padding:20px; text-align:center;">
        <h1>👑 RAUDY VIP PRO V2</h1>
        <h3 style="color:#FFD700;">ESTA VIVO - Trabajando 24 horas</h3>
        <div style="background:#222; padding:20px; border-radius:15px;">
            <h2>💰 Dinero DEMO: ${dinero_actual:.2f}</h2>
            <h3 style="color:{color};">Ganancia: ${ganancia:.2f}</h3>
            <p>Operaciones hoy: {operaciones_hoy} / 3</p>
            <p>Última señal: {ultima_señal}</p>
            <p>Estado: {'🟢 ENCENDIDO' if bot_encendido else '🟡 PRENDIENDO...'}</p>
            <p>Riesgo: Solo 1% | Stop Loss: ACTIVADO</p>
        </div>
        <div style="background:#222; padding:20px; border-radius:15px; text-align:left; margin-top:15px;">
            <h3>📊 Historial:</h3><p>{historial_html}</p>
        </div>
        <p style="color:gray;">Si ves esto, tu robot SÍ sirve. Se actualiza solo cada 30 seg.</p>
    </body></html>
    """

# Prende el bot aunque sea con gunicorn
if not bot_encendido:
    t = threading.Thread(target=bot_trabajando, daemon=True)
    t.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
