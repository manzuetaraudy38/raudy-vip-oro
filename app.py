# RAUDY VIP PRO V2 - ROBOT PROFESIONAL
# Hecho para JEFE RAUDY - SOLO DEMO, DINERO FALSO

import time
import random

# ===============================
# 1. CONFIGURACIÓN - CUIDA TU DINERO
# ===============================
DINERO_INICIAL = 100  # Dinero falso para practicar
RIESGO_POR_OPERACION = 0.01  # Solo 1% por operación - CUALIDAD #2
MAX_OPERACIONES_POR_DIA = 3  # No opera a lo loco - CUALIDAD #8
STOP_LOSS_PORCIENTO = 0.02  # Freno de emergencia - CUALIDAD #7

dinero_actual = DINERO_INICIAL
operaciones_hoy = 0

# ===============================
# 2. CEREBRO FRÍO - SIN MIEDO NI CODICIA
# ===============================
def analizar_mercado():
    """
    CUALIDAD #1 y #3: Frío y Disciplinado
    Solo entra si la señal es MUY clara.
    Si no es clara, NO opera.
    """
    # Simulamos el mercado - en la vida real aquí va el precio real
    señal = random.choice(["COMPRA", "VENTA", "ESPERAR", "ESPERAR", "ESPERAR"])
    fuerza = random.randint(1, 10)  # 1 al 10 que tan fuerte es la señal
    
    # REGLA DE DISCIPLINA: Solo opera si fuerza es 8 o más
    if señal == "ESPERAR":
        return None, 0
    if fuerza < 8:
        print(f"Señal débil ({fuerza}/10). Mejor NO operar. Esperando...")
        return None, 0
    
    return señal, fuerza

# ===============================
# 3. GESTIÓN DE RIESGO
# ===============================
def calcular_riesgo():
    """CUALIDAD #2: Nunca arriesga todo"""
    riesgo_dolares = dinero_actual * RIESGO_POR_OPERACION
    return riesgo_dolares

# ===============================
# 4. EJECUTAR OPERACIÓN CON FRENO
# ===============================
def ejecutar_operacion(señal, fuerza):
    global dinero_actual, operaciones_hoy
    
    # CUALIDAD #8: No opera a lo loco
    if operaciones_hoy >= MAX_OPERACIONES_POR_DIA:
        print("Ya hicimos 3 operaciones hoy. Paramos. A dormir.")
        return
    
    riesgo = calcular_riesgo()
    stop_loss = riesgo  # Si pierde, solo pierde el riesgo
    
    print(f"\n🟢 SEÑAL RAUDY VIP PRO V2")
    print(f"Par: EUR/USD")
    print(f"Acción: {señal}")
    print(f"Fuerza: {fuerza}/10")
    print(f"Riesgo: Solo ${riesgo:.2f}")
    print(f"Stop Loss: Puesto - Freno de emergencia ACTIVADO")
    
    # Simulamos resultado
    gano = random.choice([True, False])
    
    if gano:
        ganancia = riesgo * 2  # Gana el doble de lo que arriesgó
        dinero_actual += ganancia
        print(f"✅ GANÓ +${ganancia:.2f} | Dinero ahora: ${dinero_actual:.2f}")
    else:
        dinero_actual -= stop_loss
        print(f"❌ PERDIÓ -${stop_loss:.2f} por Stop Loss | Dinero ahora: ${dinero_actual:.2f}")
        print("Tranquilo, perdimos poquito porque teníamos freno.")
    
    operaciones_hoy += 1

# ===============================
# 5. TRABAJA 24 HORAS SIN CANSARSE
# ===============================
def bot_trabajando():
    """CUALIDAD #5: Trabaja 24 horas"""
    print(f"🤖 RAUDY VIP PRO V2 ENCENDIDO")
    print(f"Dinero inicial DEMO: ${DINERO_INICIAL}")
    print("Revisando mercado cada 1 minuto...")
    print("Si no hay oportunidad buena, NO opera.")
    
    while True:
        señal, fuerza = analizar_mercado()
        
        if señal:
            ejecutar_operacion(señal, fuerza)
        else:
            print("Sin oportunidad clara... esperando 1 minuto.")
        
        # CUALIDAD #4: Rápido, revisa cada 60 segundos
        time.sleep(60)
        
        # Para la prueba, para después de 5 revisiones
        # En real lo dejas corriendo 24 horas
        # break

# ===============================
# ENCENDER EL BOT
# ===============================
if __name__ == "__main__":
    bot_trabajando()
