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

# ===== 50 ROBOTS RAUDY - NUEVO =====
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
    (9, "Guardian Scalping", "SCALPING - Protege de perdidas"),
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
    (46, "Guardian Modo Nino", "PROTECCION - Explica facil"),
    (47, "Guardian Psicologia", "PROTECCION - No operes con miedo"),
    (48, "Guardian Copia Segura", "PROTECCION - Copia solo si 28 dicen si"),
    (49, "Guardian Idioma", "PROTECCION - Traduce todo facil"),
    (50, "MAESTRO SUPREMO ROBOT", "MAESTRO - Escucha a los 49 y decide"),
]
for _id, _nombre, _trabajo in NOMBRES_ROBOTS:
    ROBOTS_RAUDY.append({"id": _id, "nombre": _nombre, "trabajo": _trabajo, "estrellas": 0, "puntos": 0, "mensaje": "Listo para trabajar"})

def generar_chat_robots(precio, maestro50):
    chat = []
    if precio <= 3910:
        chat.append({"robot": "Robot 5 Tiburon Oro", "texto": "Oro bajo a zona COMPRA, yo digo COMPRA"})
        chat.append({"robot": "Robot 18 Guardian NY", "texto": "Confirmo, hora buena, yo tambien digo COMPRA"})
        chat.append({"robot": "Robot 21 Ojo Noticias", "texto": "Sin noticias malas, se puede operar"})
        chat.append({"robot": "Robot 50 MAESTRO", "texto": "Ok equipo, yo decido: " + maestro50["señal"]})
    elif precio >= 3970:
        chat.append({"robot": "Robot 5 Tiburon Oro", "texto": "Oro subio mucho, yo digo VENTA"})
        chat.append({"robot": "Robot 16 Rey New York", "texto": "Confirmo, New York esta fuerte, VENTA"})
        chat.append({"robot": "Robot 50 MAESTRO", "texto": "Ok equipo, yo decido: " + maestro50["señal"]})
    else:
        chat.append({"robot": "Robot 5 Tiburon Oro", "texto": "Oro esta en medio, yo digo ESPERA"})
        chat.append({"robot": "Robot 41 Guardian Capital", "texto": "Si, mejor ESPERA, no hay señal clara"})
        chat.append({"robot": "Robot 50 MAESTRO", "texto": "Equipo no esta de acuerdo, yo decido: " + maestro50["señal"]})
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
            return {"texto": "🟡 CUIDADO - MERCADO LOCO SE MOVIO RAPIDO", "color": "#FFA500", "puede": True}
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
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🔴 HOY ES " + dia_nombre + " - MERCADO CERRADO", "color": "#ff0000", "sesion": "MERCADO CERRADO", "puede": False}
    if 9 <= hora_g < 11:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🟢 HOY " + dia_nombre + " - SESION LONDRES - BUENA HORA", "color": "#00aa00", "sesion": "LONDRES", "puede": True}
    if (hora_g == 14 and minuto >= 30) or (15 <= hora_g < 17):
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🟢🟢 HOY " + dia_nombre + " - SESION NEW YORK - LA MEJOR HORA", "color": "#00aa00", "sesion": "NEW YORK", "puede": True}
    if 2 <= hora_g < 6:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🔴 SESION ASIA - MERCADO DORMIDO", "color": "#ff0000", "sesion": "ASIA", "puede": False}
    if hora_g >= 22 or hora_g < 2:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🔴 MERCADO DE NOCHE - NO COMPRES", "color": "#ff0000", "sesion": "NOCHE", "puede": False}
    return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🟡 ENTRE SESIONES - ESPERA A LAS 09:00 O 14:30", "color": "#FFA500", "sesion": "ENTRE SESIONES", "puede": True}

def get_price_yahoo(symbol, fallback):
    try:
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + symbol
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
        res = {"señal": "🟢 COMPRA SWING", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA SWING", "analisis": "IA SWING: Oro en zona 3900-3865. Es zona de COMPRA.", "entrada": precio, "tp": round(precio + 35, 2), "sl": round(precio - 18, 2), "confianza": "88%"}
    elif precio >= 3980 and precio <= 4030:
        res = {"señal": "🔴 VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA SWING", "analisis": "IA SWING: Oro en zona 3980-4020. Es zona de VENTA.", "entrada": precio, "tp": round(precio - 35, 2), "sl": round(precio + 18, 2), "confianza": "88%"}
    elif precio > 4030:
        res = {"señal": "🔴 YA PASO ZONA VENTA - ESPERA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - YA PASO VENTA", "analisis": "IA SWING: Oro alto. YA PASO la zona de venta. Espera.", "entrada": precio, "tp": 3980, "sl": round(precio + 20, 2), "confianza": "65%"}
    elif precio > 3940:
        res = {"señal": "🔴 ESPERANDO VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - ESPERANDO VENTA", "analisis": "IA SWING: Oro en medio. Espera que suba a 3980 para venta o baje a 3900 para compra.", "entrada": precio, "tp": 3900, "sl": 4040, "confianza": "65%"}
    elif precio < 3940 and precio > 3905:
        res = {"señal": "🟡 CERCA DE COMPRA SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 LUZ NARANJA - CERCA DE COMPRA", "analisis": "IA SWING: Oro se acerca a compra. Si toca 3900 es COMPRA.", "entrada": 3900, "tp": 3935, "sl": 3882, "confianza": "70%"}
    else:
        res = {"señal": "🟡 ANALIZANDO SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 ANALIZANDO", "analisis": "IA: Analizando swing... Espera señal clara.", "entrada": precio, "tp": round(precio + 30, 2), "sl": round(precio - 15, 2), "confianza": "50%"}
    res["botin"] = res["tp"]
    res["salida_emergencia"] = res["sl"]
    res["entrada_grafico"] = res["entrada"]
    return res

def analizar_50_raudy(precio, eur_val, gbp_val):
    votos = []
    votos.append(("1 SWING", "COMPRA" if precio <= 3905 else "VENTA" if precio >= 3980 else "ESPERA"))
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
    votos.append(("7 SOPORTE", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
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
    votos.append(("25 MIEDO", "ESPERA" if abs(precio-3940)<10 else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("26 HORA NOTICIA", "ESPERA" if not f["puede"] else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("27 REBOTE", "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("28 TRAMPA", "ESPERA" if 3935 <= precio <= 3945 else "COMPRA" if precio<3935 else "VENTA"))
    votos.append(("29 GUARDIAN", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("30 MAESTRO SUPREMO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("31 HISTORIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("32 CAZADOR NOCTURNO", "ESPERA"))
    votos.append(("33 ANTI-PERDIDA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("34 DOBLE CONFIRMACION", "COMPRA" if precio <= 3905 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("35 MAESTRO FINAL 2", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("36 APERTURA LONDRES", "COMPRA" if 9 <= hora_ginebra().hour < 11 and precio <= 3920 else "ESPERA"))
    votos.append(("37 APERTURA NY", "COMPRA" if 14 <= hora_ginebra().hour < 17 and precio <= 3920 else "VENTA" if 14 <= hora_ginebra().hour < 17 and precio >= 3970 else "ESPERA"))
    votos.append(("38 GAP", "ESPERA"))
    votos.append(("39 SPREAD", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("40 SWAP", "ESPERA"))
    votos.append(("41 PATRONES", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("42 PIVOT", "COMPRA" if precio <= 3900 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("43 PSICOLOGIA", "ESPERA"))
    votos.append(("44 COPIA SEGURA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("45 ALERTA FAMILIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("46 MODO NINO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("47 PROTECTOR", "ESPERA" if precio > 4030 else "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("48 MODO OSCURO", "ESPERA"))
    votos.append(("49 IDIOMA", "ESPERA"))
    c_compra = sum(1 for _, v in votos if v == "COMPRA")
    c_venta = sum(1 for _, v in votos if v == "VENTA")
    c_espera = sum(1 for _, v in votos if v == "ESPERA")
    if c_compra >= 28:
        maestro = {"señal": "👑🔥 COMPRA DIOS - LA MEJOR DEL DIA", "color": "#00ff00", "luz": "#00ff00", "texto_luz": "🟢
