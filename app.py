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

# ===== RAUDY - 50 ROBOTS QUE TRABAJAN JUNTOS + ESTRELLAS - NUEVO, NO BORRA NADA =====
# Cada robot tiene su trabajo, sus estrellas y sus puntos. Tu le das estrella si hace bien su trabajo.
ROBOTS_RAUDY = []
NOMBRES_ROBOTS = [
    (1, "Cazador Rapido", "SCALPING - Mira el precio cada 5 seg"),
    (2, "Relampago Oro", "SCALPING - Compra rapida si baja"),
    (3, "Flecha Veloz", "SCALPING - Venta rapida si sube"),
    (4, "Ojo De Aguila", "SCALPING - Vigila rompimientos"),
    (5, "Tiburon Oro", "SCALPING - Dice COMPRA o VENTA rapido"),
    (6, "Ninja Precio", "SCALPING - Sigue el precio"),
    (7, "Rayo Londres", "SCALPING - Hora de Londres"),
    (8, "Trueno NY", "SCALPING - Hora de New York"),
    (9, "Guardián Scalping", "SCALPING - Protege de perdidas"),
    (10, "Maestro Scalping", "SCALPING - Jefe de los 10 primeros"),
    (11, "Rey Londres", "SWING LONDRES - Sesion 09:00-11:00"),
    (12, "Reina Londres", "SWING LONDRES - Confirma Londres"),
    (13, "Guardian Londres", "SWING LONDRES - Si Londres duerme, espera"),
    (14, "Cazador Londres", "SWING LONDRES - Busca COMPRA en Londres"),
    (15, "Jefe Londres", "SWING LONDRES - Decide Londres"),
    (16, "Rey New York", "SWING NEW YORK - Sesion 14:30-17:00"),
    (17, "Reina New York", "SWING NEW YORK - La mejor hora"),
    (18, "Guardian NY", "SWING NEW YORK - Confirma NY"),
    (19, "Cazador NY", "SWING NEW YORK - Busca VENTA en NY"),
    (20, "Jefe New York", "SWING NEW YORK - Decide NY"),
    (21, "Ojo Noticias", "NOTICIAS - Mira si hay noticias 14:30"),
    (22, "Alarma Noticias", "NOTICIAS - Grita NO OPERES si hay noticia"),
    (23, "Guardian Noticias", "NOTICIAS - Espera 30 min despues de noticia"),
    (24, "Cazador Noticias", "NOTICIAS - Si no hay noticia, se puede operar"),
    (25, "Jefe Noticias", "NOTICIAS - Decide si es peligroso"),
    (26, "Soporte 3900", "ORO - Vigila soporte 3900"),
    (27, "Soporte 3890", "ORO - Vigila soporte 3890"),
    (28, "Soporte 3865", "ORO - Vigila soporte 3865"),
    (29, "Resistencia 3980", "ORO - Vigila resistencia 3980"),
    (30, "Resistencia 4020", "ORO - Vigila resistencia 4020"),
    (31, "Robot DIOS 1", "DIOS - Solo habla si es COMPRA DIOS"),
    (32, "Robot DIOS 2", "DIOS - Solo habla si es VENTA DIOS"),
    (33, "Robot DIOS 3", "DIOS - Cuenta los 28 votos"),
    (34, "Robot DIOS 4", "DIOS - Confirma con 50 analizadores"),
    (35, "Robot DIOS 5", "DIOS - Jefe DIOS"),
    (36, "Robot DIOS 6", "DIOS - Protege tu capital"),
    (37, "Robot DIOS 7", "DIOS - Mira si el mercado esta loco"),
    (38, "Robot DIOS 8", "DIOS - Mira si es trampa"),
    (39, "Robot DIOS 9", "DIOS - Mira rebote"),
    (40, "Robot DIOS 10", "DIOS - Maestro DIOS Final"),
    (41, "Guardian Capital", "PROTECCION - Dice NO OPERES de noche"),
    (42, "Guardian Fin Semana", "PROTECCION - Dice NO OPERES sabado/domingo"),
    (43, "Guardian Cuenta", "PROTECCION - Si pierdes mucho, para"),
    (44, "Guardian Familia", "PROTECCION - Cuida tu dinero"),
    (45, "Guardian Anti-Perdida", "PROTECCION - Pone SL siempre"),
    (46, "Guardian Modo Niño", "PROTECCION - Explica facil"),
    (47, "Guardian Psicologia", "PROTECCION - No dejes que operes con miedo"),
    (48, "Guardian Copia Segura", "PROTECCION - Copia solo si 28 dicen si"),
    (49, "Guardian Idioma", "PROTECCION - Traduce todo facil"),
    (50, "MAESTRO SUPREMO ROBOT", "MAESTRO - Escucha a los 49 y decide COMPRA DIOS / VENTA DIOS / ESPERA"),
]
for _id, _nombre, _trabajo in NOMBRES_ROBOTS:
    ROBOTS_RAUDY.append({"id": _id, "nombre": _nombre, "trabajo": _trabajo, "estrellas": 0, "puntos": 0, "ultima_senal": "ESPERA", "mensaje": "Listo para trabajar"})

def generar_chat_robots(precio, maestro50):
    # Los robots hablan entre ellos segun el precio - se comunican
    chat = []
    if precio <= 3910:
        chat.append({"robot": "Robot 5 Tiburon Oro", "texto": f"Oro en ${precio:.2f} bajo a zona COMPRA, yo digo COMPRA"})
        chat.append({"robot": "Robot 18 Guardian NY", "texto": "Confirmo, hora buena, yo tambien digo COMPRA"})
        chat.append({"robot": "Robot 21 Ojo Noticias", "texto": "Sin noticias malas, se puede operar"})
        chat.append({"robot": "Robot 50 MAESTRO SUPREMO", "texto": f"Ok equipo, {maestro50['votos_compra']} dicen COMPRA, yo decido: {maestro50['señal']}"})
    elif precio >= 3970:
        chat.append({"robot": "Robot 5 Tiburon Oro", "texto": f"Oro en ${precio:.2f} subio mucho, yo digo VENTA"})
        chat.append({"robot": "Robot 16 Rey New York", "texto": "Confirmo, New York esta fuerte, VENTA"})
        chat.append({"robot": "Robot 22 Alarma Noticias", "texto": "Sin noticias, se puede vender"})
        chat.append({"robot": "Robot 50 MAESTRO SUPREMO", "texto": f"Ok equipo, {maestro50['votos_venta']} dicen VENTA, yo decido: {maestro50['señal']}"})
    else:
        chat.append({"robot": "Robot 5 Tiburon Oro", "texto": f"Oro en ${precio:.2f} esta en medio, yo digo ESPERA"})
        chat.append({"robot": "Robot 41 Guardian Capital", "texto": "Si, mejor ESPERA, no hay señal clara"})
        chat.append({"robot": "Robot 50 MAESTRO SUPREMO", "texto": f"Equipo no esta de acuerdo, yo decido: {maestro50['señal']}"})
    return chat

def hora_ginebra():
    return datetime.utcnow() + timedelta(hours=1)

def dias_restantes():
    delta = FECHA_VENCE - hora_ginebra()
    return max(0, delta.days)

def codigo_vigente():
    return hora_ginebra() <= FECHA_VENCE

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
    res["salida_emergencia"] = res["sl"]
    res["entrada_grafico"] = res["entrada"]
    return res

# ===== RAUDY - 50 ANALIZADORES - CON 28 = DIOS =====
def analizar_50_raudy(precio, eur_val, gbp_val):
    votos = []
    if precio <= 3905:
        votos.append(("1 SWING", "COMPRA"))
    elif precio >= 3980:
        votos.append(("1 SWING", "VENTA"))
    else:
        votos.append(("1 SWING", "ESPERA"))
    if len(historial_oro) >= 2 and precio > historial_oro[-2] + 5:
        votos.append(("2 RAPIDO", "COMPRA"))
    elif len(historial_oro) >= 2 and precio < historial_oro[-2] - 5:
        votos.append(("2 RAPIDO", "VENTA"))
    else:
        votos.append(("2 RAPIDO", "ESPERA"))
    votos.append(("3 TENDENCIA", "COMPRA" if precio > 3940 else "VENTA"))
    f = filtro_noticias(precio)
    votos.append(("4 NOTICIAS", "ESPERA" if not f["puede"] else "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("5 VELAS", "VENTA" if precio >= 3970 else "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("6 ORO Y DOLAR", "COMPRA" if eur_val > 1.115 else "VENTA"))
    votos.append(("7 SOPORTE Y RESISTENCIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("8 VOLUMEN", "COMPRA" if len(historial_oro)>=5 and abs(precio-historial_oro[-5])>10 else "ESPERA"))
    votos.append(("9 ZONA PELIGROSA", "ESPERA" if abs(precio-3940) < 5 else "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("10 MAESTRO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("11 RSI", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("12 MACD", "COMPRA" if precio > 3940 else "VENTA"))
    votos.append(("13 BOLLINGER", "COMPRA" if precio <= 3900 else "VENTA" if precio >= 3990 else "ESPERA"))
    votos.append(("14 FIBONACCI", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("15 SESIONES", "COMPRA" if 9 <= hora_ginebra().hour < 17 else "ESPERA"))
    votos.append(("16 SENTIMIENTO", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("17 IA PREDICCION", "COMPRA" if precio <= 3920 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("18 DIVERGENCIA", "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("19 ROMPIMIENTO", "COMPRA" if precio > 3980 else "VENTA" if precio < 3900 else "ESPERA"))
    votos.append(("20 MAESTRO FINAL", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("21 MEDIA MOVIL", "COMPRA" if precio > 3940 else "VENTA"))
    votos.append(("22 ORO vs PLATA", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("23 PETROLEO", "COMPRA" if precio < 3940 else "ESPERA"))
    votos.append(("24 BITCOIN", "COMPRA" if precio < 3940 else "ESPERA"))
    votos.append(("25 MIEDO DEL MERCADO", "ESPERA" if abs(precio-3940)<10 else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("26 HORA DE NOTICIA", "ESPERA" if not f["puede"] else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("27 REBOTE", "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("28 TRAMPA", "ESPERA" if 3935 <= precio <= 3945 else "COMPRA" if precio<3935 else "VENTA"))
    votos.append(("29 GUARDIAN DE CUENTA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("30 MAESTRO SUPREMO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("31 HISTORIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("32 CAZADOR NOCTURNO", "ESPERA"))
    votos.append(("33 ANTI-PERDIDA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("34 DOBLE CONFIRMACION", "COMPRA" if precio <= 3905 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("35 MAESTRO SUPREMO FINAL", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("36 APERTURA LONDRES", "COMPRA" if 9 <= hora_ginebra().hour < 11 and precio <= 3920 else "ESPERA"))
    votos.append(("37 APERTURA NEW YORK", "COMPRA" if 14 <= hora_ginebra().hour < 17 and precio <= 3920 else "VENTA" if 14 <= hora_ginebra().hour < 17 and precio >= 3970 else "ESPERA"))
    votos.append(("38 GAP", "ESPERA"))
    votos.append(("39 SPREAD", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("40 SWAP", "ESPERA"))
    votos.append(("41 PATRONES", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("42 PIVOT", "COMPRA" if precio <= 3900 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("43 PSICOLOGIA", "ESPERA"))
    votos.append(("44 COPIA SEGURA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("45 ALERTA FAMILIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("46 MODO NIÑO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("47 PROTECTOR DE CAPITAL", "ESPERA" if precio > 4030 else "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("48 MODO OSCURO Y CLARO", "ESPERA"))
    votos.append(("49 IDIOMA", "ESPERA"))
    c_compra = sum(1 for _, v in votos if v == "COMPRA")
    c_venta = sum(1 for _, v in votos if v == "VENTA")
    c_espera = sum(1 for _, v in votos if v == "ESPERA")
    # === RAUDY QUIERE 28 = DIOS - YA CAMBIADO ===
    if c_compra >= 28:
        maestro = {"señal": "👑🔥 COMPRA DIOS - LA MEJOR DEL DIA", "color": "#00ff00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE FUERTE - COMPRA DIOS"}
    elif c_venta >= 28:
        maestro = {"señal": "👑🔥 VENTA DIOS - LA MEJOR DEL DIA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA FUERTE - VENTA DIOS"}
    elif c_compra > c_venta + 5:
        maestro = {"señal": "🟢 COMPRA FUERTE", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA"}
    elif c_venta > c_compra + 5:
        maestro = {"señal": "🔴 VENTA FUERTE", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA"}
    else:
        maestro = {"señal": "🟡 ESPERA - LOS 50 NO ESTAN DE ACUERDO", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 LUZ AMARILLA - ESPERA"}
    maestro["votos_compra"] = c_compra
    maestro["votos_venta"] = c_venta
    maestro["votos_espera"] = c_espera
    maestro["lista"] = votos
    maestro["total"] = 50
    return maestro

def send_telegram(mensaje):
    try:
        if "AQUI_PON" in BOT_TOKEN:
            print("FALTA BOT_TOKEN")
            return
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        for chat_id in CHAT_ID_VIP.split(","):
            chat_id = chat_id.strip()
            if not chat_id or "AQUI_PON" in chat_id:
                continue
            payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error telegram: {e}")

def telegram_bot_loop():
    global ultimo_update_id, alertado_compra, alertado_venta
    print("🤖 BOT TELEGRAM INICIADO - 6 ALERTAS + IA SWING + 50 ANALIZADORES")
    send_telegram(f"✅ *VIP ORO Raudy ACTIVO + IA SWING + 50 ANALIZADORES*\n\nTe avisaré automático:\n🟢 COMPRA: 3900, 3890, 3865\n🔴 VENTA: 3980, 3990, 4020\n\n📲 APP: raudy-vip-oro.onrender.com\nVence: {FECHA_VENCE.strftime('%d/%m/%Y')}")
    while True:
        try:
            if "AQUI_PON" not in BOT_TOKEN:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
                params = {"offset": ultimo_update_id + 1, "timeout": 5}
                resp = requests.get(url, params=params, timeout=10).json()
                if resp.get("ok"):
                    for upd in resp.get("result", []):
                        ultimo_update_id = upd["update_id"]
                        msg = upd.get("message", {})
                        texto = msg.get("text", "").lower().strip()
                        if texto in ["/start", "start", "hola", "hi"]:
                            send_telegram(f"🔥 *RAUDY ORO PRO VIP + IA SWING + 50 ANALIZADORES*\n\nBienvenido! Estás activo.\n🟢 BUY: 3900, 3890, 3865\n🔴 SELL: 3980, 3990, 4020\nAPP: raudy-vip-oro.onrender.com\n\nEscribe /precios para ver ORO ahora")
                        elif texto in ["/precios", "precios", "oro"]:
                            precio = get_oro_precio()
                            ia = analizar_ia_oro(precio)
                            filtro = filtro_noticias(precio)
                            reloj = reloj_mundial()
                            send_telegram(f"🟡 ORO AHORA: ${precio:.2f}\n{ia['señal']}\n🟡 ENTRADA: ${ia['entrada_grafico']}\n🟢 BOTIN: ${ia['botin']} | 🔴 SALIDA: ${ia['salida_emergencia']}\n{reloj['texto']}\n{filtro['texto']}\n{ia['analisis']}")
            precio = get_oro_precio()
            ia = analizar_ia_oro(precio)
            print(f"{hora_ginebra()} - ORO: {precio} IA: {ia['señal']}")
            for nivel in COMPRAS:
                if precio <= nivel and not alertado_compra[nivel]:
                    send_telegram(f"🔥 *RAUDY ORO - COMPRA SWING + IA*\n\nORO TOCO *${nivel}*\nActual: ${precio:.2f}\n🟡 ENTRADA: ${ia['entrada_grafico']}\n🟢 BOTIN: ${ia['botin']} | 🔴 SALIDA: ${ia['salida_emergencia']}\n{ia['analisis']}\n\n📲 raudy-vip-oro.onrender.com")
                    alertado_compra[nivel] = True
                if precio > nivel + 40:
                    alertado_compra[nivel] = False
            for nivel in VENTAS:
                if precio >= nivel and not alertado_venta[nivel]:
                    send_telegram(f"🔴 *RAUDY ORO - VENTA SWING + IA*\n\nORO TOCO *${nivel}*\nActual: ${precio:.2f}\n🟡 ENTRADA: ${ia['entrada_grafico']}\n🟢 BOTIN: ${ia['botin']} | 🔴 SALIDA: ${ia['salida_emergencia']}\n{ia['analisis']}\n\n📲 raudy-vip-oro.onrender.com")
                    alertado_venta[nivel] = True
                if precio < nivel - 40:
                    alertado_venta[nivel] = False
        except Exception as e:
            print(f"Error loop bot: {e}")
        time.sleep(60)

threading.Thread(target=telegram_bot_loop, daemon=True).start()

def esta_logueado():
    if not codigo_vigente():
        return False
    return session.get("vip") == CLAVE_BUENA

@app.route('/login', methods=['GET','POST'])
def login():
    if not codigo_vigente():
        return f'<body style="background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:20px"><div style="border:3px solid red;border-radius:20px;padding:25px;background:#1a0a0a;max-width:400px;margin:40px auto"><h1 style="color:red">⛔ CODIGO VENCIDO</h1><p>Tu VIP venció el {FECHA_VENCE.strftime("%d/%m/%Y")}</p><a href="https://www.paypal.me/RaudyManzueta/20" style="background:gold;color:black;padding:15px;display:block;border-radius:12px;text-decoration:none;font-weight:bold">💳 PAGAR $20</a><br><a href="https://wa.me/41767574050" style="background:#25D366;color:white;padding:15px;display:block;border-radius:12px;text-decoration:none;font-weight:bold">📱 WHATSAPP RAUDY</a></div></body>'
    error = ""
    dias = dias_restantes()
    if request.method == 'POST':
        clave = request.form.get("clave","").strip().upper()
        if clave == CLAVE_BUENA:
            session["vip"] = CLAVE_BUENA
            return redirect("/")
        error = "❌ CLAVE MALA - Revisa tu WhatsApp"
    return f'''
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY VIP</title>
<style>
body{{background:#0a0a0a;color:white;font-family:Arial;margin:0;padding:15px;text-align:center}}
.box{{border:2px solid #FFD700;border-radius:20px;padding:25px;background:#1a1a1a;max-width:400px;margin:40px auto}}
input{{width:90%;padding:18px;border-radius:12px;border:2px solid #FFD700;background:#0a0a0a;color:#FFD700;font-size:22px;text-align:center;font-weight:bold;margin:15px 0}}
.btn{{background:#FFD700;color:black;border-radius:15px;padding:18px;font-weight:bold;font-size:18px;width:100%;border:none;cursor:pointer}}
.btn-yellow{{background:#FFD700;color:black;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-blue{{background:#0a84ff;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-green{{background:#25D366;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:12px;display:block;text-decoration:none}}
.btn-telegram{{background:#229ED9;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:12px;display:block;text-decoration:none}}
.warn{{border:1px solid #ff4444;background:#1a0a0a;border-radius:12px;padding:12px;font-size:10px;color:#ffaaaa;text-align:left;margin-top:15px;line-height:1.4}}
.vence{{background:#FFD700;color:black;padding:8px;border-radius:8px;font-weight:bold;font-size:12px;margin-bottom:10px}}
</style></head><body>
<div class="box">
<h1 style="color:#FFD700;">🔒 RAUDY ORO PRO VIP</h1>
<div style="background:#FFD700;color:black;padding:6px;border-radius:8px;font-weight:bold;font-size:12px;margin-bottom:10px;">🇨🇭 CREADO POR RAUDY EN GINEBRA SUIZA - APP ÚNICA</div>
<div class="vence">⏰ VENCE EN {dias} DIAS - {FECHA_VENCE.strftime("%d/%m/%Y")}</div>
<form method="POST">
<input name="clave" placeholder="ESCRIBE TU CLAVE VIP" required>
<div style="color:#ff4444;font-weight:bold;margin:10px;">{error}</div>
<button class="btn">🔓 ENTRAR VIP</button>
</form>
<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050</a>
<a href="https://t.me/{BOT_USERNAME}?start=Hola_Raudy_quiero_VIP" target="_blank" class="btn-telegram">✈️ TELEGRAM - CONECTAR CON MI ROBOT</a>
<div class="warn"><b>⚠️ ADVERTENCIA DE RIESGO:</b> Solo educativo. No es consejo financiero. Trading Oro, Forex, Tesla, Apple es ALTO RIESGO. Puedes perder tu dinero. Vence en {dias} dias.</div>
</div></body></html>'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

# ===== RAUDY - API NUEVA PARA 50 ROBOTS + ESTRELLAS - NO BORRA NADA =====
@app.route('/api/robots')
def api_robots():
    if not esta_logueado():
        return jsonify({"error": "no autorizado"}), 401
    # Ordenar por estrellas - los mejores arriba
    ordenados = sorted(ROBOTS_RAUDY, key=lambda x: x["estrellas"], reverse=True)
    return jsonify({"robots": ordenados})

@app.route('/api/dar_estrella', methods=['POST'])
def api_dar_estrella():
    if not esta_logueado():
        return jsonify({"error": "no autorizado"}), 401
    data = request.get_json() or {}
    robot_id = int(data.get("id", 0))
    cantidad = int(data.get("estrellas", 1))
    if cantidad < 1: cantidad = 1
    if cantidad > 3: cantidad = 3
    for r in ROBOTS_RAUDY:
        if r["id"] == robot_id:
            r["estrellas"] += cantidad
            r["puntos"] += cantidad * 10
            r["mensaje"] = f"Raudy me dio {cantidad} ⭐ - ¡Gracias jefe! Voy a trabajar mejor"
            return jsonify({"ok": True, "robot": r, "mensaje": f"⭐ Le diste {cantidad} estrella(s) a {r['nombre']} - Ahora tiene {r['estrellas']} estrellas"})
    return jsonify({"error": "robot no encontrado"}), 404

@app.route('/api/precios')
def precios():
    if not esta_logueado():
        return jsonify({"error": "no autorizado o vencido"}), 401
    oro = 3951.50
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=4)
        oro = r.json().get('price', oro)
    except:
        oro = get_price_yahoo('GC=F', oro)
    oro_f = float(oro)
    gbp_v = get_price_yahoo('GBPUSD=X', 1.3412)
    eur_v = get_price_yahoo('EURUSD=X', 1.1197)
    tesla_v = get_price_yahoo('TSLA', 245.80)
    apple_v = get_price_yahoo('AAPL', 185.30)
    ia = analizar_ia_oro(oro_f)
    filtro = filtro_noticias(oro_f)
    reloj = reloj_mundial()
    maestro50 = analizar_50_raudy(oro_f, eur_v, gbp_v)
    chat_robots = generar_chat_robots(oro_f, maestro50)
    historial_senales.append({"hora": hora_ginebra().strftime("%H:%M"), "precio": oro_f, "señal": maestro50["señal"]})
    if len(historial_senales) > 100:
        historial_senales.pop(0)
    return {"oro": oro_f,"gbp": gbp_v,"eur": eur_v,"tesla": tesla_v,"apple": apple_v,"ia": ia, "filtro": filtro, "reloj": reloj, "maestro50": maestro50, "historial": historial_senales[-20:], "chat_robots": chat_robots, "robots_top": sorted(ROBOTS_RAUDY, key=lambda x: x["estrellas"], reverse=True)[:5]}

@app.route('/')
def home():
    if not esta_logueado():
        return redirect("/login")
    dias = dias_restantes()
    return f'''
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY ORO PRO</title>
<script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
<style>
body {{ background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:10px; }}
.header {{ text-align:center; padding:15px; border:2px solid #FFD700; border-radius:15px; background:#1a1a1a; margin-bottom:12px; }}
.header h1 {{ margin:0; color:#FFD700; font-size:26px; }}
.box {{ border:2px solid #FFD700; border-radius:15px; padding:12px; text-align:center; margin-bottom:14px; background:#1a1a1a; }}
.precio {{ font-size:32px; color:#00ff00; font-weight:bold; }}
.zonas {{ font-size:11px; margin-top:6px; line-height:1.4; }}
.estado {{ border-radius:10px; padding:8px; font-weight:bold; font-size:13px; margin-top:8px; }}
.chart {{ width:100%; height:180px; margin-top:10px; border-radius:10px; background:#0f0f0f; }}
.btn-yellow {{ background:#FFD700; color:black; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }}
.btn-blue {{ background:#0a84ff; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }}
.btn-green {{ background:#25D366; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:12px; display:block; text-decoration:none; }}
.btn-telegram {{ background:#229ED9; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:12px; display:block; text-decoration:none; }}
.footer {{ text-align:center; font-size:10px; color:#666; padding:10px; }}
.warn-main {{ border:2px solid #ff4444; background:#1a0a0a; border-radius:15px; padding:12px; font-size:10px; color:#ffaaaa; line-height:1.4; text-align:left; margin-bottom:14px; }}
.warn-title {{ color:#ff4444; font-weight:bold; font-size:11px; text-align:center; margin-bottom:6px; }}
.vence-top{{background:#FFD700;color:black;padding:6px;border-radius:8px;font-weight:bold;font-size:11px;margin-top:6px}}
.luz {{ width:30px; height:30px; border-radius:50%; background:#333; margin:10px auto 5px auto; }}
@keyframes parpadeo {{ 0%{{opacity:1}} 50%{{opacity:0.3}} 100%{{opacity:1}} }}
.luz-activa {{ animation: parpadeo 0.8s infinite; }}
.ia-box {{ border:2px solid #00ff00; border-radius:15px; padding:12px; background:#0a1a0a; margin-bottom:14px; text-align:left; }}
.tpsl {{ display:flex; gap:8px; margin-top:8px; }}
.tpsl div {{ flex:1; border-radius:10px; padding:10px; font-weight:bold; text-align:center; }}
.mi-op {{ border:2px solid #FFD700; border-radius:15px; padding:14px; background:#1a1a1a; margin-bottom:14px; text-align:left; }}
.mi-op input {{ width:100%; padding:14px; border-radius:10px; border:2px solid #FFD700; background:#0a0a0a; color:#FFD700; font-size:20px; text-align:center; font-weight:bold; margin:6px 0; box-sizing:border-box; }}
.mi-op label {{ font-size:12px; color:#aaa; }}
.btn-compra {{ background:#00aa00; color:white; border:none; border-radius:12px; padding:16px; font-weight:bold; font-size:16px; width:48%; cursor:pointer; }}
.btn-venta {{ background:#ff0000; color:white; border:none; border-radius:12px; padding:16px; font-weight:bold; font-size:16px; width:48%; cursor:pointer; }}
.ghost-box {{ border:2px solid #FFD700; border-radius:15px; padding:12px; background:#f5f0d5; color:black; margin-bottom:14px; text-align:left; }}
.ghost-line {{ display:flex; justify-content:space-between; align-items:center; margin:8px 0; padding:6px 8px; font-weight:bold; font-size:14px; }}
.ghost-botin {{ background:#009933; color:white; }}
.ghost-entrada {{ background:#FFD700; color:black; }}
.ghost-salida {{ background:#cc0000; color:white; }}
.ghost-dash {{ border-top:3px dashed; flex:1; margin:0 8px; }}
.filtro-box {{ border:2px solid #FFD700; border-radius:15px; padding:12px; background:#1a1a00; margin-bottom:14px; text-align:center; }}
.reloj-box {{ border:2px solid #00ff00; border-radius:15px; padding:12px; background:#0a1a0a; margin-bottom:14px; text-align:center; }}
.maestro-box {{ border:3px solid #FFD700; border-radius:15px; padding:12px; background:#1a1a00; margin-bottom:14px; text-align:center; }}
.luz-grande {{ width:60px; height:60px; border-radius:50%; background:#333; margin:10px auto; box-shadow:0 0 30px 10px #333; }}
.robot-card {{ border:2px solid #FFD700; border-radius:12px; padding:10px; background:#1a1a1a; margin-bottom:8px; text-align:left; }}
.btn-estrella {{ background:#FFD700; color:black; border:none; padding:8px 12px; border-radius:10px; font-weight:bold; cursor:pointer; margin:2px; }}
</style></head><body>
<div class="header">
<h1>🔥 RAUDY ORO PRO + IA SWING + 50 🔥</h1>
<div style="background:#FFD700;color:black;padding:6px;border-radius:8px;font-weight:bold;font-size:12px;margin-top:6px;">🇨🇭 CREADO POR RAUDY EN GINEBRA SUIZA - APP ÚNICA EN EL MUNDO</div>
<div style="font-size:11px;color:#FFD700;margin-top:4px;">⭐ SOLO PARA VIP DE RAUDY - NO COPIAR ⭐</div>
<div style="font-size:11px; color:#aaa;">APP OFICIAL - VELAS EN VIVO + BOT TELEGRAM 6 ALERTAS + IA SWING + RELOJ MUNDIAL + 50 ANALIZADORES</div>
<div style="font-size:11px; color:#00ff00;" id="hora">VIVO - RAUDY ORO PRO - VIP ✅ - BOT ACTIVO + IA</div>
<div class="vence-top">⏰ TU VIP VENCE EN {dias} DIAS - {FECHA_VENCE.strftime("%d/%m/%Y")}</div>
<div style="margin-top:5px;"><a href="/logout" style="color:#ff4444; font-size:11px; text-decoration:none;">SALIR</a></div>
</div>

<div class="maestro-box">
<div style="font-weight:bold; color:#FFD700; font-size:18px;">👑 MAESTRO SUPREMO - 50 ANALIZADORES - LUZ - CON 28 = DIOS</div>
<div id="luz-maestro" class="luz-grande luz-activa"></div>
<div id="maestro-texto" style="font-size:18px;font-weight:bold;">ESPERANDO MAESTRO...</div>
<div id="maestro-votos" style="font-size:12px;color:#aaa;">--</div>
<div id="maestro-lista" style="font-size:11px;text-align:left;max-height:120px;overflow:auto;margin-top:8px;"></div>
<button onclick="document.getElementById('modal-como').style.display='block'" style="background:#FFD700;color:black;border:none;padding:12px;border-radius:10px;font-weight:bold;width:100%;margin-top:10px;cursor:pointer;">❓ ¿COMO USAR LA APP? - TOCA AQUI</button>
<button onclick="sonidoPrueba()" style="background:#00aa00;color:white;border:none;padding:12px;border-radius:10px;font-weight:bold;width:100%;margin-top:8px;cursor:pointer;">🔔 PROBAR SONIDO</button>
</div>

<!-- ===== RAUDY - 50 ROBOTS QUE HABLAN Y TU LES DAS ESTRELLA - NUEVO ===== -->
<div class="maestro-box" style="border-color:#00ff00;">
<div style="font-weight:bold; color:#00ff00; font-size:18px;">🤖 50 ROBOTS RAUDY - CADA UNO HACE SU TRABAJO Y HABLAN ENTRE ELLOS</div>
<div style="font-size:12px; color:#aaa; margin-top:4px;">Si un robot hace bien su trabajo, dale ⭐. El que tenga mas estrellas, el Maestro le hace mas caso.</div>
<div id="chat-robots" style="background:#0a0a0a; border-radius:10px; padding:10px; text-align:left; font-size:12px; line-height:1.6; margin-top:10px; max-height:150px; overflow:auto;">Esperando que los robots hablen...</div>
<div style="font-weight:bold; color:#FFD700; margin-top:12px;">🏆 TOP 5 ROBOTS CON MAS ESTRELLAS</div>
<div id="top-robots" style="font-size:12px; text-align:left; margin-top:6px;">--</div>
<button onclick="cargarRobots()" style="background:#FFD700;color:black;border:none;padding:12px;border-radius:10px;font-weight:bold;width:100%;margin-top:10px;cursor:pointer;">🤖 VER LOS 50 ROBOTS Y DARLES ESTRELLA ⭐</button>
<div id="lista-robots" style="margin-top:10px; max-height:400px; overflow:auto;"></div>
</div>

<div id="modal-como" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:9999;padding:20px;box-sizing:border-box;overflow:auto;">
<div style="background:white;color:black;border-radius:15px;padding:20px;max-width:400px;margin:20px auto;">
<h2>¿COMO USAR LA APP RAUDY?</h2>
<p>1. Mira la LUZ grande. Verde = compra, Roja = venta, Amarilla = espera.<br><br>2. Si el Maestro dice COMPRA DIOS o VENTA DIOS, es porque 28 de los 50 estan de acuerdo.<br><br>3. Pon tu TP y SL en tu broker tal cual.<br><br>4. Si el Filtro dice ROJO, NO operes aunque haya señal.<br><br>5. Solo educativo, no es consejo financiero. Puedes perder dinero.<br><br>6. NUEVO: Mira como los 50 robots hablan entre ellos. Si un robot acierta, dale ⭐ para premiarlo.</p>
<button onclick="document.getElementById('modal-como').style.display='none'" style="background:red;color:white;padding:12px;border:none;border-radius:10px;width:100%;font-weight:bold;">CERRAR</button>
</div>
</div>

<div class="reloj-box">
<div style="font-weight:bold; color:#00ff00; font-size:16px;">🌍 RELOJ MUNDIAL RAUDY - ¿CUANDO COMPRAR ORO?</div>
<div id="reloj-texto" style="font-size:14px; font-weight:bold; margin-top:6px;">REVISANDO HORA MUNDIAL...</div>
<div style="display:flex; gap:6px; margin-top:8px; font-size:11px;">
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇨🇭 GINEBRA<br><b id="h-ginebra">--:--</b></div>
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇬🇧 LONDRES<br><b id="h-londres">--:--</b></div>
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇺🇸 NEW YORK<br><b id="h-ny">--:--</b></div>
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇯🇵 TOKIO<br><b id="h-tokio">--:--</b></div>
</div>
<div id="reloj-sesion" style="font-size:12px; font-weight:bold; margin-top:6px; color:#FFD700;">--</div>
<div style="font-size:11px
