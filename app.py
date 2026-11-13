from flask import Flask, jsonify, request
import requests, os
from datetime import datetime
app = Flask(__name__)

# ===== RAUDY ORO M5 - AUTOMATICO =====
# MT5 | M5 | XAUUSD ORO | ROBOT AUTO SIEMPRE PRENDIDO
ZONA_ABAJO = 3910
ZONA_ARRIBA = 3970
MT5_DATA = {"ultimo": "MT5 M5 esperando...", "hora": "", "precio": 0, "activo": "XAUUSD", "accion": "ESPERA"}
OPS = {"abiertas": [], "cerradas": [], "auto": True, "ganado": 0, "perdido": 0, "u": "Robot M5 AUTO PRENDIDO"}

def precio_oro_m5():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=4)
        return float(r.json().get("price", 4088))
    except:
        return 4088

def analiza_m5(precio):
    rango = ZONA_ARRIBA - ZONA_ABAJO
    tol = rango * 0.15
    if abs(precio - ZONA_ABAJO) <= tol:
        return {"accion": "COMPRA M5", "msg": "🟢 M5 COMPRA AUTO - ORO $" + str(precio) + " toco ZONA ABAJO M5", "tp": round(precio + rango*0.8, 2), "sl": round(precio - rango*0.2, 2)}
    if abs(precio - ZONA_ARRIBA) <= tol:
        return {"accion": "VENTA M5", "msg": "🔴 M5 VENTA AUTO - ORO $" + str(precio) + " toco ZONA ARRIBA M5", "tp": round(precio - rango*0.8, 2), "sl": round(precio + rango*0.2, 2)}
    return {"accion": "ESPERA M5", "msg": "🟡 M5 ESPERA AUTO - ORO $" + str(precio) + " esperando zona M5", "tp": ZONA_ABAJO, "sl": ZONA_ARRIBA}

def robot_m5_auto(precio, info):
    # 1. CIERRA SOLO SI LLEGO A TP O SL
    for op in list(OPS["abiertas"]):
        gano = False; perdio = False
        if op["lado"] == "COMPRA M5":
            if precio >= op["tp"]: gano = True
            elif precio <= op["sl"]: perdio = True
        else:
            if precio <= op["tp"]: gano = True
            elif precio >= op["sl"]: perdio = True
        if gano or perdio:
            op["resultado"] = "GANO +$5" if gano else "PERDIO -$2"
            op["cierre"] = precio
            OPS["abiertas"].remove(op)
            OPS["cerradas"].append(op)
            if gano: OPS["ganado"] += 5
            else: OPS["perdido"] += 2
            OPS["u"] = "🤖 ROBOT M5 CERRO SOLO: " + op["lado"] + " - " + op["resultado"]
    # 2. SI AUTO ESTA APAGADO, NO ABRE
    if not OPS.get("auto", True):
        return OPS["u"]
    # 3. SI YA HAY UNA ABIERTA, NO ABRE OTRA
    if len(OPS["abiertas"]) >= 1:
        return "🤖 ROBOT M5 AUTO: Ya hay una abierta - esperando TP/SL"
    # 4. SI NO TOCO ZONA, NO OPERA
    if info["accion"] not in ["COMPRA M5", "VENTA M5"]:
        return "🤖 ROBOT M5 AUTO: ESPERA - no toco zona M5"
    # 5. ABRE SOLO
    nueva = {"activo": "XAUUSD", "lado": info["accion"], "entrada": precio, "tp": info["tp"], "sl": info["sl"], "lote": 0.01, "hora": datetime.now().strftime("%H:%M"), "estado": "ABIERTA", "tf": "M5", "modo": "AUTO"}
    OPS["abiertas"].append(nueva)
    OPS["u"] = "🤖 ROBOT M5 ABRIO SOLO AUTO: " + info["accion"] + " ORO $" + str(precio) + " TP $" + str(info["tp"]) + " SL $" + str(info["sl"])
    return OPS["u"]

@app.route("/")
def home():
    return """<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>RAUDY ORO M5 AUTO</title><style>body{background:#050505;color:#fff;font-family:Arial;text-align:center;margin:0}header{background:#FFD700;color:#000;padding:15px}.box{margin:10px;padding:15px;border-radius:15px;border:3px solid #FFD700}.m5{border-color:#FF00FF;background:#1a001a}.auto{border-color:#00FF88;background:#001a0a}button{width:100%;padding:14px;border-radius:15px;font-weight:bold;margin-top:5px}input{width:100%;padding:12px;margin:4px 0;border-radius:10px;background:#111;color:#fff}table{width:100%;font-size:12px;border-collapse:collapse}td,th{border:1px solid #333;padding:5px}</style></head><body><header><h1>👑 RAUDY ORO M5 AUTO 👑</h1><p>MT5 + M5 + XAUUSD ORO + ROBOT AUTOMATICO</p><p id='vivo'>🟢 EN VIVO M5 AUTO...</p></header><div class='box m5'><h2>📊 M5 - MT5 - CADA 5 MINUTOS</h2><p>Plataforma: MT5 | Timeframe: M5 | Simbolo: XAUUSD ORO</p><p id='m5Zona' style='font-weight:bold;font-size:18px'>Cargando M5...</p><p id='m5TP'></p><p id='mt5Estado'></p></div><div class='box auto'><h2>🤖 ROBOT M5 AUTOMATICO - PRENDIDO SOLO</h2><p>El robot abre solo y cierra solo. Tu no tocas nada.</p><p id='robotEstado'>Robot M5 AUTO esperando...</p><p id='robotOps'></p><button onclick='toggleAuto()' style='background:#00FF88'>🤖 APAGAR / PRENDER ROBOT AUTO</button><p id='autoEstado'>AUTO: 🟢 PRENDIDO</p></div><div class='box'><h2>📋 OPERACIONES M5 AUTO</h2><div id='tablaOps'>Cargando...</div></div><div class='box'><h2>💬 CHAT M5</h2><input id='chat' placeholder='Ej: m5 oro'><button onclick='enviarChat()' style='background:#FFD700'>💬 ENVIAR</button><p id='chatR' style='background:#111;padding:12px;border-radius:10px'>🤖 Hola jefe M5 AUTO...</p></div><script>async function enviarChat(){let t=document.getElementById('chat').value;if(!t)return;let r=await fetch('/api/chat?msg='+encodeURIComponent(t));let d=await r.json();document.getElementById('chatR').innerHTML='🤖 '+d.respuesta}async function toggleAuto(){let r=await fetch('/api/robot_auto');let d=await r.json();document.getElementById('autoEstado').innerHTML='AUTO: '+(d.auto?'🟢 PRENDIDO':'🔴 APAGADO')}async function up(){try{let r=await fetch('/api/m5?v='+Date.now());let d=await r.json();document.getElementById('vivo').innerHTML='🟢 EN VIVO M5 AUTO '+d.hora+' - ORO $'+d.precio;document.getElementById('m5Zona').innerHTML=d.m5.mensaje;document.getElementById('m5TP').innerHTML='TP M5 $'+d.m5.tp+' SL M5 $'+d.m5.sl+' - Accion: '+d.m5.accion;document.getElementById('mt5Estado').innerHTML=d.mt5.ultimo;document.getElementById('robotEstado').innerHTML=d.robot.mensaje;document.getElementById('robotOps').innerHTML='Abiertas: '+d.robot.abiertas.length+' | Ganado $'+d.robot.ganado+' | Perdido $'+d.robot.perdido+' | AUTO: '+(d.robot.auto?'🟢 ON':'🔴 OFF');let html='<table><tr><th>Hora</th><th>Lado</th><th>Entrada</th><th>TP</th><th>SL</th></tr>';d.robot.abiertas.forEach(o=>{html+='<tr><td>'+o.hora+'</td><td>'+o.lado+'</td><td>'+o.entrada+'</td><td>'+o.tp+'</td><td>'+o.sl+'</td></tr>'});d.robot.cerradas.slice(-5).forEach(o=>{html+='<tr><td>'+o.hora+'</td><td>'+o.lado+'</td><td>'+o.entrada+'</td><td>'+o.tp+'</td><td>'+o.sl+'</td></tr>'});html+='</table>';document.getElementById('tablaOps').innerHTML=html}catch(e){}}setInterval(up,10000);up();</script></body></html>"""

@app.route("/api/m5")
def api_m5():
    precio = precio_oro_m5()
    info = analiza_m5(precio)
    msg = robot_m5_auto(precio, info)
    return jsonify({"precio": precio, "hora": datetime.now().strftime("%H:%M:%S"), "m5": {"mensaje": info["msg"], "accion": info["accion"], "tp": info["tp"], "sl": info["sl"]}, "mt5": MT5_DATA, "robot": {"mensaje": msg, "abiertas": OPS["abiertas"], "cerradas": OPS["cerradas"], "ganado": OPS["ganado"], "perdido": OPS["perdido"], "auto": OPS.get("auto", True)}})

@app.route("/api/mt5", methods=["GET", "POST"])
def api_mt5():
    global MT5_DATA
    try:
        if request.method == "POST":
            data = request.get_json(force=True, silent=True) or {}
        else:
            data = request.args.to_dict()
        MT5_DATA = {"ultimo": "✅ MT5 M5 AUTO CONECTADO - XAUUSD $" + str(data.get("precio", "")) + " - " + str(data.get("accion", "")), "hora": datetime.now().strftime("%H:%M:%S"), "precio": data.get("precio", 0), "activo": "XAUUSD", "accion": data.get("accion", "ESPERA")}
        return jsonify({"ok": True, "recibido": MT5_DATA})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/api/robot_auto")
def api_auto():
    OPS["auto"] = not OPS.get("auto", True)
    return jsonify({"auto": OPS["auto"]})

@app.route("/api/chat")
def api_chat():
    precio = precio_oro_m5()
    info = analiza_m5(precio)
    return jsonify({"respuesta": info["msg"] + " | TP M5 $" + str(info["tp"]) + " SL M5 $" + str(info["sl"]) + " | Robot AUTO: " + ("PRENDIDO" if OPS.get("auto", True) else "APAGADO")})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
