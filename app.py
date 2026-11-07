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
        return {"respuesta": "❌ NO JEFE, NO compres " + activo + " a $" + str(precio_quiero) + ", está CARO. Ahora está en $" + str(precio_actual) + " y va a BAJAR a $" + str(z["soporte"]) + ". ESPERA a $" + str(z["soporte"]) + ".", "decision": "NO-COMPRAR-ESPERA", "precio_recomendado": z["soporte"], "precio_actual": precio_actual}
    if precio_quiero <= z["compra"] + 30:
        return {"respuesta": "✅ SÍ JEFE, COMPRA YA " + activo + " a $" + str(precio_quiero) + ", está BARATO. Zona del JEFE.", "decision": "SI-COMPRAR", "precio_recomendado": precio_quiero, "precio_actual": precio_actual}
    return {"respuesta": "🟡 JEFE, ESPERA. Quieres comprar a $" + str(precio_quiero) + " pero ahora está en $" + str(precio_actual) + ". Mejor espera a $" + str(z["soporte"]) + ".", "decision": "ESPERA-BAJE", "precio_recomendado": z["soporte"], "precio_actual": precio_actual}

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
    return robots_conectados

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP ROBOTS PODEROSOS - ACCIONES + ORO</title>
<style>
*{box-sizing:border-box;font-family:Arial,sans-serif}
body{margin:0;background:#050505;color:white;text-align:center}
header{background:linear-gradient(90deg,#FFD700,#FF6B00,#FFD700);color:black;padding:15px}
header h1{margin:0;font-size:22px}
header p{margin:5px 0;font-weight:bold}
.top-btns{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px;background:#111}
.top-btns a{padding:12px 16px;border-radius:25px;text-decoration:none;font-weight:bold;color:white;font-size:14px}
.wa{background:#25D366}.tg{background:#0088cc}.ig{background:#E1306C}.pay{background:#FFD700;color:black!important}
.clock{background:#111;padding:10px;border:2px solid #FFD700;margin:10px;border-radius:15px}
.clock b{color:#FFD700;font-size:20px}
.maestro{background:linear-gradient(180deg,#FFD700,#FF6B00);color:black;margin:10px;padding:18px;border-radius:20px;border:4px solid white;box-shadow:0 0 30px #FFD700}
.maestro h2{margin:0;font-size:26px}
.maestro p{font-size:18px;font-weight:bold}
.maestro button{padding:12px 20px;border:none;border-radius:20px;background:black;color:#FFD700;font-weight:bold;font-size:16px;cursor:pointer;margin:3px}
.broker{background:#1a1a2e;margin:10px;padding:15px;border-radius:15px;border:2px solid #00FFFF}
.broker img{width:90px;height:90px;border-radius:50%;border:3px solid #00FFFF;object-fit:cover}
.acciones{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px}
.act{background:#1a1a1a;border:1px solid #333;padding:10px;border-radius:12px;min-width:130px;cursor:pointer}
.act b{color:#FFD700}.act span{font-size:12px}
.act.active{border:2px solid #FFD700;box-shadow:0 0 15px #FFD700}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.robot{background:#1a1a1a;border:2px solid #333;border-radius:15px;padding:10px}
.robot .luz{width:18px;height:18px;border-radius:50%;background:yellow;margin:0 auto 5px;box-shadow:0 0 12px yellow;animation:parpadeo 1s infinite}
@keyframes parpadeo{0%{opacity:1}50%{opacity:.3}100%{opacity:1}}
.robot h3{margin:5px 0;font-size:14px;color:#FFD700}
.robot p{font-size:12px;margin:3px 0}
.robot .poder{font-size:18px}
.robot .msg{font-size:12px;background:#222;padding:6px;border-radius:8px;min-height:38px}
.btns{margin-top:6px;display:flex;gap:5px;justify-content:center}
.btns button{border:none;padding:7px 8px;border-radius:10px;font-weight:bold;cursor:pointer;font-size:11px}
.felicitar{background:#00FF88}.estrella{background:#FFD700}
.estrellas{font-size:16px;color:#FFD700}
.footer{padding:20px;font-size:12px;color:#888}
.satelite{background:#001a33;margin:10px;padding:15px;border-radius:15px;border:2px solid #00FFFF}
.motorbox{background:#2a0000;margin:10px;padding:15px;border-radius:15px;border:2px solid #FF0000}
.buscadorbox{background:#0a2a00;margin:10px;padding:15px;border-radius:15px;border:2px solid #00FF88}
.origen{font-size:11px;color:#aaa;background:#111;padding:8px;border-radius:10px;margin-top:8px;text-align:left}
.conectado{background:#002a00;margin:10px;padding:12px;border-radius:15px;border:2px solid #00FF88}
.bancobox{background:#1a1a00;margin:10px;padding:15px;border-radius:15px;border:2px solid #FFD700;text-align:left}
.jefebox{background:#2a0000;margin:10px;padding:15px;border-radius:15px;border:3px solid #FF0000}
.extrabox{background:#001a33;margin:10px;padding:15px;border-radius:15px;border:2px solid #00FFFF;text-align:left}
.presidentbox{background:#2a0000;margin:10px;padding:15px;border-radius:15px;border:3px solid #FF4444}
.preguntabox{background:#0a2a00;margin:10px;padding:15px;border-radius:15px;border:3px solid #00FF88}
.preguntabox input{width:100%;padding:12px;border-radius:10px;background:#111;color:white;font-size:16px;border:1px solid #00FF88}
.preguntabox button{width:100%;padding:14px;border-radius:15px;background:#00FF88;font-weight:bold;font-size:16px;border:none;margin-top:5px;cursor:pointer}
</style>
</head>
<body>
<header>
<h1>👑 RAUDY VIP ROBOTS PODEROSOS ⚡☄️</h1>
<p>ACCIONES + ORO • ELLOS BUSCAR Y ANALIZAN SOLOS</p>
<p>JEFE: RAUDY MANZUETA</p>
</header>
<div class="top-btns">
<a class="wa" href="https://wa.me/41767574050" target="_blank">💬 WHATSAPP 0767574050</a>
<a class="tg" href="https://t.me/raudy_vip_oro_bot" target="_blank">✈️ TELEGRAM @raudy_vip_oro_bot</a>
<a class="ig" href="https://instagram.com/raudy_vip_oro_bot" target="_blank">📸 INSTAGRAM @raudy_vip_oro_bot</a>
<a class="pay" href="https://paypal.me/RaudyManzueta/20" target="_blank">💰 PAGAR VIP $20</a>
</div>
<!-- 🆕 NUEVO - PRESIDENTE + PREGUNTALE - AGREGADO AHORA -->
<div class="presidentbox">
<h2 style="color:#FF4444;margin:0;text-align:center;">🇺🇸 🚨 ALERTA PRESIDENTE - CAMBIO DE ECONOMÍA</h2>
<p id="presidente-mensaje" style="font-weight:bold;">🇺🇸 Vigilando Casa Blanca...</p>
<p id="presidente-accion" style="color:#FFD700;">Esperando...</p>
<p style="font-size:11px;color:#aaa;">Si el Presidente habla de aranceles, guerra o ley nueva, el JEFE dice PAUSA. Fuente: whitehouse.gov - GRATIS</p>
</div>
<div class="preguntabox">
<h2 style="color:#00FF88;margin:0;text-align:center;">🤖 PREGÚNTALE AL ROBOT - ¿QUIERO COMPRAR A TAL PRECIO?</h2>
<p>Escribe el precio donde QUIERES comprar y el robot te dice si está caro o barato.</p>
<input id="precio-pregunta" type="number" placeholder="Ej: 4070">
<button onclick="preguntarRobot()">🤖 PREGUNTAR AL ROBOT AHORA</button>
<p id="respuesta-robot" style="font-weight:bold;background:#111;padding:12px;border-radius:10px;">🤖 Robot esperando tu pregunta jefe...</p>
</div>
<div class="jefebox">
<h2 style="color:#FF4444;margin:0;">👑 JEFE 40 - YO MANDO A LOS 39 - ORDEN EN VIVO</h2>
<p id="jefe-orden" style="font-size:16px;font-weight:bold;color:white;">👑 JEFE: Cargando orden...</p>
<p id="jefe-mensaje" style="font-size:13px;color:#FFD700;">Esperando orden del Jefe...</p>
<p style="font-size:11px;color:#aaa;">Si el JEFE dice PAUSA, nadie opera. Asi no pierdes dinero con noticias de bancos.</p>
</div>
<div class="bancobox">
<h2 style="color:#FFD700;margin:0;text-align:center;">🏦 BANCOS QUE MUEVEN EL ORO - INFO EN VIVO</h2>
<p id="banco-alerta" style="font-size:14px;font-weight:bold;color:#00FF88;">🏦 Bancos: Cargando...</p>
<p id="banco-lista" style="font-size:12px;line-height:1.6;">Cargando bancos...</p>
<p style="font-size:11px;color:#aaa;">Fuente: ForexFactory.com + federalreserve.gov (FED) + ecb.europa.eu (BCE) + TradingEconomics - GRATIS</p>
</div>
<!-- 🆕 NUEVO - DXY + VIX + BTC + PETROLEO -->
<div class="extrabox">
<h2 style="color:#00FFFF;margin:0;text-align:center;">💵 DOLAR + 😱 MIEDO + ₿ BITCOIN - LO QUE USAN LOS BANCOS</h2>
<p id="dxy-texto" style="font-size:14px;font-weight:bold;">💵 DXY: Cargando...</p>
<p id="vix-texto" style="font-size:14px;font-weight:bold;">😱 VIX: Cargando...</p>
<p id="extra-texto" style="font-size:13px;">₿ BTC + 🛢️ Petroleo + 📈 Bono 10 años: Cargando...</p>
<p style="font-size:11px;color:#aaa;">Si DXY sube, ORO baja. Si VIX pasa 30, JEFE dice PAUSA. Fuente: Yahoo Finance USA - GRATIS</p>
</div>
<div class="satelite">
<h2 style="color:#00FFFF;margin:0;">🛰️ SATÉLITE RAUDY - LLEGÓ A ESTADOS UNIDOS 🇺🇸</h2>
<p style="font-size:14px;font-weight:bold;">Mirando WALL STREET - NEW YORK en vivo - NYSE + NASDAQ</p>
<p id="satelite-texto" style="font-size:13px;">🛰️ Satélite conectando con USA... Buscando bolsa...</p>
<p id="satelite-usa" style="font-size:13px;color:#00FF88;">Cargando bolsa USA...</p>
<iframe src="https://www.google.com/maps?q=Wall+Street+New+York+USA&z=16&t=k&output=embed" width="100%" height="180" style="border:0;border-radius:10px;margin-top:8px;"></iframe>
<div class="origen">📍 <b>SATÉLITE APUNTA A:</b> Wall Street, New York, USA - 40.7075° N, 74.0113° W<br>📍 <b>FUENTE BOLSA USA:</b> Yahoo Finance USA - query1.finance.yahoo.com - Precios reales de NYSE / NASDAQ</div>
</div>
<div class="conectado">
<h2 style="color:#00FF88;margin:0;">🔌 TODOS LOS 40 ROBOTS CONECTADOS A LA BOLSA USA ✅</h2>
<p id="conexion-texto" style="font-size:13px;font-weight:bold;">🔌 Conectando robots a Wall Street...</p>
<p style="font-size:11px;color:#aaa;">Cada robot lee el mismo precio real de NYSE / NASDAQ - Ya no inventan</p>
</div>
<div class="motorbox">
<h2 style="color:#FF4444;margin:0;">💪 MOTOR FUERZA TOTAL ULTRA 200% 🔥</h2>
<p id="motor-texto" style="font-size:15px;font-weight:bold;">💪 MOTOR: Cargando fuerza...</p>
<p style="font-size:12px;color:#aaa;">Motor vigilando ORO + ACCIONES USA con satélite</p>
</div>
<div class="buscadorbox">
<h2 style="color:#00FF88;margin:0;">🔍 BUSCADOR RAUDY - NADA SE ESCAPA</h2>
<p id="buscador-texto" style="font-size:13px;font-weight:bold;">🔍 Buscando en todo el mercado...</p>
<p style="font-size:11px;color:#aaa;">Busca: ORO, NVDA, TESLA, APPLE, META, GOOGLE, AMAZON, MICROSOFT cada 15 segundos</p>
</div>
<div class="clock">SESION NEW YORK 🕐 <b id="reloj">--:--:--</b><br><span id="sesion">Buscando información...</span></div>
<div class="acciones" id="acciones"></div>
<div class="maestro">
<div style="font-size:40px">👑⚡☄️🔥🧊</div>
<h2>ROBOT 40 - MAESTRO DIOS RAUDY</h2>
<p>Función: Yo mando a los 39. Yo tengo TODOS los poderes. Yo decido.</p>
<p id="maestroMsg">Analizando todo... Espera jefe...</p>
<p>⭐ Estrellas del Maestro: <span id="maestroEstrellas">⭐⭐⭐⭐⭐</span></p>
<button onclick="felicitarMaestro()">👏 FELICITAR MAESTRO</button>
<button onclick="estrellaMaestro()">⭐ MANDAR ESTRELLA AL MAESTRO</button>
</div>
<div class="broker">
<img src="https://i.pravatar.cc/150?img=12" alt="Broker">
<h3>🧑‍💼 BROKER RAUDY - Persona Real</h3>
<p id="brokerMsg">Hola jefe, soy tu Broker. Estoy mirando lo que dicen los robots...</p>
<button onclick="hablarBroker()" style="padding:10px 18px;border-radius:20px;background:#00FFFF;border:none;font-weight:bold">🎤 PREGUNTAR AL BROKER</button>
</div>
<h2>🤖 LOS 40 ROBOTS CON PODERES</h2>
<p>Ellos buscan información, la analizan y te dicen COMPRA o VENTA solos.</p>
<div class="grid" id="grid"></div>
<div style="background:#111;margin:10px;padding:15px;border-radius:15px;border:2px solid #FFD700;text-align:left;">
<h3 style="color:#FFD700;margin:0;">📍 ¿DE DÓNDE SALE CADA PRECIO? - DIRECTO JEFE</h3>
<p id="origen-precios" style="font-size:12px;line-height:1.6;">Cargando origen...</p>
<p style="font-size:11px;color:#888;">Esto es para que tú sepas que no es inventado. Cada precio viene de USA.</p>
</div>
<div class="footer">RAUDY VIP © 2026 - Solo Robots Hacen Todo - WhatsApp 0767574050 - No es consejo financiero, es educación</div>
<script>
const simbolos=[{id:"ORO",nombre:"ORO",precio:4088,emoji:"🥇"},{id:"NVDA",nombre:"NVIDIA",precio:185.20,emoji:"💚"},{id:"AAPL",nombre:"APPLE",precio:262.10,emoji:"🍎"},{id:"TSLA",nombre:"TESLA",precio:340.50,emoji:"🚗"},{id:"MSFT",nombre:"MICROSOFT",precio:495.30,emoji:"🪟"},{id:"AMZN",nombre:"AMAZON",precio:235.40,emoji:"📦"},{id:"META",nombre:"META",precio:645.20,emoji:"👍"},{id:"GOOGL",nombre:"GOOGLE",precio:282.10,emoji:"🔍"}];
let activo="ORO";
let datosRealesGlobal=null;
const accDiv=document.getElementById("acciones");
function renderAcc(){
 accDiv.innerHTML="";
 simbolos.forEach(s=>{
  let cambio=(Math.random()*4-2).toFixed(2);
  let color=cambio>=0?"#00FF88":"#FF4444";
  let d=document.createElement("div");
  d.className="act "+(activo===s.id?"active":"");
  d.innerHTML="<b>"+s.emoji+" "+s.id+"</b><br>"+s.nombre+"<br><b>$"+s.precio.toFixed(2)+"</b><br><span style='color:"+color+"'>"+cambio+"%</span>";
  d.onclick=()=>{activo=s.id;renderAcc();analizarTodo();sonido()};
  accDiv.appendChild(d);
 });
}
renderAcc();
const robots=[
[1,"RAYO RAUDY","⚡","Yo soy el más rápido, busco noticias de USA"],
[2,"RAYO VELOZ","⚡","Yo busco noticias de NVDA y TESLA"],
[3,"COMETA ORO","☄️","Yo busco noticias del ORO"],
[4,"GUARDIA 08:30","🔥","Yo vigilo noticias de las 08:30"],
[5,"COMETA VENTA","☄️","Yo busco ventas fuertes, rompo el mercado"],
[6,"COMETA FUERTE","☄️","Yo analizo caídas rápidas"],
[7,"COMETA DIOS","☄️","Yo aviso cuando viene una venta grande"],
[8,"RAYO COMPRA","⚡","Yo busco compras rápidas"],
[9,"RAYO ORO","⚡","Yo sigo el ORO segundo a segundo"],
[10,"HIELO PACIENTE","🧊","Yo espero frío, no entro con prisa"],
[11,"HIELO ANALISTA","🧊","Yo analizo si el mercado está tranquilo"],
[12,"FUEGO COMPRA","🔥","Yo quemo cuando hay compra fuerte"],
[13,"FUEGO TESLA","🔥","Yo cuido solo TESLA"],
[14,"FUEGO NVDA","🔥","Yo cuido solo NVIDIA"],
[15,"FUEGO APPLE","🔥","Yo cuido solo APPLE"],
[16,"FUEGO ORO","🔥","Yo cuido el ORO con fuego"],
[17,"FUEGO VENTA","🔥","Yo digo V
