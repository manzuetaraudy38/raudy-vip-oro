# ============================================
# RAUDY VIP PRO V2 - TODO JUNTO FINAL
# 8 CUALIDADES + ARREGLO RENDER + TELEGRAM
# SOLO DEMO - DINERO FALSO
# ============================================

import os
import time
import random
import requests
import threading
from flask import Flask

# ============================================
# 1. ARREGLO PARA RENDER - MINI PAGINA WEB
# ============================================
app = Flask(__name__)

@app.route('/')
def home():
    return "RAUDY VIP PRO V2 ESTA VIVO 👑 - Trabajando 24 horas"

# ============================================
# 2. CONFIGURACIÓN - CUIDA TU DINERO
# ============================================
# En Render > Environment pon:
# TELEGRAM_TOKEN = tu token de BotFather
# TELEGRAM_CHAT_ID = tu ID de Telegram

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "PON_AQUI_TU_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "PON_AQUI_TU_CHAT_ID")

DINERO_INICIAL = 100.0
RIESGO_POR_OPERACION = 0.01  # CUALIDAD #2: Solo 1% - Si tienes $100, arriesga $1
MAX_OPERACIONES_POR_DIA = 3  # CUALIDAD #8: No opera a lo loco
STOP_LOSS_PORCIENTO = 0.02  # CUALIDAD #7: Freno de emergencia

dinero_actual = DINERO_INICIAL
operaciones_hoy = 0

# ============================================
# 3. MANDAR MENSAJE A TELEGRAM
# ============================================
def mandar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
        requests.post(url, data=data, timeout=10)
        print("Mensaje mandado a Telegram ✅")
    except Exception as e:
        print(f"No se pudo mandar a Telegram: {e}")

# ============================================
# 4. CEREBRO FRÍO - SIN MIEDO NI CODICIA
# ============================================
def analizar_mercado():
    # CUALIDAD #1 y #3: Frío y Disciplinado
    # Solo entra si la señal es MUY clara
    señal = random.choice(["COMPRA", "VENTA", "ESPERAR", "ESPERAR", "ESPERAR"])
    fuerza = random.randint(1, 10)

    # REGLA DE DISCIPLINA: Solo opera si fuerza es 8 o más
    if señal == "ESPERAR":
        return None, 0
    if fuerza < 8:
        print(f"Señal débil ({fuerza}/10). Mejor NO operar.")
        return None, 0

    return señal, fuerza

# ============================================
# 5. GESTIÓN DE RIESGO
# ============================================
def calcular_riesgo():
    # CUALIDAD #2: Nunca arriesga todo
    return dinero_actual * RIESGO_POR_OPERACION

# ============================================
# 6. EJECUTAR OPERACIÓN CON FRENO
# ============================================
def ejecutar_operacion(señal, fuerza):
    global dinero_actual, operaciones_hoy

    # CUALIDAD #8: Max 3 por día
    if operaciones_hoy >= MAX_OPERACIONES_POR_DIA:
        print("Ya hicimos 3 hoy. Paramos.")
        return

    riesgo = calcular_riesgo()

    mensaje = f"""
🟢 SEÑAL RAUDY VIP PRO V2
Par: EUR/USD
Acción: {señal}
Fuerza: {fuerza}/10
Riesgo: Solo ${riesgo:.2f}
Stop Loss: Puesto - Freno ACTIVADO
Dinero actual: ${dinero_actual:.2f}
"""
    print(mensaje)
    mandar_telegram(mensaje)

    # Simulamos resultado DEMO
    gano = random.choice([True, False])
    if gano:
        ganancia = riesgo * 2
        dinero_actual += ganancia
        resultado = f"✅ GANÓ +${ganancia:.2f} | Dinero ahora: ${dinero_actual:.2f}"
    else:
        dinero_actual -= riesgo
        resultado = f"❌ PERDIÓ -${riesgo:.2f} por Stop Loss | Dinero ahora: ${dinero_actual:.2f}\nTranquilo, perdimos poquito porque teníamos freno."

    print(resultado)
    mandar_telegram(resultado)
    operaciones_hoy += 1

# ============================================
# 7. TRABAJA 24 HORAS SIN CANSARSE
# ============================================
def bot_trabajando():
    # CUALIDAD #5: Trabaja 24 horas
    print(f"🤖 RAUDY VIP PRO V2 ENCENDIDO")
    print(f"Dinero DEMO: ${DINERO_INICIAL}")
    mandar_telegram("🤖 RAUDY VIP PRO V2 ENCENDIDO 👑\nYa estoy trabajando para ti, jefe. Solo DEMO.")

    while True:
        señal, fuerza = analizar_mercado()
        if señal:
            ejecutar_operacion(señal, fuerza)
        else:
            print("Sin oportunidad clara... esperando 1 minuto.")
        # CUALIDAD #4: Rápido, revisa cada 60 segundos
        time.sleep(60)

# ============================================
# 8. PRENDER TODO JUNTO - ARREGLO FINAL
# Esto hace que el bot prenda aunque sea con GUNICORN
# ============================================
# Ya no está dentro del if __main__, ahora prende siempre
hilo_bot = threading.Thread(target=bot_trabajando, daemon=True)
hilo_bot.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
