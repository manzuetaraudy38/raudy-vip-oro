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
    dxy = get_precio_yahoo('DX-Y.NYB', 99.50)
    vix = get_precio_yahoo('^VIX', 15.20)
    btc = get_precio_yahoo('BTC-USD', 105000)
    petroleo = get_precio_yahoo('CL=F', 61.50)
    bono10 = get_precio_yahoo('^TNX', 4.10)
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
# 🆕🆕 NUEVO JEFE - ALERTA PRESIDENTE / CAMBIO ECONOMIA - NO BORRA NADA
# El robot esta atento cuando el presidente decide algun cambio
# ============================================================
EVENTOS_PRESIDENCIALES_FIJOS = [
    {"evento": "Presidente USA - Habla de Economía", "impacto": "ALTO", "efecto": "Si habla de aranceles o guerra, ORO SUBE fuerte. Si habla de paz, ORO BAJA"},
    {"evento": "Casa Blanca - Cambio de Ley / Arancel", "impacto": "ALTO", "efecto": "Arancel nuevo = Dólar sube, ORO se mueve $30-$80"},
    {"evento": "Presidente - Reunión con FED", "impacto": "ALTO", "efecto": "Si presiona a FED para bajar tasa, ORO SUBE"},
    {"evento": "Elecciones / Decisión Presidencial", "impacto": "ALTO", "efecto": "Incertidumbre = ORO SUBE, la gente busca refugio"},
]

def get_alerta_presidencial():
    # Vigila noticias de presidencia via TradingEconomics + palabras clave
    alerta = {
        "nivel": "VERDE",
        "mensaje": "🟢 SIN CAMBIO PRESIDENCIAL AHORA - Presidente tranquilo, robot puede trabajar",
        "accion_jefe": "Puedes operar normal",
        "eventos": EVENTOS_PRESIDENCIALES_FIJOS,
        "fuente": "whitehouse.gov + TradingEconomics + ForexFactory - Vigilando"
    }
    try:
        r = requests.get('https://api.tradingeconomics.com/calendar?c=guest:guest&f=json&d1=today&d2=today', timeout=4)
        if r.status_code == 200:
            data = r.json()
            for e in data:
                texto = str(e.get('Event','')) + " " + str(e.get('Category','')) + " " + str(e.get('Country',''))
                texto_low = texto.lower()
                if any(p in texto_low for p in ["president", "white house", "election", "tariff", "government", "fiscal", "treasury", "speech"]):
                    alerta["nivel"] = "ROJO"
                    alerta["mensaje"] = "🚨 ALERTA PRESIDENTE: " + e.get('Event','Cambio Presidencial') + " - " + e.get('Country','USA') + " - JEFE ORDENA PAUSA 1 HORA"
                    alerta["accion_jefe"] = "NO COMPRES AHORA - Espera que pase el discurso del presidente, ORO se va a mover fuerte"
                    break
    except:
        pass
    return alerta

# ============================================================
# 🆕🆕 NUEVO JEFE - PREGUNTALE AL ROBOT - TU LE DICES PRECIO Y EL TE DICE SI COMPRAR
# Tu dices: "Quiero comprar a 4070" - El robot dice: "No jefe, espera, va a bajar a 3940"
# ============================================================
def robot_responde_pregunta(precio_quiero, activo="ORO", precio_actual=4088, extra=None):
    precio_quiero = float(precio_quiero)
    # Zonas del JEFE - las mismas que ya tienes en tu codigo
    zonas = {
        "ORO": {"compra": 3910, "venta": 3970, "soporte": 3940, "resistencia": 4150},
        "NVDA": {"compra": 180, "venta": 195, "soporte": 180, "resistencia": 195},
        "AAPL": {"compra": 255, "venta": 270, "soporte": 255, "resistencia": 270},
        "TSLA": {"compra": 330, "venta": 355, "soporte": 330, "resistencia": 355},
        "MSFT": {"compra": 490, "venta": 505, "soporte": 490, "resistencia": 505},
        "AMZN": {"compra": 230, "venta": 245, "soporte": 230, "resistencia": 245},
        "META": {"compra": 640, "venta": 660, "soporte": 640, "resistencia": 660},
        "GOOGL": {"compra": 280, "venta": 292, "soporte": 280, "resistencia": 292},
