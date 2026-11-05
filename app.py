from flask import Flask, session, request, redirect, jsonify
import requests
import threading
import time
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cambia-esto-en-render-por-una-larga")

CLAVE_BUENA = os.getenv("VIP_CLAVE", "RAUDY26")
FECHA_VENCE = datetime(2026, 12, 3, 23, 59, 59)
BOT_TOKEN = os.getenv("BOT_TOKEN", "AQUI_PON_TU_TOKEN_DEL_BOTFATHER")
CHAT_ID_VIP = os.getenv("CHAT_ID", "AQUI_PON_TU_ID_O_DEL_CANAL")
BOT_USERNAME = os.getenv("BOT_USERNAME", "raudy_vip_oro_bot")
COMPRAS = [3900, 3890, 3865]
VENTAS = [3980, 3990, 4020]
alertado_compra = {p: False for p in COMPRAS}
alertado_venta = {p: False for p in VENTAS}
ultimo_update_id = 0
historial_oro = []
historial_senales = []

# ===== RAUDY - 40 ROBOTS - CADA UNO HACE SU TRABAJO - NUEVO =====
ROBOTS_RAUDY = []
NOMBRES_40 = ["Cazador Rapido","Relampago Oro","Flecha Veloz","Ojo Aguila","Tiburon Oro","Ninja Precio","Rayo Londres","Trueno NY","Guardian Scalping","Maestro Scalping","Rey Londres","Reina Londres","Guardian Londres","Cazador Londres","Jefe Londres","Rey NY","Reina NY","Guardian NY","Cazador NY","Jefe NY","Ojo Noticias","Alarma Noticias","Guardian Noticias","Cazador Noticias","Jefe Noticias","Soporte 3900","Soporte 3890","Soporte 3865","Resistencia 3980","Resistencia 4020","Robot DIOS 1","Robot DIOS 2","Robot DIOS 3","Robot DIOS 4","Robot DIOS 5","Guardian Capital","Guardian Cuenta","Guardian Familia","Guardian Anti-Perdida","MAESTRO SUPREMO"]
for i, nom in enumerate(NOMBRES_40, 1):
    ROBOTS_RAUDY.append({"id": i, "nombre": nom, "trabajo": "Trabaja con el equipo", "estrellas": 0, "puntos": 0, "mensaje": "Listo para trabajar"})

def chat_robots(precio, maestro):
    if precio <= 3910:
        return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro bajo, yo digo COMPRA"}, {"robot": "Robot 18 Guardian NY", "texto": "Confirmo, yo tambien COMPRA"}, {"robot": "Robot 40 MAESTRO", "texto": "Decido: " + maestro["señal"]}]
    if precio >= 3970:
        return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro subio, yo digo VENTA"}, {"robot": "Robot 16 Rey NY", "texto": "Confirmo, yo tambien VENTA"}, {"robot": "Robot 40 MAESTRO", "texto": "Decido: " + maestro["señal"]}]
    return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro en medio, yo digo ESPERA"}, {"robot": "Robot 40 MAESTRO", "texto": "Decido: " + maestro["señal"]}]

# === ARREGLO HORA GINEBRA RAUDY - Render esta en UTC, Ginebra es UTC+1 ===
def hora_ginebra():
    return datetime.utcnow() + timedelta(hours=1)

def dias_restantes():
    delta = FECHA_VENCE - hora_ginebra()
    return max(0, delta.days)

def codigo_vigente():
    return hora_ginebra() <= FECHA_VENCE

# === FILTRO DE NOTICIAS RAUDY ===
def filtro_noticias(precio):
    ahora = hora_ginebra()
    hora = ahora.hour
    minuto = ahora.minute
    if hora == 14 and 25 <= minuto <= 59:
        return {"texto": "🔴 NO OPERES - NOTICIAS USA 14:30 - ESPERA 30 MIN", "color": "#ff0000", "puede": False}
    if hora == 8 and 25 <= minuto <= 45:
        return {"texto": "🔴 NO OPERES - NOTICIAS 08:30 - ESPERA", "color": "#ff0000", "puede": False}
    if hora == 10 and 0 <= minuto <= 15:
        return {"texto": "🟡 CUIDADO - NOTICIAS EUROPA 10:00", "color": "#FFA500", "puede": True}
    if len(historial_oro) >= 5:
        cambio = abs(precio - historial_oro[-5])
        if cambio > 25:
            return {"texto": f"🟡 CUIDADO - MERCADO LOCO SE MOVIO ${cambio:.2f} RAPIDO - ESPERA QUE SE CALME", "color": "#FFA500", "puede": True}
    return {"texto": "🟢 FILTRO OK - PUEDES OPERAR - SIN NOTICIAS FUERTES", "color": "#00aa00", "puede": True}

# === RELOJ MUNDIAL RAUDY ===
def reloj_mundial():
    ahora_ginebra = hora_ginebra()
    hora_londres = ahora_ginebra - timedelta(hours=1)
    hora_ny = ahora_ginebra - timedelta(hours=6)
    hora_tokio = ahora_ginebra + timedelta(hours=8)
    dia_semana = ahora_ginebra.weekday()
    nombres_dia = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
    dia_nombre = nombres_dia[dia_semana]
    hora_g = ahora_ginebra.hour
    minuto = ahora_ginebra.minute
    if dia_semana >= 5:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🔴 HOY ES {dia_nombre} - MERCADO CERRADO - NO SE COMPRA ORO - DESCANSA", "color": "#ff0000", "sesion": "MERCADO CERRADO", "puede": False}
    if 9 <= hora_g < 11:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🟢 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - SESION LONDRES - BUENA HORA PARA COMPRAR ORO", "color": "#00aa00", "sesion": "LONDRES 🟢", "puede": True}
    if (hora_g == 14 and minuto >= 30) or (15 <= hora_g < 17):
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🟢🟢 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - SESION NEW YORK - LA MEJOR HORA PARA COMPRAR / VENDER ORO", "color": "#00aa00", "sesion": "NEW YORK 🟢🟢 MEJOR HORA", "puede": True}
    if 2 <= hora_g < 6:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🔴 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - SESION ASIA - MERCADO DORMIDO - NO COMPRES ORO AHORA", "color": "#ff0000", "sesion": "ASIA 🔴 DORMIDO", "puede": False}
    if hora_g >= 22 or hora_g < 2:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🔴 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - MERCADO DE NOCHE - NO HAY GENTE - NO COMPRES", "color": "#ff0000", "sesion": "NOCHE 🔴", "puede": False}
    return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🟡 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - ENTRE SESIONES - ESPERA A LAS 09:00 O 14:30 PARA COMPRAR", "color": "#FFA500", "sesion": "ENTRE SESIONES 🟡", "puede": True}

def get_price_yahoo(symbol, fallback):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        j = r.json()
        price = j['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except:
        return fallback

def get_oro_precio():
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=4)
        return float(r.json().get('price', 3922))
    except:
        return get_price_yahoo('GC=F', 3922)

def analizar_ia_oro(precio):
    historial_oro.append(precio)
    if len(historial_oro) > 50:
        historial_oro.pop(0)
    if len(historial_oro) >= 10:
        max_reciente = max(historial_oro[-20:])
        min_reciente = min(historial_oro[-20:])
    else:
        max_reciente = precio + 20
        min_reciente = precio - 20
    if precio <= 3905 and precio >= 3860:
        res = {"señal": "🟢 COMPRA SWING", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA SWING", "analisis": f"IA SWING: Oro hizo SWING BAJO en {min_reciente:.2f} en zona 3900-3865. Bajó y ahora rebota para subir. Es zona de COMPRA.", "entrada": precio, "tp": round(precio + 35, 2), "sl": round(precio - 18, 2), "confianza": "88%"}
    elif precio >= 3980 and precio <= 4030:
        res = {"señal": "🔴 VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA SWING", "analisis": f"IA SWING: Oro hizo SWING ALTO en {max_reciente:.2f} en zona 3980-4020. Subió mucho y ahora va a bajar. Es zona de VENTA.", "entrada": precio, "tp": round(precio - 35, 2), "sl": round(precio + 18, 2), "confianza": "88%"}
    elif precio > 4030:
        res = {"señal": "🔴 YA PASO ZONA VENTA - ESPERA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - YA PASO VENTA", "analisis": f"IA SWING: Oro alto en ${precio:.2f}. YA PASO la zona de venta 3980-4020. NO persigas la venta aquí. Espera que baje a 3980 para venta o a 3900 para compra. Swing Alto {max_reciente:.2f} / Bajo {min_reciente:.2f}", "entrada": precio, "tp": 3980, "sl": round(precio + 20, 2), "confianza": "65%"}
    elif precio > 3940:
        res = {"señal": "🔴 ESPERANDO VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - ESPERANDO VENTA", "analisis": f"IA SWING: Oro en ${precio:.2f}. No compres aquí. Swing Alto {max_reciente:.2f} / Bajo {min_reciente:.2f}. Espera que suba a 3980 para venta o baje a 3900 para compra.", "entrada": precio, "tp": 3900, "sl": 4040, "confianza": "65%"}
    elif precio < 3940 and precio > 3905:
        res = {"señal": "🟡 CERCA DE COMPRA SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 LUZ NARANJA - CERCA DE COMPRA", "analisis": f"IA SWING: Oro en ${precio:.2f} se acerca a compra. Si toca 3900 es SWING BAJO = COMPRA. Bajo reciente {min_reciente:.2f}", "entrada": 3900, "tp": 3935, "sl": 3882, "confianza": "70%"}
    else:
        res = {"señal": "🟡 ANALIZANDO SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 ANALIZANDO", "analisis": f"IA: Analizando swing... Precio ${precio:.2f}. Alto {max_reciente:.2f} Bajo {min_reciente:.2f}. Espera señal clara.", "entrada": precio, "tp": round(precio + 30, 2), "sl": round(precio - 15, 2), "confianza": "50%"}
    res["botin"] = res["tp"]
    res
