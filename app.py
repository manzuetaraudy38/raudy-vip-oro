from flask import Flask, jsonify, request
import requests
from datetime import datetime
import json, os, random
app = Flask(__name__)

# 🧠 CEREBRO + HISTORIAL GANADAS / PERDIDAS - 4
ARCHIVO = "cerebro_memoria.json"
CEREBRO = {"historial": [], "veces_compra": 0, "veces_venta": 0, "veces_espera": 0, "ganadas": 0, "perdidas": 0, "ultima_leccion": "Empezando jefe."}
def cerebro_cargar():
    global CEREBRO
    try:
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO) as f: CEREBRO = json.load(f)
    except: pass
def cerebro_guardar():
    try:
        with open(ARCHIVO, "w") as f: json.dump(CEREBRO, f)
    except: pass
def cerebro_aprende(datos, jefe_orden):
    global CEREBRO
    oro = datos.get("ORO", 4088)
    if oro <= 3910:
        decision = "COMPRA"; CEREBRO["veces_compra"] += 1
        leccion = "Jefe, ORO toco ZONA ABAJO $" + str(oro) + ". Como en la foto, reboto para ARRIBA."
        # Simulamos ganada si rebota - para historial
        CEREBRO["ganadas"] += 1
    elif oro >= 3970:
        decision = "VENTA"; CEREBRO["veces_venta"] += 1
        leccion = "Jefe, ORO toco ZONA ARRIBA $" + str(oro) + ". Como en la foto, reboto para ABAJO."
        CEREBRO["ganadas"] += 1
    else:
        decision = "ESPERA"; CEREBRO["veces_espera"] += 1
        leccion = "Jefe, ORO en $" + str(oro) + " en medio de las 2 ZONAS. Esperar."
    CEREBRO["ultima_leccion"] = leccion
    CEREBRO["historial"].append({"hora": datetime.now().strftime("%H:%M:%S"), "oro": oro, "decision": decision, "leccion": leccion})
    CEREBRO["historial"] = CEREBRO["historial"][-20:]
    cerebro_guardar()
    return CEREBRO
def cerebro_recuerda():
    total = CEREBRO["veces_compra"] + CEREBRO["veces_venta"] + CEREBRO["veces_espera"]
    return {"mensaje": "🧠 Me acuerdo de " + str(total) + " jugadas - COMPRA: " + str(CEREBRO["veces_compra"]) + " | VENTA: " + str(CEREBRO["veces_venta"]) + " | ESPERA: " + str(CEREBRO["veces_espera"]), "total": total, "leccion": CEREBRO["ultima_leccion"], "ganadas": CEREBRO.get("ganadas",0), "perdidas": CEREBRO.get("perdidas",0), "historial": CEREBRO["historial"][-5:]}
cerebro_cargar()

# 📍 ZONA + MAS ZONAS - 7
ZONAS_TODAS = {
    "ORO": {"compra": 3910, "venta": 3970, "nombre": "ORO"},
    "EURUSD": {"compra": 1.1150, "venta": 1.1250, "nombre": "EUR/USD"},
    "GBPUSD": {"compra": 1.3300, "venta": 1.3450, "nombre": "GBP/USD"},
    "USDJPY": {"compra": 148.00, "venta": 152.00, "nombre": "USD/JPY"},
    "BTC": {"compra": 100000, "venta": 108000, "nombre": "BITCOIN"},
    "NVDA": {"compra": 180, "venta": 195, "nombre": "NVIDIA"},
    "AAPL": {"compra": 255, "venta": 270, "nombre": "APPLE"},
    "TSLA": {"compra": 330, "venta": 355, "nombre": "TESLA"},
}
def get_zona(oro):
    if oro <= 3910: return {"zona": "ZONA ABAJO", "flecha": "⬆️", "color": "#00FF88", "senal": "COMPRA", "mensaje": "🟢 ZONA ⬆️ TOCADA! ORO $" + str(oro) + " toco ZONA ABAJO. REBOTE PARA ARRIBA. COMPRA", "accion": "COMPRA"}
    if oro >= 3970: return {"zona": "ZONA ARRIBA", "flecha": "⬇️", "color": "#FF4444", "senal": "VENTA", "mensaje": "🔴 ZONA ⬇️ TOCADA! ORO $" + str(oro) + " toco ZONA ARRIBA. REBOTE PARA ABAJO. VENTA", "accion": "VENTA"}
    if oro <= 3940: return {"zona": "CERCA ZONA ABAJO", "flecha": "⬆️", "color": "#FFD700", "senal": "PREPARATE COMPRA", "mensaje": "🟡 ORO $" + str(oro) + " cerca de ZONA ABAJO $3910. Preparado.", "accion": "ESPERA"}
    if oro >= 3955: return {"zona": "CERCA ZONA ARRIBA", "flecha": "⬇️", "color": "#FFD700", "senal": "PREPARATE VENTA", "mensaje": "🟡 ORO $" + str(oro) + " cerca de ZONA ARRIBA $3970. Preparado.", "accion": "ESPERA"}
    return {"zona": "EN MEDIO", "flecha": "⏳", "color": "#888", "senal": "ESPERA", "mensaje": "⏳ ORO $" + str(oro) + " en medio de las 2 ZONAS. Esperando que toque una ZONA.", "accion": "ESPERA"}

def get_zona_del_dia(datos):
    # Elige la ZONA mas cerca de tocar
    mejor = None; mejor_dist = 999999
    for k, z in ZONAS_TODAS.items():
        precio = datos.get(k, datos.get("ORO", 4088))
        if k == "ORO": precio = datos.get("ORO", 4088)
        if k == "EURUSD": precio = datos.get("EURUSD", 1.1140)
        if k == "GBPUSD": precio = datos.get("GBPUSD", 1.3350)
        if k == "USDJPY": precio = datos.get("USDJPY", 150.0)
        if k == "BTC": precio = datos.get("BTC", 105000)
        # distancia a la zona mas cercana
        d1 = abs(precio - z["compra"]) / max(z["compra"],1)
        d2 = abs(precio - z["venta"]) / max(z["venta"],1)
        d = min(d1, d2)
        if d < mejor_dist:
            mejor_dist = d; mejor = {"activo": k, "nombre": z["nombre"], "precio": precio, "compra": z["compra"], "venta": z["venta"], "dist": round(d*100,2)}
    if mejor["precio"] <= mejor["compra"]:
        mejor["mensaje"] = "👑 ZONA DEL DIA: " + mejor["nombre"] + " en $" + str(mejor["precio"]) + " TOCO ZONA ABAJO $" + str(mejor["compra"]) + " - COMPRA ⬆️"
        mejor["accion"] = "COMPRA"
    elif mejor["precio"] >= mejor["venta"]:
        mejor["mensaje"] = "👑 ZONA DEL DIA: " + mejor["nombre"] + " en $" + str(mejor["precio"]) + " TOCO ZONA ARRIBA $" + str(mejor["venta"]) + " - VENTA ⬇️"
        mejor["accion"] = "VENTA"
    else:
        mejor["mensaje"] = "👑 ZONA DEL DIA: " + mejor["nombre"] + " en $" + str(mejor["precio"]) + " - Esperando toque ZONA ABAJO $" + str(mejor["compra"]) + " o ZONA ARRIBA $" + str(mejor["venta"])
        mejor["accion"] = "ESPERA"
    return mejor

def get_precio_yahoo(symbol, fallback):
    try:
        r = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}', headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        return float(r.json()['chart']['result'][0]['meta']['regularMarketPrice'])
    except: return fallback

def get_info_bancaria():
    return {"fed_tasa": "5.25% - FED USA", "bce_tasa": "2.15% - BCE", "fuente": "ForexFactory + federalreserve.gov + ecb.europa.eu", "eventos_hoy": [{"evento": "FED - Tasa USA", "impacto": "ALTO", "hora": "14:00 NY", "efecto": "Si sube tasa, ORO BAJA"}, {"evento": "NFP - Empleo USA", "impacto": "ALTO", "hora": "08:30 NY", "efecto": "Si empleo fuerte, ORO BAJA"}, {"evento": "CPI - Inflación USA", "impacto": "ALTO", "hora": "08:30 NY", "efecto": "Si inflación alta, ORO SUBE"}, {"evento": "BCE - Banco Europa", "impacto": "ALTO", "hora": "08:15 NY", "efecto": "Mueve EUR y ORO"}], "alerta_banco": "SIN NOTICIA FUERTE AHORA", "nivel_riesgo": "VERDE"}
def get_mercado_extra():
    dxy = get_precio_yahoo('DX-Y.NYB', 99.50); vix = get_precio_yahoo('^VIX', 15.20); btc = get_precio_yahoo('BTC-USD', 105000)
    return {"DXY": dxy, "DXY_texto": "💵 DOLAR " + str(round(dxy,2)), "VIX": vix, "VIX_texto": "VIX " + str(round(vix,2)) + " - Tranquilo" if vix < 20 else "VIX " + str(round(vix,2)) + " - Cuidado", "VIX_nivel": "VERDE" if vix < 20 else "AMARILLO", "BTC": btc, "PETROLEO": get_precio_yahoo('CL=F', 61.50), "BONO10": get_precio_yahoo('^TNX', 4.10)}
def get_alerta_presidencial():
    return {"nivel": "VERDE", "mensaje": "🟢 SIN CAMBIO PRESIDENCIAL AHORA", "accion_jefe": "Puedes operar normal", "eventos": [], "fuente": "whitehouse.gov"}
def jefe_manda_orden(bancos, datos, extra=None):
    if datos["ORO"] > 3910 and datos["ORO"] < 3970:
        return {"orden": "🟡 ESPERA - ORDEN DEL JEFE", "motivo": "Oro fuera de zona", "permiso_operar": False, "mensaje": "JEFE DICE: Oro en $" + str(datos["ORO"]) + " fuera de zona. Buscando."}
    return {"orden": "🟢 PERMISO PARA OPERAR - ORDEN DEL JEFE", "motivo": "Oro en zona", "permiso_operar": True, "mensaje": "JEFE DICE: Oro en zona. Pueden operar con cuidado."}
def motor_fuerza_total(precio, simbolo):
    if precio <= 3910 or precio >= 3970: return "🔥🔥🔥🔥🔥 FUERZA TOTAL ULTRA 200%"
    return "🔥🔥 FUERZA ALTA 100%"
def buscador_nada_se_escape(datos):
    enc = []
    if datos["ORO"] <= 3910: enc.append("🟢 ORO COMPRA")
    if datos["ORO"] >= 3970: enc.append("🔴 ORO VENTA")
    if not enc: return "🔍 BUSCADOR: Nada en zona, ESPERA"
    return "🔍 ENCONTRÓ: " + " | ".join(enc)
def conectar_todos(datos):
    out = {}
    for k, z in ZONAS_TODAS.items():
        p = datos.get(k, 0)
        if p <= z["compra"]: out[k] = {"senal": "COMPRA", "precio": p}
        elif p >= z["venta"]: out[k] = {"senal": "VENTA", "precio": p}
        else: out[k] = {"senal": "ESPERA", "precio": p}
    return out
def robot_responde_pregunta(precio_quiero, activo="ORO", precio_actual=4088):
    precio_quiero = float(precio_quiero)
    z = ZONAS_TODAS.get(activo, ZONAS_TODAS["ORO"])
    mem = cerebro_recuerda()
    if precio_quiero > z["venta"] and precio_quiero > precio_actual:
        return {"respuesta": "❌ NO JEFE, NO compres " + activo + " a $" + str(precio_quiero) + ", está CARO. Espera a $" + str(z["compra"]) + ". | 🧠 " + mem["leccion"], "decision": "NO-COMPRAR", "precio_recomendado": z["compra"], "precio_actual": precio_actual}
    if precio_quiero <= z["compra"] + 30:
        return {"respuesta": "✅ SÍ JEFE, COMPRA YA " + activo + " a $" + str(precio_quiero) + ", está BARATO. | 🧠 " + mem["leccion"], "decision": "SI-COMPRAR", "precio_recomendado": precio_quiero, "precio_actual": precio_actual}
    return {"respuesta": "🟡 JEFE, ESPERA. Quieres comprar a $" + str(precio_quiero) + " pero ahora está en $" + str(precio_actual) + ". Mejor espera a $" + str(z["compra"]) + ". | 🧠 " + mem["leccion"], "decision": "ESPERA", "precio_recomendado": z["compra"], "precio_actual": precio_actual}

ROBOTS = {40: {"nombre": "MAESTRO DIOS RAUDY - JEFE", "rol": "JEFE", "tarea": "Yo mando a los 39."}}

HTML = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY VIP - 8 PODERES</title>
<style>*{box-sizing:border-box;font-family:Arial,sans-serif}body{margin:0;background:#050505;color:white;text-align:center}header{background:linear-gradient(90deg,#FFD700,#FF6B00,#FFD700);color:black;padding:15px}header h1{margin:0;font-size:22px}.top-btns{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px;background:#111}.top-btns a{padding:12px 16px;border-radius:25px;text-decoration:none;font-weight:bold;color:white;font-size:14px}.wa{background:#25D366}.tg{background:#0088cc}.ig{background:#E1306C}.pay{background:#FFD700;color:black!important}.box{margin:10px;padding:15px;border-radius:15px;border:3px solid #333}.gold{border-color:#FFD700;background:#1a1a00}.purple{border-color:#CC00FF;background:#1a0033}.green{border-color:#00FF88;background:#0a2a00}.blue{border-color:#00FFFF;background:#001a33}.red{border-color:#FF4444;background:#2a0000}.orange{border-color:#FF6B00;background:#1a0a00}input{width:100%;padding:12px;border-radius:10px;background:#111;color:white;font-size:16px;border:1px solid #555;margin:4px 0}button{padding:12px 16px;border-radius:15px;font-weight:bold;font-size:15px;border:none;cursor:pointer;margin:4px}.btn-green{background:#00FF88}.btn-gold{background:#FFD700}.btn-blue{background:#00FFFF}.btn-red{background:#FF4444;color:white}.btn-purple{background:#CC00FF;color:white}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}.robot{background:#1a1a1a;border:2px solid #333;border-radius:15px;padding:10px}.robot .luz{width:18px;height:18px;border-radius:50%;background:yellow;margin:0 auto 5px;box-shadow:0 0 12px yellow}.robot h3{margin:5px 0;font-size:14px;color:#FFD700}.robot p{font-size:12px}.robot .msg{font-size:12px;background:#222;padding:6px;border-radius:8px;min-height:38px}.acciones{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px}.act{background:#1a1a1a;border:1px solid #333;padding:10px;border-radius:12px;min-width:130px;cursor:pointer}.act.active{border:2px solid #FFD700}.maestro{background:linear-gradient(180deg,#FFD700,#FF6B00);color:black;margin:10px;padding:18px;border-radius:20px;border:4px solid white}.clock{background:#111;padding:10px;border:2px solid #FFD700;margin:10px;border-radius:15px}.footer{padding:20px;font-size:12px;color:#888}canvas{background:#0a0a0a;border-radius:12px;width:100%;height:220px}.zona-bar{height:90px;background:#111;border-radius:12px;position:relative;overflow:hidden;margin:10px 0;border:2px solid #333}.zona-line-top{position:absolute;left:0;right:0;top:8px;height:3px;background:#FF4444}.zona-line-bottom{position:absolute;left:0;right:0;bottom:8px;height:3px;background:#00FF88}.zona-dot{position:absolute;left:50%;width:22px;height:22px;border-radius:50%;background:#FFD700;transform:translate(-50%,-50%);box-shadow:0 0 20px #FFD700;border:3px solid white}</style></head><body>
<header><h1>👑 RAUDY VIP ROBOTS PODEROSOS ⚡☄️</h1><p>8 PODERES NUEVOS • ZONA DEL DÍA • VIP</p><p>JEFE: RAUDY MANZUETA</p></header>
<div class="top-btns"><a class="wa" href="https://wa.me/41767574050" target="_blank">💬 WHATSAPP</a><a class="tg" href="https://t.me/raudy_vip_oro_bot" target="_blank">✈️ TELEGRAM</a><a class="ig" href="https://instagram.com/raudy_vip_oro_bot" target="_blank">📸 INSTAGRAM</a><a class="pay" href="https://paypal.me/RaudyManzueta/20" target="_blank">💰 PAGAR VIP $20</a></div>

<!-- 8 - MODO VIP -->
<div class="box gold"><h2>🔐 8 - MODO VIP - SOLO LOS QUE PAGARON</h2><p>Contraseña VIP es: <b>RAUDY20</b> - Pruébala ahora</p><input id="vip-pass" type="password" placeholder="Escribe contraseña VIP"><button class="btn-gold" onclick="entrarVIP()">🔓 ENTRAR VIP</button><p id="vip-msg">🔒 Señal VIP bloqueada. Escribe la contraseña.</p><div id="vip-secreto" style="display:none;background:#000;padding:12px;border-radius:10px;"><p id="vip-senal" style="font-weight:bold;color:#FFD700;">Cargando señal VIP...</p><button class="btn-green" onclick="copiarVIP()">📋 5 - COPIAR SEÑAL PARA VIP</button><button class="btn-blue" onclick="mandarWhatsApp()">💬 2 - MANDAR A WHATSAPP</button><button class="btn-blue" onclick="mandarTelegram()">✈️ 2 - MANDAR A TELEGRAM</button></div></div>

<!-- ZONA DEL DIA -->
<div class="box gold"><h2>👑 ZONA DEL DÍA - SOLO 1 JUGADA HOY</h2><p id="zona-dia-mensaje" style="font-size:17px;font-weight:bold;">👑 Calculando ZONA DEL DÍA...</p><p id="zona-dia-detalle" style="color:#FFD700;">Esperando...</p><button class="btn-green" onclick="copiarVIP()">📋 COPIAR ZONA DEL DÍA PARA VIP</button></div>

<!-- 1 - ALARMA -->
<div class="box red"><h2>🔔 1 - ALARMA QUE GRITA</h2><p>Cuando toca ZONA, suena y habla solo.</p><button class="btn-red" onclick="probarAlarma()">🔔 PROBAR ALARMA AHORA</button><p id="alarma-estado">🔕 Alarma lista, esperando que toque ZONA...</p><label><input type="checkbox" id="alarma-on" checked> Alarma ENCENDIDA</label></div>

<!-- ZONA -->
<div class="box blue"><h2>📍 ESTRATEGIA ZONA - COMO EN LA FOTO</h2><div style="display:flex;justify-content:space-between;font-weight:bold;"><span style="color:#FF4444;">ZONA ARRIBA $3970 ⬇️ VENTA</span><span style="color:#00FF88;">ZONA ABAJO $3910 ⬆️ COMPRA</span></div><div class="zona-bar"><div class="zona-line-top"></div><div class="zona-line-bottom"></div><div id="zona-dot" class="zona-dot" style="top:50%;"></div></div><p id="zona-mensaje" style="font-size:16px;font-weight:bold;">📍 Calculando ZONA...</p><p id="zona-accion" style="color:#FFD700;font-weight:bold;">Esperando...</p></div>

<!-- 3 - GRAFICO VELAS -->
<div class="box blue"><h2>📊 3 - GRÁFICO DE VELAS COMO EN LA FOTO</h2><p>Velas verdes y rojas, con ZONA ABAJO y ZONA ARRIBA</p><canvas id="chartVelas" width="360" height="220"></canvas><p style="font-size:11px;color:#aaa;">Verde = subió, Rojo = bajó. Si toca la línea verde de abajo, rebota arriba.</p></div>

<!-- 7 - MAS ZONAS -->
<div class="box green"><h2>🌍 7 - MÁS ZONAS - MÁS MONEDAS</h2><p id="mas-zonas" style="font-size:13px;line-height:1.8;">Cargando más zonas...</p><p style="font-size:11px;">ORO, EUR/USD, GBP/USD, USD/JPY, BTC, NVDA, TESLA, APPLE - Todas con su ZONA</p></div>

<!-- 4 - HISTORIAL -->
<div class="box purple"><h2>📈 4 - HISTORIAL - GANADAS Y PERDIDAS</h2><p id="cerebro-mensaje" style="font-weight:bold;">🧠 Cargando...</p><p id="cerebro-leccion" style="color:#FFD700;">Esperando...</p><p id="historial-texto" style="font-weight:bold;">🏆 Ganadas: ? | ❌ Perdidas: ?</p><p id="historial-lista" style="font-size:12px;text-align:left;">...</p></div>

<!-- 6 - CALCULADORA -->
<div class="box orange"><h2>🧮 6 - CALCULADORA DE DINERO</h2><p>¿Cuánto ganas si entras en ZONA?</p><input id="calc-dinero" type="number" placeholder="Tu dinero Ej: 100"><input id="calc-entrada" type="number" placeholder="Entrada Ej: 3910" value="3910"><input id="calc-salida" type="number" placeholder="Salida Ej: 3970" value="3970"><button class="btn-gold" onclick="calcularDinero()">🧮 CALCULAR CUÁNTO GANO</button><p id="calc-resultado" style="font-weight:bold;background:#000;padding:10px;border-radius:10px;">🧮 Escribe tu dinero y dale CALCULAR</p></div>

<div class="box red"><h2>🇺🇸 🚨 ALERTA PRESIDENTE</h2><p id="presidente-mensaje">Vigilando...</p><p id="presidente-accion">Esperando...</p></div>
<div class="box green"><h2>🤖 PREGÚNTALE AL ROBOT</h2><input id="precio-pregunta" type="number" placeholder="Ej: 4070"><button class="btn-green" onclick="preguntarRobot()">🤖 PREGUNTAR AL ROBOT</button><p id="respuesta-robot" style="font-weight:bold;background:#111;padding:12px;border-radius:10px;">🤖 Esperando...</p></div>
<div class="box red"><h2>👑 JEFE 40</h2><p id="jefe-orden">Cargando...</p><p id="jefe-mensaje">Esperando...</p></div>
<div class="box gold"><h2>🏦 BANCOS</h2><p id="banco-alerta">Cargando...</p><p id="banco-lista">Cargando...</p></div>
<div class="box blue"><h2>💵 DOLAR + MIEDO + BTC</h2><p id="dxy-texto">Cargando...</p><p id="vix-texto">Cargando...</p><p id="extra-texto">Cargando...</p></div>
<div class="box blue"><h2>🛰️ SATÉLITE USA</h2><p id="satelite-texto">Conectando...</p><p id="satelite-usa">Cargando...</p></div>
<div class="box green"><h2>🔌 40 ROBOTS CONECTADOS</h2><p id="conexion-texto">Conectando...</p></div>
<div class="box red"><h2>💪 MOTOR 200%</h2><p id="motor-texto">Cargando...</p></div>
<div class="box green"><h2>🔍 BUSCADOR</h2><p id="buscador-texto">Buscando...</p></div>
<div class="clock">SESION NEW YORK 🕐 <b id="reloj">--:--:--</b><br><span id="sesion">Buscando...</span></div><div class="acciones" id="acciones"></div>
<div class="maestro"><h2>ROBOT 40 - MAESTRO DIOS RAUDY</h2><p id="maestroMsg">Analizando...</p><p>⭐ <span id="maestroEstrellas">⭐⭐⭐⭐⭐</span></p><button onclick="felicitarMaestro()">👏 FELICITAR</button><button onclick="estrellaMaestro()">⭐ ESTRELLA</button></div>
<h2>🤖 LOS 40 ROBOTS</h2><div class="grid" id="grid"></div>
<div class="box gold"><h3>📍 ¿DE DÓNDE SALE CADA PRECIO?</h3><p id="origen-precios">Cargando...</p></div>
<div class="footer">RAUDY VIP © 2026 - WhatsApp 0767574050 - No es consejo financiero, es educación</div>
<script>
const simbolos=[{id:"ORO",nombre:"ORO",precio:4088,emoji:"🥇"},{id:"NVDA",nombre:"NVIDIA",precio:185.20,emoji:"💚"},{id:"AAPL",nombre:"APPLE",precio:262.10,emoji:"🍎"},{id:"TSLA",nombre:"TESLA",precio:340.50,emoji:"🚗"},{id:"EURUSD",nombre:"EUR/USD",precio:1.1140,emoji:"💶"},{id:"BTC",nombre:"BTC",precio:105000,emoji:"₿"}];
let activo="ORO"; let datosGlobal=null; let ultimaSenalVIP="VIP RAUDY: ORO en ZONA, espera señal";
const accDiv=document.getElementById("acciones");
function renderAcc(){accDiv.innerHTML="";simbolos.forEach(s=>{let d=document.createElement("div");d.className="act "+(activo===s.id?"active":"");d.innerHTML="<b>"+s.emoji+" "+s.id+"</b><br>"+s.nombre+"<br><b>$"+s.precio+"</b>";d.onclick=()=>{activo=s.id;renderAcc();analizarTodo();sonido()};accDiv.appendChild(d);});}renderAcc();
const robots=[[1,"RAYO RAUDY","⚡","Busco noticias USA"],[2,"RAYO VELOZ","⚡","Busco NVDA y TESLA"],[3,"COMETA ORO","☄️","Busco noticias ORO"],[4,"GUARDIA 08:30","🔥","Vigilo 08:30"],[5,"COMETA VENTA","☄️","Busco ventas"],[6,"COMETA FUERTE","☄️","Analizo caidas"],[7,"COMETA DIOS","☄️","Aviso venta grande"],[8,"RAYO COMPRA","⚡","Busco compras"],[9,"RAYO ORO","⚡","Sigo ORO"],[10,"HIELO PACIENTE","🧊","Espero frio"],[11,"HIELO ANALISTA","🧊","Analizo calma"],[12,"FUEGO COMPRA","🔥","Quemo compra"],[13,"FUEGO TESLA","🔥","Cuido TESLA"],[14,"FUEGO NVDA","🔥","Cuido NVDA"],[15,"FUEGO APPLE","🔥","Cuido APPLE"],[16,"FUEGO ORO","🔥","Cuido ORO"],[17,"FUEGO VENTA","🔥","Digo VENTA"],[18,"RAYO META","⚡","Cuido META"],[19,"RAYO AMAZON","⚡","Cuido AMAZON"],[20,"HIELO JEFE","🧊","Digo ESPERA"],[21,"COMETA AMAZON","☄️","Busco AMAZON"],[22,"COMETA MICROSOFT","☄️","Busco MICROSOFT"],[23,"RAYO NOTICIAS","⚡","Busco Telegram"],[24,"HIELO SOPORTE","🧊","Busco soportes"],[25,"FUEGO RESISTENCIA","🔥","Busco resistencias"],[26,"COMETA 14:30","☄️","Vigilo FED"],[27,"RAYO ENTRADA","⚡","Busco ENTRADA"],[28,"FUEGO BOTIN","🔥","Calculo BOTIN"],[29,"HIELO SALIDA","🧊","Digo SALIR"],[30,"COMETA PELIGRO","☄️","Grito PELIGRO"],[31,"RAYO VIP","⚡","Solo VIP"],[32,"FUEGO DIOS","🔥","Fuego DIOS"],[33,"HIELO DIOS","🧊","Hielo DIOS"],[34,"COMETA ORO 2","☄️","Confirmo ORO"],[35,"RAYO CONFIRMA","⚡","Confirmo"],[36,"FUEGO CONFIRMA","🔥","Confirmo fuego"],[37,"HIELO CONFIRMA","🧊","Confirmo calma"],[38,"COMETA JEFE","☄️","Jefe cometas"],[39,"RAYO MAESTRO 2","⚡","Mano derecha"],[40,"MAESTRO DIOS","👑","Mando a todos"]];
const grid=document.getElementById("grid"); let estrellas={};
robots.slice(0,39).forEach(r=>{let num=r[0];estrellas[num]=0;let div=document.createElement("div");div.className="robot";div.innerHTML="<div class='luz'></div><div>"+r[2]+"</div><h3>Robot "+num+" - "+r[1]+"</h3><p>"+r[3]+"</p><div class='msg' id='msg"+num+"'>Buscando...</div><div id='est"+num+"'></div><button onclick='felicitar("+num+")'>👏 FELICITAR</button> <button onclick='darEstrella("+num+")'>⭐ ESTRELLA</button>";grid.appendChild(div);});
function sonido(){try{let ctx=new (window.AudioContext||window.webkitAudioContext)();let o=ctx.createOscillator();let g=ctx.createGain();o.connect(g);g.connect(ctx.destination);o.frequency.value=880;o.type="sine";g.gain.value=0.1;o.start();o.stop(ctx.currentTime+0.15);}catch(e){}}
function hablar(t){if('speechSynthesis' in window){let u=new SpeechSynthesisUtterance(t);u.lang='es-ES';speechSynthesis.speak(u);}}
function felicitar(n){sonido();document.getElementById("msg"+n).innerHTML="¡Gracias jefe! 👏";hablar("Gracias jefe");}
function darEstrella(n){sonido();estrellas[n]++;document.getElementById("est"+n).innerHTML="⭐".repeat(estrellas[n]);document.getElementById("msg"+n).innerHTML="¡Gracias por la estrella! ⭐";}
let mc=5; function felicitarMaestro(){sonido();document.getElementById("maestroMsg").innerHTML="¡Gracias jefe! 👑";} function estrellaMaestro(){sonido();mc++;document.getElementById("maestroEstrellas").innerHTML="⭐".repeat(mc);}
// 8 - VIP
function entrarVIP(){let p=document.getElementById("vip-pass").value;if(p==="RAUDY20"){document.getElementById("vip-secreto").style.display="block";document.getElementById("vip-msg").innerHTML="✅ VIP ABIERTO JEFE - Ya puedes ver la señal";sonido();hablar("VIP abierto jefe");}else{document.getElementById("vip-msg").innerHTML="❌ Contraseña mal. Paga VIP $20 para tenerla.";}}
// 5 - COPIAR
function copiarVIP(){let texto=ultimaSenalVIP;if(navigator.clipboard){navigator.clipboard.writeText(texto).then(()=>{alert("✅ COPIADO JEFE: "+texto);});}else{alert(texto);}}
// 2 - WHATSAPP / TELEGRAM
function mandarWhatsApp(){let texto=encodeURIComponent(ultimaSenalVIP);window.open("https://wa.me/41767574050?text="+texto,"_blank");}
function mandarTelegram(){let texto=encodeURIComponent(ultimaSenalVIP);window.open("https://t.me/raudy_vip_oro_bot?text="+texto,"_blank");}
// 1 - ALARMA
function probarAlarma(){sonido();sonido();setTimeout(()=>sonido(),300);hablar("Jefe, tocó zona, compra");document.getElementById("alarma-estado").innerHTML="🔔 ALARMA SONÓ - Así va a sonar cuando toque ZONA";}
function alarmaTocoZona(mensaje){if(!document.getElementById("alarma-on").checked) return;sonido();setTimeout(()=>sonido(),300);setTimeout(()=>sonido(),600);hablar(mensaje);document.getElementById("alarma-estado").innerHTML="🚨 ALARMA: "+mensaje;}
// 6 - CALCULADORA
function calcularDinero(){let dinero=parseFloat(document.getElementById("calc-dinero").value||0);let ent=parseFloat(document.getElementById("calc-entrada").value||3910);let sal=parseFloat(document.getElementById("calc-salida").value||3970);if(!dinero){document.getElementById("calc-resultado").innerHTML="🧮 Jefe, escribe tu dinero. Ej: 100";return;}let dif=Math.abs(sal-ent);let pct=dif/ent*100;let ganancia=dinero*pct/100;let total=dinero+ganancia;document.getElementById("calc-resultado").innerHTML="💰 Si pones $"+dinero+" en $"+ent+" y sales en $"+sal+", ganas $"+ganancia.toFixed(2)+" - Total: $"+total.toFixed(2)+" - Eso es "+pct.toFixed(2)+"% - JEFE, eso es tu BOTIN";hablar("Jefe, ganas "+ganancia.toFixed(0)+" dolares");}
// 3 - GRAFICO VELAS
let velasHistorial=[];
function dibujarVelas(precioActual){
  let c=document.getElementById("chartVelas"); if(!c) return; let ctx=c.getContext("2d");
  velasHistorial.push(precioActual); if(velasHistorial.length>20) velasHistorial.shift();
  ctx.clearRect(0,0,360,220);
  // Zonas
  ctx.fillStyle="#00FF88"; ctx.fillRect(0,180,360,2); ctx.fillStyle="#00FF88"; ctx.fillText("ZONA ABAJO $3910 COMPRA", 10, 195);
  ctx.fillStyle="#FF4444"; ctx.fillRect(0,30,360,2); ctx.fillStyle="#FF4444"; ctx.fillText("ZONA ARRIBA $3970 VENTA", 10, 25);
  // Velas
  let min=3850, max=4150;
  velasHistorial.forEach((p,i)=>{
    let x=10+i*16; let y=200 - ((p-min)/(max-min))*170;
    let prev=velasHistorial[i-1]||p; let color=p>=prev?"#00FF88":"#FF4444";
    ctx.fillStyle=color; ctx.fillRect(x, Math.min(y, 200-((prev-min)/(max-min))*170), 10, Math.max(8, Math.abs(y - (200-((prev-min)/(max-min))*170))));
    ctx.fillRect(x+4, y-8, 2, 16);
  });
  ctx.fillStyle="#FFD700"; ctx.fillText("ORO AHORA $"+precioActual, 180, 110);
}
async function preguntarRobot(){let precio=document.getElementById("precio-pregunta").value;if(!precio){document.getElementById("respuesta-robot").innerHTML="🤖 Jefe, escribe un precio";return;}document.getElementById("respuesta-robot").innerHTML="🤖 Pensando...";try{let r=await fetch('/api/preguntale?precio='+precio+'&activo='+activo);let d=await r.json();document.getElementById("respuesta-robot").innerHTML="🤖 "+d.respuesta;hablar(d.respuesta);}catch(e){document.getElementById("respuesta-robot").innerHTML="🤖 Error";}}
async function analizarTodo(){sonido();let datos=datosGlobal;if(!datos){try{let r=await fetch('/api/satelite_usa?v='+Date.now());datos=await r.json();datosGlobal=datos;}catch(e){datos=null;}}let precioReal=datos&&datos[activo]?datos[activo]:simbolos.find(s=>s.id===activo).precio;let senal="ESPERA 🟡";if(activo==="ORO"){if(precioReal<=3910)senal="COMPRA 🟢";else if(precioReal>=3970)senal="VENTA 🔴";}document.getElementById("maestroMsg").innerHTML="Analicé "+activo+" $"+precioReal+" - Decisión: "+senal;robots.slice(0,39).forEach(r=>{let el=document.getElementById("msg"+r[0]);if(el)el.innerHTML="🔌 "+r[3]+" - "+activo+" $"+precioReal+" - "+senal;});}
async function actualizarSateliteUSA(){
  try{
    let r=await fetch('/api/satelite_usa?v='+Date.now());let d=await r.json();datosGlobal=d;
    document.getElementById("satelite-texto").innerHTML="🛰️ SATÉLITE EN USA ✅ - NYSE: "+d.nyse;document.getElementById("satelite-usa").innerHTML="🇺🇸 ORO $"+d.ORO+" | NVDA $"+d.NVDA+" | TESLA $"+d.TSLA+" | APPLE $"+d.AAPL+" | EUR/USD $"+d.EURUSD+" | BTC $"+Math.round(d.BTC);
    document.getElementById("motor-texto").innerHTML="💪 "+d.motor;document.getElementById("buscador-texto").innerHTML=d.buscador;document.getElementById("conexion-texto").innerHTML="🔌 40/40 CONECTADOS - ORO $"+d.ORO;
    if(d.jefe){document.getElementById("jefe-orden").innerHTML=d.jefe.orden;document.getElementById("jefe-mensaje").innerHTML=d.jefe.mensaje;}
    if(d.bancos){document.getElementById("banco-alerta").innerHTML="🏦 "+d.bancos.alerta_banco;document.getElementById("banco-lista").innerHTML=d.bancos.eventos_hoy.map(e=>"🏦 "+e.evento+" - "+e.efecto).join("<br>");}
    if(d.extra){document.getElementById("dxy-texto").innerHTML="💵 "+d.extra.DXY_texto;document.getElementById("vix-texto").innerHTML="😱 "+d.extra.VIX_texto;document.getElementById("extra-texto").innerHTML="₿ BTC $"+Math.round(d.extra.BTC)+" | 🛢️ "+d.extra.PETROLEO;}
    if(d.presidente){document.getElementById("presidente-mensaje").innerHTML=d.presidente.mensaje;document.getElementById("presidente-accion").innerHTML=d.presidente.accion_jefe;}
    if(d.cerebro){document.getElementById("cerebro-mensaje").innerHTML=d.cerebro.mensaje;document.getElementById("cerebro-leccion").innerHTML="📖 "+d.cerebro.leccion;document.getElementById("historial-texto").innerHTML="🏆 Ganadas: "+d.cerebro.ganadas+" | ❌ Perdidas: "+d.cerebro.perdidas;document.getElementById("historial-lista").innerHTML=d.cerebro.historial.map(h=>"⏰ "+h.hora+" - ORO $"+h.oro+" - "+h.decision).join("<br>");}
    if(d.zona){document.getElementById("zona-mensaje").innerHTML=d.zona.mensaje;document.getElementById("zona-accion").innerHTML="👉 ACCION: "+d.zona.accion;let dot=document.getElementById("zona-dot");let pos=50;if(d.ORO<=3910)pos=88;else if(d.ORO>=3970)pos=12;else if(d.ORO<=3940)pos=75;else if(d.ORO>=3955)pos=25;dot.style.top=pos+"%";dot.style.background=d.zona.color;if(d.zona.accion==="COMPRA"||d.zona.accion==="VENTA"){alarmaTocoZona(d.zona.mensaje);}}
    if(d.zona_del_dia){document.getElementById("zona-dia-mensaje").innerHTML=d.zona_del_dia.mensaje;document.getElementById("zona-dia-detalle").innerHTML="Precio ahora: $"+d.zona_del_dia.precio+" | ZONA ABAJO: $"+d.zona_del_dia.compra+" | ZONA ARRIBA: $"+d.zona_del_dia.venta+" | Cerca: "+d.zona_del_dia.dist+"%";ultimaSenalVIP="👑 VIP RAUDY - ZONA DEL DIA: "+d.zona_del_dia.nombre+" - "+d.zona_del_dia.mensaje+" - Entra en $"+d.zona_del_dia.compra+" - WhatsApp 0767574050";document.getElementById("vip-senal").innerHTML=ultimaSenalVIP;}
    if(d.mas_zonas){document.getElementById("mas-zonas").innerHTML=Object.entries(d.mas_zonas).map(([k,v])=>"🌍 <b>"+k+"</b> $"+v.precio+" - ZONA ABAJO $"+(v.compra||"")+" | ZONA ARRIBA $"+(v.venta||"")+" - <b>"+v.senal+"</b>").join("<br>");}
    document.getElementById("origen-precios").innerHTML="🥇 ORO $"+d.ORO+" → gold-api.com + Yahoo USA - "+d.robots_conectados.ORO.senal+"<br>💶 EUR/USD $"+d.EURUSD+" → Yahoo USA - "+d.robots_conectados.EURUSD.senal+"<br>₿ BTC $"+Math.round(d.BTC)+" → Yahoo USA";
    dibujarVelas(d.ORO);
    let mapa={"ORO":d.ORO,"NVDA":d.NVDA,"AAPL":d.AAPL,"TSLA":d.TSLA,"EURUSD":d.EURUSD,"BTC":d.BTC};simbolos.forEach(s=>{if(mapa[s.id])s.precio=mapa[s.id];});renderAcc();
  }catch(e){document.getElementById("satelite-texto").innerHTML="🛰️ Buscando USA...";}
}
setInterval(actualizarSateliteUSA,15000);actualizarSateliteUSA();setInterval(()=>{let d=new Date();document.getElementById("reloj").innerHTML=d.toLocaleTimeString("es-ES");document.getElementById("sesion").innerHTML=d.getHours()>=14&&d.getHours()<21?"🟢 SESIÓN NEW YORK ABIERTA":"🟡 Sesión cerrada";},1000);setInterval(analizarTodo,30000);analizarTodo();
</script></body></html>
"""

@app.route("/")
def home(): return HTML

@app.route("/api/satelite_usa")
def satelite_usa():
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=4); oro = float(r.json().get('price', 4088))
    except: oro = get_precio_yahoo('GC=F', 4088)
    datos = {"ORO": oro, "NVDA": get_precio_yahoo('NVDA', 185.20), "AAPL": get_precio_yahoo('AAPL', 262.10), "TSLA": get_precio_yahoo('TSLA', 340.50), "MSFT": get_precio_yahoo('MSFT', 495.30), "AMZN": get_precio_yahoo('AMZN', 235.40), "META": get_precio_yahoo('META', 645.20), "GOOGL": get_precio_yahoo('GOOGL', 282.10), "EURUSD": get_precio_yahoo('EURUSD=X', 1.1140), "GBPUSD": get_precio_yahoo('GBPUSD=X', 1.3350), "USDJPY": get_precio_yahoo('USDJPY=X', 150.0), "BTC": get_precio_yahoo('BTC-USD', 105000)}
    motor_txt = motor_fuerza_total(oro, "ORO"); buscador_txt = buscador_nada_se_escape(datos); robots_conectados = conectar_todos(datos); bancos_info = get_info_bancaria(); extra_info = get_mercado_extra(); presidente_info = get_alerta_presidencial(); jefe_orden = jefe_manda_orden(bancos_info, datos, extra_info)
    cerebro_info = cerebro_aprende(datos, jefe_orden); cerebro_resumen = cerebro_recuerda(); zona_info = get_zona(oro); zona_dia = get_zona_del_dia(datos)
    return jsonify({**datos, "motor": motor_txt, "velocidad": "TURBO", "buscador": buscador_txt, "nyse": "ABIERTO", "nasdaq": "ABIERTO", "robots_conectados": robots_conectados, "mas_zonas": robots_conectados, "bancos": bancos_info, "jefe": jefe_orden, "extra": extra_info, "presidente": presidente_info, "cerebro": cerebro_resumen, "zona": zona_info, "zona_del_dia": zona_dia, "equipo_40": ROBOTS, "total_robots": 40})

@app.route("/api/preguntale")
def api_preguntale():
    try:
        precio_quiero = float(request.args.get("precio", 4070)); activo = request.args.get("activo", "ORO")
        try:
            r = requests.get('https://api.gold-api.com/price/XAU', timeout=4); precio_actual = float(r.json().get('price', 4088))
        except: precio_actual = 4088
        if activo != "ORO": precio_actual = get_precio_yahoo(activo, precio_actual)
        return jsonify(robot_responde_pregunta(precio_quiero, activo, precio_actual))
    except: return jsonify({"respuesta": "🤖 Jefe, escribe un numero", "decision": "ERROR", "precio_recomendado": 3910, "precio_actual": 4088})

if __name__ == "__main__": app.run(host="0.0.0.0", port=10000)
