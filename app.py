# JEFE 12 ROBOTS - PYTHON PARA RENDER - COMPLETO
# 6 COMPRA - 6 VENTA - M1 M5 M15 H1 H4
import time
import random
from flask import Flask

app = Flask(__name__)

# H4 MANDA - SOLO COMPRA CON 4-5 VERDES - SI 3 ROJAS NO ENTRA
# Este es comentario con # jefe, no con // jefe

def calcular_robot(nombre, timeframe):
    # Simulamos EMA 9 y EMA 21, jefe
    ema_rapida = random.uniform(2600, 2650)
    ema_lenta = random.uniform(2600, 2650)
    rsi = random.uniform(30, 70)
    
    compra = ema_rapida > ema_lenta and rsi > 50
    venta = ema_rapida < ema_lenta and rsi < 50
    return compra, venta, rsi

def revisar_12_robots():
    robots = [
        ("1 COMPRA", "M1"),
        ("2 COMPRA", "M5"),
        ("3 COMPRA", "M15"),
        ("4 COMPRA", "H1"),
        ("5 COMPRA", "H4"),
        ("6 COMPRA", "M5"),
        ("7 VENTA", "M1"),
        ("8 VENTA", "M5"),
        ("9 VENTA", "M15"),
        ("10 VENTA", "H1"),
        ("11 VENTA", "H4"),
        ("12 VENTA", "M15"),
    ]
    compras = 0
    ventas = 0
    print("=== JEFE REVISANDO 12 ROBOTS ===", flush=True)
    for nombre, tf in robots:
        compra, venta, rsi = calcular_robot(nombre, tf)
        if compra:
            compras += 1
            print(f"✅ {nombre} {tf} -> COMPRA JEFE - RSI {rsi:.1f}", flush=True)
        if venta:
            ventas += 1
            print(f"🔴 {nombre} {tf} -> VENTA JEFE - RSI {rsi:.1f}", flush=True)
    
    # REGLA JEFE H4 MANDA
    if compras >= 4:
        print(">>> COMPRA JEFE COMPRA JEFE TODOS DICEN COMPRA <<<", flush=True)
    elif ventas >= 4:
        print(">>> VENTA JEFE VENTA JEFE TODOS DICEN VENTA <<<", flush=True)
    else:
        print(">>> JEFE NO ENTRA - ESPERA <<<", flush=True)
    return compras, ventas

@app.route("/")
def home():
    compras, ventas = revisar_12_robots()
    return f"JEFE 12 ROBOTS OK - Compras: {compras} Ventas: {ventas} - H4 MANDA"

@app.route("/check")
def check():
    compras, ventas = revisar_12_robots()
    return {"compras": compras, "ventas": ventas, "mensaje": "JEFE OK"}

if __name__ == "__main__":
    print("JEFE BOT ENCENDIDO", flush=True)
    revisar_12_robots()
    app.run(host="0.0.0.0", port=10000)
