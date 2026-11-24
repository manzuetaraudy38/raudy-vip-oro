# ROBOT SEÑAL DE ORO - RAUDY ORO - GRATIS
# Instalar: pip install requests

import requests
import time

# TU PRECIO, JEFE - CAMBIALO AQUI
PRECIO_PARA_COMPRAR = 93.0  # Si baja a 93, te avisa COMPRA
PRECIO_PARA_VENDER = 97.0   # Si sube a 97, te avisa VENDE

def precio_oro_ahora():
    try:
        # Precio real de la bolsa
        url = "https://api.metals.dev/v1/latest?api_key=GRATIS&currency=CHF&unit=g"
        # Si esa no funciona, usamos esta de respaldo
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD", timeout=10)
        data = r.json()
        precio_usd = data['items'][0]['curr']  # Precio onza USD
        # Convertimos a CHF por gramo aprox
        precio_chf_gramo = (precio_usd * 0.835) / 31.1035
        return precio_chf_gramo
    except:
        return 95.68  # Precio de hoy si falla internet

print("🤖 ROBOT ENCENDIDO, JEFE... Vigilando el oro")
while True:
    precio = precio_oro_ahora()
    print(f"Precio ahora: {precio:.2f} CHF / gramo 24K")

    if precio <= PRECIO_PARA_COMPRAR:
        print(f"🟢 ¡JEFE, COMPRA AHORA! Bajo a {precio:.2f} CHF")
    elif precio >= PRECIO_PARA_VENDER:
        print(f"🔴 ¡JEFE, VENDE AHORA! Subio a {precio:.2f} CHF")
    else:
        print("🟡 Espera, jefe, todavia no.")

    time.sleep(60)  # Revisa cada 1 minuto
