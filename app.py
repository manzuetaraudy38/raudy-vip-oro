from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
app = Flask(__name__)

# ============================================================
# 🏦 INFORMACION BANCARIA PARA EL JEFE
# ============================================================
EVENTOS_BANCOS_FIJOS = [
    {"evento": "FED - Tasa de Interés USA", "impacto": "ALTO", "hora": "14:00 NY", "efecto": "Si sube tasa, ORO BAJA. Si baja tasa, ORO SUBE"},
    {"evento": "NFP - Empleo USA", "impacto": "ALTO", "hora": "08:30 NY", "efecto": "Si empleo fuerte, ORO BAJA. Si empleo flojo, ORO SUBE"},
    {"evento": "CPI - Inflación USA", "impacto": "ALTO", "hora": "08:30 NY", "efecto": "Si inflación alta, ORO SUBE. Si inflación baja, ORO BAJA"},
    {"evento": "BCE - Banco Central Europa", "impacto": "ALTO", "hora": "08:15 NY", "efecto": "Mueve EUR y ORO fuerte"},
    {"evento": "FOMC - Habla Powell FED", "impacto": "ALTO", "hora": "14:30 NY", "efecto": "Cada palabra mueve el ORO $20-$50"},
    {"evento": "PPI - Precios Productor", "impacto": "MEDIO", "hora": "08:30 NY", "efecto": "Adelanta inflación"},
    {"evento": "Ventas Minoristas USA", "impacto": "MEDIO", "hora": "08:30 NY", "efecto": "Si ventas fuertes, dólar sube, oro baja"},
    {"evento": "PIB USA", "impacto": "ALTO", "hora": "08:30 NY", "efecto": "Mueve todo el mercado"},
]

def get_info_bancaria():
    bancos = {
        "fed_tasa": "5.25% - FED USA - Vigilando",
        "bce_tasa": "2.15% - BCE Europa",
        "inflacion_usa": "CPI - Vigilando cada mes",
        "fuente": "ForexFactory.com + TradingEconomics + federalreserve.gov + ecb.europa.eu",
        "eventos_hoy": EVENTOS_BANCOS_FIJOS,
        "alerta_banco": "SIN NOTICIA FUERTE AHORA - Robots pueden trabajar",
        "nivel_riesgo": "VERDE"
    }
    try:
        r = requests.get('https://api.tradingeconomics.com/calendar?c=guest:guest&f=json&d1=today&d2=today', timeout=4)
        if r.status_code == 200:
            data = r.json()
            eventos_reales = []
            for e in data[:8]:
                eventos_reales.append({
                    "evento": e.get('Event', 'Evento Banco'),
                    "impacto": e.get('Importance', 'MEDIO'),
                    "hora": e.get('Date', '')[:16],
                    "efecto": e.get('Country', 'USA') + " - " + e.get('Category', '')
                })
            if eventos_reales:
                bancos["eventos_hoy"] = eventos_reales
                for ev in eventos_reales:
                    if str(ev.get("impacto")).upper() in ["HIGH", "3", "ALTO"]:
                        bancos["alerta_banco"] = "⚠️ ALERTA BANCO: Hoy hay noticia FUERTE - " + ev["evento"] + " - JEFE ORDENA PRECAUCION"
                        bancos["nivel_riesgo"] = "ROJO"
                        break
    except:
        pass
    return bancos

# ============================================================
# 🆕 NUEVO - DXY + VIX + BTC + PETROLEO + BONO 10 AÑOS - AGREGADO AHORA
# ESTO ES LO QUE USAN LOS BANCOS - NO SE BORRO NADA DE LO TUYO
# ============================================================
def get_mercado_extra():
    # DXY = Dolar, VIX = Miedo, BTC = Bitcoin, CL = Petroleo, TNX = Bono 10 años
    dxy = get_precio_yahoo('DX-Y.NYB', 99.50)
    vix = get_precio_yahoo('^VIX', 15.20)
    btc = get_precio_yahoo('BTC-USD', 105000)
    petroleo = get_precio_yahoo('CL=F', 61.50)
    bono10 = get_precio_yahoo('^TNX', 4.10)
    # Interpretación para el JEFE
    if vix >= 30:
        vix_texto = "😱 PANICO TOTAL - VIX " + str(round(vix,2)) + " - JEFE ORDENA PAUSA - Viene caida fuerte"
        vix_nivel = "ROJO"
    elif vix >= 20:
        vix_texto = "⚠️ MIEDO ALTO - VIX " + str(round(vix,2)) + " - Cuidado, mercado nervioso"
        vix_nivel = "AMARILLO"
    else:
        vix_texto = "😎 MERCADO TRANQUILO - VIX " + str(round(vix,2)) + " - Se puede operar"
        vix_nivel = "VERDE"
    if dxy >= 101:
        dxy_texto = "💵 DOLAR FUERTE " + str(round(dxy,2)) + " - Malo para ORO, oro tiende a BAJAR"
        dxy_para_oro = "BAJISTA"
    elif dxy <= 98:
        dxy_texto = "💵 DOLAR DEBIL " + str(round(dxy,2)) + " - Bueno para ORO, oro tiende a SUBIR"
        dxy_para_oro = "ALCISTA"
    else:
        dxy_texto = "💵 DOLAR NEUTRAL " + str(round(dxy,2)) + " - Oro sin presion del dolar"
        dxy_para_oro = "NEUTRAL"
    return {
        "DXY": dxy, "DXY_texto": dxy_texto, "DXY_para_oro": dxy_para_oro,
        "VIX": vix, "VIX_texto": vix_texto, "VIX_nivel": vix_nivel,
        "BTC": btc, "PETROLEO": petroleo, "BONO10": bono10,
        "fuente": "Yahoo Finance USA - DX-Y.NYB + ^VIX + BTC-USD + CL=F + ^TNX - GRATIS",
        "resumen_jefe": dxy_texto + " | " + vix_texto
    }

# ============================================================
# 🆕 NUEVO - PRESIDENTE USA + PREGUNTALE AL ROBOT - AGREGADO AHORA
# ESTO ES LO NUEVO - NO SE BORRO NADA DE LO TUYO
# ============================================================
EVENTOS_PRESIDENCIALES_FIJOS = [
    {"evento": "Presidente USA - Habla de Economía", "impacto": "ALTO", "efecto": "Si habla de aranceles o guerra, ORO SUBE fuerte"},
    {"evento": "Casa Blanca - Cambio de Ley / Arancel", "impacto": "ALTO", "efecto": "Arancel nuevo = ORO se mueve $30-$80"},
    {"evento": "Presidente - Reunión con FED", "impacto": "ALTO", "efecto": "Si presiona a FED para bajar tasa, ORO SUBE"},
    {"evento": "Elecciones / Decisión Presidencial", "impacto": "ALTO", "efecto": "Incertidumbre = ORO SUBE"},
]

def get_alerta_presidencial():
    alerta = {
        "nivel": "VERDE",
        "mensaje": "🟢 SIN CAMBIO PRESIDENCIAL AHORA - Presidente tranquilo",
        "accion_jefe": "Puedes operar normal",
        "eventos": EVENTOS_PRESIDENCIALES_FIJOS,
        "fuente": "whitehouse.gov + TradingEconomics"
    }
    try:
        r = requests.get('https://api.tradingeconomics.com/calendar?c=guest:guest&f=json&d1=today&d2=today', timeout=4)
        if r.status_code == 200:
            for e in r.json():
                t = (str(e.get('Event', '')) + " " + str(e.get('Category', ''))).lower()
                if any(p in t for p in ["president", "white house", "election", "tariff", "government", "treasury", "speech"]):
                    alerta["nivel"] = "ROJO"
                    alerta["mensaje"] = "🚨 ALERTA PRESIDENTE: " + e.get('Event', 'Cambio Presidencial') + " - JEFE ORDENA PAUSA 1 HORA"
                    alerta["accion_jefe"] = "NO COMPRES AHORA - Espera que pase el discurso"
                    break
    except:
        pass
    return alerta

def robot_responde_pregunta(precio_quiero, activo="ORO", precio_actual=4088):
    precio_quiero = float(precio_quiero)
    zonas = {
        "ORO": {"compra": 3910, "venta": 3970, "soporte": 3940, "resistencia": 4150},
        "NVDA": {"compra": 180, "venta": 195, "soporte": 180, "resistencia": 195},
        "AAPL": {"compra": 255, "venta": 270, "soporte": 255, "resistencia": 270},
        "TSLA": {"compra": 330, "venta": 355, "soporte": 330, "resistencia": 355},
        "MSFT": {"compra": 490, "venta": 505, "soporte": 490, "resistencia": 505},
        "AMZN": {"compra": 230, "venta": 245, "soporte": 230, "resistencia": 245},
        "META": {"compra": 640, "venta": 660, "soporte": 640, "resistencia": 660},
        "GOOGL": {"compra": 280, "venta": 292, "soporte": 280, "resistencia": 292},
    }
    z = zonas.get(activo, zonas["ORO"])
    presi = get_alerta_presidencial()
    if presi["nivel"] == "ROJO":
        return {"respuesta": "🛑 JEFE NO COMPRES AHORA - " + presi["mensaje"] + " - Espera 1 hora", "decision": "ESPERA-PRESIDENTE", "precio_recomendado": z["soporte"], "precio_actual": precio_actual}
    if precio_quiero > z["venta"] and precio_quiero > precio_actual:
        return {"respuesta": "❌ NO JEFE, NO compres " + activo + " a $" + str(precio_quiero) + ", está CARO. Ahora está en $" + str(precio_actual) + " y va a BAJAR a $" + str(z["soporte"]) + ". ESPERA a $" + str(z["soporte"]) + ".", "decision": "NO-COMPRAR-ESPERA", "precio_recomendado": z["soporte"], "precio_actual": precio_actual, "ahorro": round(precio_quiero - z["soporte"], 2)}
    if precio_quiero <= z["compra"] + 30:
        return {"respuesta": "✅ SÍ JEFE, COMPRA YA " + activo + " a $" + str(precio_quiero) + ", está BARATO. Zona del JEFE.", "decision": "SI-COMPRAR", "precio_recomendado": precio_quiero, "precio_actual": precio_actual}
    return {"respuesta": "🟡 JEFE, ESPERA. Quieres comprar a $" + str(precio_quiero) + " pero ahora está en $" + str(precio_actual) + ". Mejor espera a $" + str(z["soporte"]) + " y te ahorras $" + str(round(precio_quiero - z["soporte"], 2)) + ".", "decision": "ESPERA-BAJE", "precio_recomendado": z["soporte"], "precio_actual": precio_actual}

ROBOTS_EQUIPO_COMPLETO = {
    40: {"nombre": "MAESTRO DIOS RAUDY - JEFE", "rol": "JEFE", "tarea": "Yo mando a los 39. Yo leo bancos, FED, BCE, NFP, CPI, DXY, VIX. Yo digo CUANDO operar y CUANDO PARAR. Nadie opera sin mi permiso."},
    1: {"nombre": "RAYO RAUDY", "rol": "TRABAJADOR", "tarea": "Busca noticias USA rapido"},
    2: {"nombre": "RAYO VELOZ", "rol": "TRABAJADOR", "tarea": "Busca noticias NVDA y TESLA"},
    3: {"nombre": "COMETA ORO", "rol": "TRABAJADOR", "tarea": "Busca noticias del ORO"},
    4: {"nombre": "GUARDIA 08:30", "rol": "VIGIA BANCO", "tarea": "Vigila noticias 08:30 - NFP, CPI - Si hay noticia, avisa al JEFE"},
    5: {"nombre": "COMETA VENTA", "rol": "TRABAJADOR", "tarea": "Busca ventas fuertes"},
    6: {"nombre": "COMETA FUERTE", "rol": "TRABAJADOR", "tarea": "Analiza caidas rapidas"},
    7: {"nombre": "COMETA DIOS", "rol": "TRABAJADOR", "tarea": "Avisa cuando viene venta grande"},
    8: {"nombre": "RAYO COMPRA", "rol": "TRABAJADOR", "tarea": "Busca compras rapidas"},
    9: {"nombre": "RAYO ORO", "rol": "TRABAJADOR", "tarea": "Sigue ORO segundo a segundo"},
    10: {"nombre": "HIELO PACIENTE", "rol": "TRABAJADOR", "tarea": "Espera frio, no entra con prisa"},
    11: {"nombre": "HIELO ANALISTA", "rol": "TRABAJADOR", "tarea": "Analiza si mercado esta tranquilo"},
    12: {"nombre": "FUEGO COMPRA", "rol": "TRABAJ
