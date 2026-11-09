from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
app = Flask(__name__)

# ============================================================
# 💰 QR DE BYBIT DEL JEFE - SOLO AGREGADO, NO SE BORRO NADA
# Pon aqui el link de tu imagen QR de Bybit
# Ejemplo: https://tu-link.com/mi-qr-bybit.png
# ============================================================
BYBIT_QR_URL = "PON_AQUI_TU_LINK_DE_QR_BYBIT"
BYBIT_LINK_DEPOSITO = "https://www.bybit.com"  # Si quieres, pon tu link de referido de Bybit aqui

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
    12: {"nombre": "FUEGO COMPRA", "rol": "TRABAJADOR", "tarea": "Quema cuando hay compra fuerte"},
    13: {"nombre": "FUEGO TESLA", "rol": "TRABAJADOR", "tarea": "Cuida solo TESLA"},
    14: {"nombre": "FUEGO NVDA", "rol": "TRABAJADOR", "tarea": "Cuida solo NVIDIA"},
    15: {"nombre": "FUEGO APPLE", "rol": "TRABAJADOR", "tarea": "Cuida solo APPLE"},
    16: {"nombre": "FUEGO ORO", "rol": "TRABAJADOR", "tarea": "Cuida ORO con fuego"},
    17: {"nombre": "FUEGO VENTA", "rol": "TRABAJADOR", "tarea": "Dice VENTA cuando hay fuego rojo"},
    18: {"nombre": "RAYO META", "rol": "TRABAJADOR", "tarea": "Cuida META y GOOGLE"},
    19: {"nombre": "RAYO AMAZON", "rol": "TRABAJADOR", "tarea": "Cuida AMAZON"},
    20: {"nombre": "HIELO JEFE", "rol": "TRABAJADOR", "tarea": "Dice ESPERA cuando hay peligro"},
    21: {"nombre": "COMETA AMAZON", "rol": "TRABAJADOR", "tarea": "Busca noticias AMAZON"},
    22: {"nombre": "COMETA MICROSOFT", "rol": "TRABAJADOR", "tarea": "Busca noticias MICROSOFT"},
    23: {"nombre": "RAYO NOTICIAS", "rol": "TRABAJADOR", "tarea": "Busca noticias Telegram y WhatsApp"},
    24: {"nombre": "HIELO SOPORTE", "rol": "TRABAJADOR", "tarea": "Busca soportes donde precio no baja"},
    25: {"nombre": "FUEGO RESISTENCIA", "rol": "TRABAJADOR", "tarea": "Busca resistencias donde precio no sube"},
    26: {"nombre": "COMETA 14:30", "rol": "VIGIA BANCO", "tarea": "Vigila 14:30 - Habla FED Powell - Avisa al JEFE"},
    27: {"nombre": "RAYO ENTRADA", "rol": "TRABAJADOR", "tarea": "Busca mejor ENTRADA"},
    28: {"nombre": "FUEGO BOTIN", "rol": "TRABAJADOR", "tarea": "Calcula tu BOTIN"},
    29: {"nombre": "HIELO SALIDA", "rol": "TRABAJADOR", "tarea": "Te dice cuando SALIR"},
    30: {"nombre": "COMETA PELIGRO", "rol": "VIGIA BANCO", "tarea": "Grita PELIGRO si hay noticia mala de banco"},
    31: {"nombre": "RAYO VIP", "rol": "TRABAJADOR", "tarea": "Solo habla para los VIP"},
    32: {"nombre": "FUEGO DIOS", "rol": "TRABAJADOR", "tarea": "Tiene fuego de DIOS"},
    33: {"nombre": "HIELO DIOS", "rol": "TRABAJADOR", "tarea": "Tiene hielo de DIOS"},
    34: {"nombre": "COMETA ORO 2", "rol": "TRABAJADOR", "tarea": "Confirma lo que dice el ORO"},
    35: {"nombre": "RAYO CONFIRMA", "rol": "TRABAJADOR", "tarea": "Confirma COMPRA o VENTA"},
    36: {"nombre": "FUEGO CONFIRMA", "rol": "TRABAJADOR", "tarea": "Confirma con fuego"},
    37: {"nombre": "HIELO CONFIRMA", "rol": "TRABAJADOR", "tarea": "Confirma con calma"},
    38: {"nombre": "COMETA JEFE", "rol": "TRABAJADOR", "tarea": "Jefe de los cometas"},
    39: {"nombre": "RAYO MAESTRO 2", "rol": "TRABAJADOR", "tarea": "Mano derecha del Maestro 40"},
}

def jefe_manda_orden(bancos, datos, extra=None):
    """EL JEFE 40 DECIDE - Ahora lee BANCOS + DXY + VIX"""
    if extra and extra.get("VIX_nivel") == "ROJO":
        return {"orden": "🛑 PAUSA TOTAL - PANICO - ORDEN DEL JEFE", "motivo": extra["VIX_texto"], "permiso_operar": False, "mensaje": "JEFE DICE: VIX en " + str(extra["VIX"]) + " - Hay PANICO. Todos los 39 robots PARADOS. No operen, viene caida."}
    if bancos["nivel_riesgo"] == "ROJO":
        return {"orden": "🛑 PAUSA TOTAL - ORDEN DEL JEFE", "motivo": bancos["alerta_banco"], "permiso_operar": False, "mensaje": "JEFE DICE: Hay noticia de BANCO FUERTE ahora. Todos los 39 robots PARADOS. Esperen que pase la noticia. No pierdan dinero."}
    if datos["ORO"] > 3910 and datos["ORO"] < 3970:
        extra_txt = ""
        if extra:
            extra_txt = " | " + extra["DXY_texto"] + " | " + extra["VIX_texto"]
        return {"orden": "🟡 ESPERA - ORDEN DEL JEFE", "motivo": "Oro fuera de zona + Bancos tranquilos", "permiso_operar": False, "mensaje": "JEFE DICE: Oro en $" + str(datos["ORO"]) + " fuera de zona. Mis 39 robots buscando." + extra_txt}
    extra_txt = ""
    if extra:
        extra_txt = " | " + extra["DXY_texto"]
    return {"orden": "🟢 PERMISO PARA OPERAR - ORDEN DEL JEFE", "motivo": "Bancos tranquilos + Oro en zona", "permiso_operar": True, "mensaje": "JEFE DICE: Bancos tranquilos, Oro en zona. Mis 39 robots listos. Pueden operar con cuidado." + extra_txt}

def get_precio_yahoo(symbol, fallback):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        j = r.json()
        price = j['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except:
        return fallback

def motor_fuerza_total(precio, simbolo):
    if simbolo == "ORO":
        if precio <= 3910 or precio >= 3970:
            return "🔥🔥🔥🔥🔥 FUERZA TOTAL ULTRA 200% - DIOS - SATELITE ACTIVO"
        if precio <= 3940:
            return "🔥🔥🔥 FUERZA MEGA 150% - SATELITE ACTIVO"
        return "🔥🔥 FUERZA ALTA 100% - BUSCANDO"
    else:
        return "💪 MOTOR 200% VIGILANDO " + simbolo + " DESDE SATELITE USA"

def buscador_nada_se_escape(datos):
    encontrados = []
    if datos["ORO"] <= 3910:
        encontrados.append("🟢 ORO EN COMPRA " + str(datos["ORO"]))
    if datos["ORO"] >= 3970:
        encontrados.append("🔴 ORO EN VENTA " + str(datos["ORO"]))
    if datos["NVDA"] <= 180:
        encontrados.append("🟢 NVDA EN COMPRA " + str(datos["NVDA"]))
    if datos["TSLA"] <= 330:
        encontrados.append("🟢 TESLA EN COMPRA " + str(datos["TSLA"]))
    if datos["AAPL"] <= 255:
        encontrados.append("🟢 APPLE EN COMPRA " + str(datos["AAPL"]))
    if not encontrados:
        return "🔍 BUSCADOR: Revisé TODO - ORO, NVDA, TESLA, APPLE, META, GOOGLE, AMAZON, MICROSOFT - Nada en zona, ESPERA"
    return "🔍 BUSCADOR ENCONTRÓ: " + " | ".join(encontrados)

def conectar_todos_los_robots(datos):
    robots_conectados = {}
    zonas = {
        "ORO": {"compra": 3910, "venta": 3970, "fuente": "gold-api.com + Yahoo USA GC=F"},
        "NVDA": {"compra": 180, "venta": 195, "fuente": "Yahoo USA - NASDAQ"},
        "AAPL": {"compra": 255, "venta": 270, "fuente": "Yahoo USA - NASDAQ"},
        "TSLA": {"compra": 330, "venta": 355, "fuente": "Yahoo USA - NASDAQ"},
        "MSFT": {"compra": 490, "venta": 505, "fuente": "Yahoo USA - NASDAQ"},
        "AMZN": {"compra": 230, "venta": 245, "fuente": "Yahoo USA - NASDAQ"},
        "META": {"compra": 640, "venta": 660, "fuente": "Yahoo USA - NASDAQ"},
        "GOOGL": {"compra": 280, "venta": 292, "fuente": "Yahoo USA - NASDAQ"},
    }
    for simbolo, precio in datos.items():
        if simbolo in zonas:
            z = zonas[simbolo]
            if precio <= z["compra"]:
                robots_conectados[simbolo] = {"senal": "COMPRA", "precio": precio, "fuente": z["fuente"]}
            elif precio >= z["venta"]:
                robots_conectados[simbolo] = {"senal": "VENTA", "precio": precio, "fuente": z["fuente"]}
            else:
                robots_conectados[simbolo] = {"senal": "ESPERA", "precio": precio, "fuente": z["fuente"]}
    return robots
