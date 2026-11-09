# ROBOT 2 - REAL - SOLO $20 - JEFE RAUDY - CON FRENO
import os, time
from pybit.unified_trading import HTTP

API_KEY = os.environ.get("BYBIT_REAL_KEY", "")
API_SECRET = os.environ.get("BYBIT_REAL_SECRET", "")

# testnet=False = DINERO REAL - OJO JEFE
session = HTTP(testnet=False, api_key=API_KEY, api_secret=API_SECRET)

SYMBOL = "XAUUSDT"
CANTIDAD = 0.01  # NUNCA SUBIR ESTO SIN AVISARME
MAX_OPERACIONES_DIA = 1
operaciones_hoy = 0

def precio_oro():
    r = session.get_tickers(category="linear", symbol=SYMBOL)
    return float(r['result']['list'][0]['lastPrice'])

def ya_tengo_abierta():
    pos = session.get_positions(category="linear", symbol=SYMBOL)
    for p in pos['result']['list']:
        if float(p['size']) > 0:
            return True
    return False

def operar_real():
    global operaciones_hoy
    if operaciones_hoy >= MAX_OPERACIONES_DIA:
        print("Jefe, ya hice 1 hoy, me apago hasta mañana")
        return
    if ya_tengo_abierta():
        print("Jefe, ya tengo una abierta, ESPERA")
        return

    precio = precio_oro()
    print(f"Oro real ahora: {precio}")

    ZONA_COMPRA = 4100
    ZONA_VENTA = 4150

    if precio < ZONA_COMPRA:
        print(f"COMPRA REAL ${precio} - Con TP +$5 y SL -$5")
        session.place_order(
            category="linear", symbol=SYMBOL, side="Buy",
            orderType="Market", qty=CANTIDAD,
            takeProfit=precio+5, stopLoss=precio-5
        )
        operaciones_hoy += 1
        print("COMPRA REAL HECHA JEFE!")
    elif precio > ZONA_VENTA:
        print(f"VENTA REAL ${precio}")
        session.place_order(
            category="linear", symbol=SYMBOL, side="Sell",
            orderType="Market", qty=CANTIDAD,
            takeProfit=precio-5, stopLoss=precio+5
        )
        operaciones_hoy += 1
        print("VENTA REAL HECHA JEFE!")
    else:
        print(f"En medio {precio}, ESPERA, no compro")

while True:
    try:
        operar_real()
    except Exception as e:
        print(f"Error real: {e}")
    time.sleep(3600)
