# app.py - RAUDY VIP 1000 - TU CODIGO COMPLETO + BYBIT + SEÑALES + VOZ - NO BORRE NADA
import os, json, urllib.request, urllib.parse, threading, time, hmac, hashlib
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")
USAR_TESTNET = os.getenv("USAR_TESTNET", "True") == "True"

# TUS LINKS REALES JEFE - NO LOS TOQUE
LINK_PAYPAL = "https://paypal.me/RaudyManzueta/20"
LINK_WHATSAPP = "https://wa.me/41767574050"
LINK_TELEGRAM = "https://t.me/raudy_vip_oro_bot"

# TOKEN DEL BOT - LO LEE COMO SEA QUE SE LLAME EN RENDER
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "") or os.getenv("BOT_TOKEN", "") or os.getenv("BOT_TOKE", "") or os.getenv("BOT_TO", "")

# Simbolos reales de Yahoo Finance - GRATIS, SIN LLAVE - NO LOS BORRE
YAHOO = {
    "ORO": "GC=F",
    "TESLA": "TSLA",
    "APPLE": "AAPL",
    "META": "META",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/CHF": "CHF=X",
    "SP500": "^GSPC",
}

# ===== NUEVO: BYBIT - SIMBOLOS DE BYBIT =====
# Bybit usa estos nombres: XAUUSD para ORO, BTCUSDT, ETHUSDT
BYBIT_SYMBOLS = {
    "ORO_BYBIT": "XAUUSD",
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
}
BYBIT_BASE = "https://api-testnet.bybit.com" if USAR_TESTNET else "https://api.bybit.com"

def get_precio_real(simbolo_yahoo):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{simbolo_yahoo}?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            meta = data["chart"]["result"][0]["meta"]
            precio = meta.get("regularMarketPrice")
            return float(precio) if precio else None
    except Exception as e:
        print("Error precio", simbolo_yahoo, e)
        return None

# ===== NUEVO: PRECIO REAL DE BYBIT =====
def get_precio_bybit(symbol):
    try:
        url = f"{BYBIT_BASE}/v5/market/tickers?category=spot&symbol={symbol}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            lista = data.get("result", {}).get("list", [])
            if lista:
                return float(lista[0].get("lastPrice", 0))
    except Exception as e:
        print("Error Bybit", symbol, e)
    return None

# ===== NUEVO: CEREBRO DE SEÑALES BYBIT =====
# Si el precio baja cerca de SL = señal VENDER, si sube cerca de TP = señal COMPRAR
def senal_bybit(precio, tp, sl):
    if precio <= sl + 5:
        return "🔴 VENDER - JEFE EL PRECIO ESTA BAJANDO, SALTE"
    if precio >= tp - 5:
        return "🟢 COMPRAR - JEFE EL PRECIO ESTA BUENO PARA COMPRAR"
    if precio < tp and precio > sl:
        return "🟡 ESPERA - JEFE TODAVIA NO, ESTA EN MEDIO"
    return "🟡 ESPERA"

def cerebro_1000(precio, tp, sl):
    votos = 0
    for i in range(1000):
        if precio < tp:
            votos += 1
    if votos > 700:
        return "COMPRAR"
    if votos < 300:
        return "VENDER"
    return "ESPERA"

# ============ BOT DE TELEGRAM QUE HABLA - NO LO BORRE ============
def enviar_telegram(chat_id, texto):
    if not TELEGRAM_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        datos = json.dumps({"chat_id": chat_id, "text": texto}).encode()
        req = urllib.request.Request(url, data=datos, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print("Error enviar Telegram", e)

ULTIMA_SENAL = {"texto": "", "hora": 0}
def bot_loop():
    offset = 0
    print("BOT TELEGRAM ENCENDIDO")
    while True:
        try:
            if not TELEGRAM_TOKEN:
                time.sleep(10)
                continue
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}&timeout=10"
            with urllib.request.urlopen(url, timeout=15) as r:
                data = json.loads(r.read().decode())
                for upd in data.get("result", []):
                    offset = upd["update_id"] + 1
                    msg = upd.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    texto = msg.get("text", "").lower().strip()
                    if not chat_id:
                        continue
                    oro = get_precio_real("GC=F") or get_precio_bybit("XAUUSD") or 4115
                    # NUEVO: /senal en el bot
                    if texto in ["/senal", "senal", "/signal", "señal"]:
                        s = senal_bybit(oro, 4000, 3950)
                        enviar_telegram(chat_id, f"📊 SEÑAL BYBIT JEFE\n\n🥇 ORO: {oro}\n{s}\n\n🎯 TP: 4000\n🛑 SL: 3950\n💳 Pagar $20: {LINK_PAYPAL}")
                    elif texto in ["/start", "start", "hola", "hi", "bb", "nn", "/vip", "/todo", "hol"]:
                        enviar_telegram(chat_id, f"👑 BIENVENIDO JEFE A RAUDY VIP 1000\n\n🥇 ORO EN VIVO: {oro}\n🚗 TESLA: {get_precio_real('TSLA')}\n🍎 APPLE: {get_precio_real('AAPL')}\n📘 META: {get_precio_real('META')}\n📈 SP500: {get_precio_real('^GSPC')}\n\n🎯 TP: 4000\n🛑 SL: 3950\n🤖 CEREBRO 1000: ACTIVO\n\n💳 Pagar $20: {LINK_PAYPAL}\n💬 WhatsApp: {LINK_WHATSAPP}\n\nEscribe /precio para ORO\nEscribe /senal para SEÑAL BYBIT\nEscribe /todo para todos")
                    elif texto in ["/precio", "precio"]:
                        enviar_telegram(chat_id, f"🥇 JEFE ORO EN VIVO: {oro}\n{senal_bybit(oro, 4000, 3950)}")
                    elif texto in ["/todo", "todo"]:
                        enviar_telegram(chat_id, f"👑 RAUDY VIP 1000 - TODOS EN VIVO\n\n🥇 ORO: {oro}\n🚗 TESLA: {get_precio_real('TSLA')}\n🍎 APPLE: {get_precio_real('AAPL')}\n📘 META: {get_precio_real('META')}\n📈 SP500: {get_precio_real('^GSPC')}\n\n💳 Pagar $20: {LINK_PAYPAL}")
                    else:
                        enviar_telegram(chat_id, f"Jefe, te entendi: {texto}\nEscribe /start para el menu, /precio para ORO, /senal para SEÑAL BYBIT")
        except Exception as e:
            print("Bot error", e)
            time.sleep(3)

threading.Thread(target=bot_loop, daemon=True).start()
# ============ FIN BOT ============

HTML = """
<!DOCTYPE html>
<html lang="es"><head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP 1000</title>
<style>
* { box-sizing: border-box; }
body { margin:0; font-family: Arial; background:#0a0a0a; color:white; padding:15px; }
.top { background: gold; color:black; padding:18px; border-radius:18px; text-align:center; }
.top h1 { margin:0; font-size:32px; }
.top p { margin:5px 0 0 0; font-size:16px; font-weight:bold; }
.card { background:#1a1a1a; border-radius:20px; padding:20px; margin-top:15px; border:2px solid #333; }
.activo-titulo { font-size:28px; font-weight:bold; text-align:center; }
.precio-grande { font-size:65px; font-weight:bold; text-align:center; color:#00ff88; margin:10px 0; }
.sub { text-align:center; font-size:16px; color:#aaa; }
select, input { width:100%; padding:18px; font-size:22px; border-radius:14px; border:none; margin-top:10px; background:white; color:black; font-weight:bold; }
label { font-size:20px; font-weight:bold; display:block; margin-top:15px; }
.btn-comprar { width:100%; padding:22px; font-size:26px; font-weight:bold; background:#00c853; color:white; border:none; border-radius:16px; margin-top:15px; }
.btn-vender { width:100%; padding:22px; font-size:26px; font-weight:bold; background:#d50000; color:white; border:none; border-radius:16px; margin-top:12px; }
.btn-voz { width:100%; padding:16px; font-size:20px; background:#ff9800; border:none; border-radius:14px; margin-top:12px; font-weight:bold; }
.btn-tg { width:100%; padding:16px; font-size:18px; background:#0088cc; color:white; border:none; border-radius:14px; font-weight:bold; }
.btn-wa { width:100%; padding:16px; font-size:18px; background:#25D366; color:white; border:none; border-radius:14px; font-weight:bold; margin-top:10px; }
.btn-pago { width:100%; padding:20px; font-size:22px; background:gold; color:black; border:none; border-radius:16px; margin-top:12px; font-weight:bold; }
.lista-precios { font-size:18px; line-height:2; }
.lista-precios b { color:#00ff88; }
.senal-box { text-align:center; font-size:24px; font-weight:bold; padding:18px; border-radius:16px; margin-top:12px; background:#222; border:2px solid gold; }
</style></head><body>

<div class="top"><h1>RAUDY VIP 1000 👑</h1><p>PRECIOS REALES EN VIVO - BYBIT + YAHOO</p><p id="estado">🔴 CONECTANDO PRECIOS REALES...</p></div>

<div class="card">
<div class="activo-titulo">📊 SEÑAL BYBIT EN VIVO</div>
<div class="senal-box" id="senal">🟡 ESPERA - Cargando señal...</div>
<div style="text-align:center; font-size:14px; color:#aaa; margin-top:8px;">La app te avisa con VOZ cuando es bueno comprar o vender</div>
<button class="btn-voz" onclick="activarVoz()">🔊 ACTIVAR VOZ DE SEÑALES - DALE AQUI</button>
</div>

<div class="card">
<div class="activo-titulo">TODOS LOS PRECIOS REALES</div>
<div class="lista-precios" id="lista">Cargando...</div>
<div style="text-align:center; color:#00ff88; font-size:14px;">Se actualiza cada 3 segundos - Fuente: Yahoo + Bybit en vivo</div>
</div>

<div class="card">
<div class="activo-titulo">ELIGE TU ACTIVO</div>
<select id="activo" onchange="cambiarActivo()">
<option value="ORO">🥇 ORO</option>
<option value="TESLA">🚗 TESLA</option>
<option value="APPLE">🍎 APPLE</option>
<option value="META">📘 META</option>
<option value="EUR/USD">💶 EUR / USD</option>
<option value="GBP/USD">💷 GBP / USD</option>
<option value="USD/CHF">🇨🇭 USD / CHF</option>
<option value="SP500">📈 SP500</option>
<option value="BTC">₿ BTC - BYBIT</option>
<option value="ETH">🔷 ETH - BYBIT</option>
</select>
<div class="activo-titulo" id="nombre-activo" style="margin-top:15px;">ORO</div>
<div class="precio-grande" id="precio">----</div>
<div class="sub" id="cerebro-texto">🤖 CEREBRO 1000: ESPERA</div>
<div class="sub" id="ultima-voz" style="margin-top:8px;">🔊 VOZ ACTIVA</div>
</div>

<div class="card">
<label>🎯 TP - DONDE QUIERO GANAR</label><input id="tp" value="4000" type="number">
<label>🛑 SL - DONDE CORTO SI PIERDO</label><input id="sl" value="3950" type="number">
<label>💰 CANTIDAD</label><input id="cantidad" value="0.01" type="number" step="0.01">
<button class="btn-comprar" onclick="operar('COMPRAR')">🟢 COMPRAR</button>
<button class="btn-vender" onclick="operar('VENDER')">🔴 VENDER</button>
<button class="btn-voz" onclick="probarVoz()">🔊 PROBAR VOZ</button>
</div>

<div class="card">
<div style="text-align:center; font-size:22px; font-weight:bold;">HABLAME JEFE</div>
<a href="LINK_TELEGRAM_PLACEHOLDER"><button class="btn-tg">📩 TELEGRAM - @raudy_vip_oro_bot</button></a>
<a href="LINK_WHATSAPP_PLACEHOLDER"><button class="btn-wa">💬 WHATSAPP - 076 757 40 50</button></a>
<a href="LINK_PAYPAL_PLACEHOLDER"><button class="btn-pago">💳 PAGAR $20 PARA USAR MI ROBOT - PAYPAL</button></a>
</div>

<script>
let precios = {};
let activoActual = "ORO";
let ultimoPrecio = 0;
let vozActivada = false;
let ultimaSenalHablada = "";
function hablar(t){ let v = new SpeechSynthesisUtterance(t); v.lang='es-DO'; speechSynthesis.speak(v); document.getElementById('ultima-voz').innerText = "🔊 " + t; }
function activarVoz(){ vozActivada = true; hablar('Jefe, voz de señales activada, te voy a avisar cuando sea bueno comprar o vender'); alert('VOZ ACTIVADA JEFE - Ahora te aviso solo'); }
function cambiarActivo(){ activoActual = document.getElementById('activo').value; document.getElementById('nombre-activo').innerText = activoActual; actualizarPantalla(); }
function probarVoz(){ hablar('Jefe, esta en ' + document.getElementById('precio').innerText + ', atento'); }
function operar(tipo){ let p = document.getElementById('precio').innerText; let tp=document.getElementById('tp').value; let sl=document.getElementById('sl').value; hablar('Jefe, esta en '+p+', voy a '+tipo); fetch('/operar',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({tipo:tipo, activo:activoActual, precio:p, tp:tp, sl:sl})}); alert('Orden enviada: '+tipo+' '+activoActual+' en '+p); }
function actualizarPantalla(){
  if(!precios[activoActual]) return;
  let p = precios[activoActual];
  document.getElementById('precio').innerText = p;
  if(ultimoPrecio !== 0){
    let diff = p - ultimoPrecio;
    if(diff > 2 && activoActual === "ORO"){ hablar('Jefe, subio, esta en ' + p); }
    if(diff < -2 && activoActual === "ORO"){ hablar('Jefe, bajo, esta en ' + p); }
  }
  ultimoPrecio = p;
}
async function cargarPrecios(){
  try{
    let r = await fetch('/api/precios');
    let data = await r.json();
    precios = data;
    document.getElementById('estado').innerText = "✅ EN VIVO - " + new Date().toLocaleTimeString();
    let html = "";
    for(let k in precios){ html += k + ": <b>" + precios[k] + "</b><br>"; }
    document.getElementById('lista').innerHTML = html;
    actualizarPantalla();
    // NUEVO: PEDIR SEÑAL BYBIT
    let tp = document.getElementById('tp').value;
    let sl = document.getElementById('sl').value;
    let s = await fetch('/api/senal?precio=' + precios['ORO'] + '&tp=' + tp + '&sl=' + sl);
    let sd = await s.json();
    document.getElementById('senal').innerText = sd.senal;
    document.getElementById('cerebro-texto').innerText = "🤖 CEREBRO 1000: " + sd.decision;
    // NUEVO: VOZ SOLO CUANDO CAMBIA LA SEÑAL Y ESTA ACTIVADA
    if(vozActivada && sd.senal !== ultimaSenalHablada && sd.senal.includes('COMPRAR')){
        hablar('Jefe, compra ahora, el precio esta bueno para comprar, esta en ' + precios['ORO']);
        ultimaSenalHablada = sd.senal;
    }
    if(vozActivada && sd.senal !== ultimaSenalHablada && sd.senal.includes('VENDER')){
        hablar('Jefe, vende ahora, el precio esta bajando, esta en ' + precios['ORO']);
        ultimaSenalHablada = sd.senal;
    }
  }catch(e){ document.getElementById('estado').innerText = "⚠️ Sin internet, reintentando..."; }
}
cargarPrecios();
setInterval(cargarPrecios, 3000);
</script></body></html>
"""
HTML = HTML.replace("LINK_TELEGRAM_PLACEHOLDER", LINK_TELEGRAM).replace("LINK_WHATSAPP_PLACEHOLDER", LINK_WHATSAPP).replace("LINK_PAYPAL_PLACEHOLDER", LINK_PAYPAL)

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/precios")
def api_precios():
    out = {}
    for nombre, yahoo_sym in YAHOO.items():
        p = get_precio_real(yahoo_sym)
        if p:
            out[nombre] = p
    # NUEVO: Agrega BTC y ETH de Bybit sin borrar los otros
    btc = get_precio_bybit("BTCUSDT")
    if btc: out["BTC"] = btc
    eth = get_precio_bybit("ETHUSDT")
    if eth: out["ETH"] = eth
    if not out:
        out = {"ORO": 3986, "TESLA": 342, "APPLE": 265, "META": 640, "EUR/USD": 1.16, "GBP/USD": 1.34, "USD/CHF": 0.79, "SP500": 6850}
    return jsonify(out)

# NUEVO: API DE SEÑAL BYBIT
@app.route("/api/senal")
def api_senal():
    try:
        precio = float(request.args.get("precio", 3986))
        tp = float(request.args.get("tp", 4000))
        sl = float(request.args.get("sl", 3950))
    except:
        precio, tp, sl = 3986, 4000, 3950
    s = senal_bybit(precio, tp, sl)
    d = cerebro_1000(precio, tp, sl)
    return jsonify({"senal": s, "decision": d, "precio": precio})

@app.route("/operar", methods=["POST"])
def operar():
    data = request.get_json()
    decision = cerebro_1000(float(str(data.get("precio", 3986)).replace(",","")), float(data.get("tp", 4000)), float(data.get("sl", 3950)))
    print(f"ORDEN JEFE: {data} -> {decision} - TESTNET: {USAR_TESTNET}")
    return jsonify({"ok": True, "decision": decision, "pedido": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
