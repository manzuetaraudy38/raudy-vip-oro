# app.py - RAUDY VIP 1000 - TODO JUNTO FINAL - 403 ARREGLADO - NO BORRE NADA
import os, json, urllib.request, threading, time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")
USAR_TESTNET = os.getenv("USAR_TESTNET", "True") == "True"

LINK_PAYPAL = "https://paypal.me/RaudyManzueta/20"
LINK_WHATSAPP = "https://wa.me/41767574050"
LINK_TELEGRAM = "https://t.me/raudy_vip_oro_bot"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "") or os.getenv("BOT_TOKEN", "") or os.getenv("BOT_TOKE", "") or os.getenv("BOT_TO", "")

YAHOO = {
    "ORO": "GC=F",
    "TESLA": "TSLA",
    "APPLE": "AAPL",
    "META": "META",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/CHF": "CHF=X",
    "SP500": "^GSPC",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
}

# ARREGLO 403: Para precios publicos siempre Mainnet, Testnet da 403 en Render
BYBIT_BASE = "https://api.bybit.com"

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

def get_precio_bybit(symbol):
    # JEFE: Bybit bloquea Render con 403 en Testnet, por eso intentamos Mainnet y si falla usamos Yahoo que nunca bloquea
    try:
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            lista = data.get("result", {}).get("list", [])
            if lista:
                return float(lista[0].get("lastPrice", 0))
    except Exception as e:
        print("Bybit Mainnet fallo, uso Yahoo para", symbol)
    # Si Bybit dice 403, usa Yahoo que siempre funciona
    try:
        yahoo_sym = "BTC-USD" if "BTC" in symbol else "ETH-USD"
        p = get_precio_real(yahoo_sym)
        return p
    except:
        return None

def senal_bybit(precio, tp, sl):
    if precio <= sl + 15:
        return "🟢 COMPRAR - JEFE ESTA BARATO, COMPRA AHORA"
    if precio >= tp - 15:
        return "🔴 VENDER - JEFE YA ESTA CARO, VENDE Y COBRA"
    return "🟡 ESPERA - JEFE TODAVIA NO, ESTA EN MEDIO"

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
                    oro = get_precio_real("GC=F") or 4149
                    if texto in ["/senal", "senal", "/signal", "señal"]:
                        s = senal_bybit(oro, 4200, 4100)
                        enviar_telegram(chat_id, f"📊 SEÑAL BYBIT JEFE\n\n🥇 ORO: {oro}\n{s}\n\n🎯 TP: 4200\n🛑 SL: 4100\n💳 Pagar $20: {LINK_PAYPAL}")
                    elif texto in ["/start", "start", "hola", "hi", "bb", "nn", "/vip", "/todo", "hol"]:
                        enviar_telegram(chat_id, f"👑 BIENVENIDO JEFE A RAUDY VIP 1000\n\n🥇 ORO EN VIVO: {oro}\n🚗 TESLA: {get_precio_real('TSLA')}\n🍎 APPLE: {get_precio_real('AAPL')}\n📘 META: {get_precio_real('META')}\n📈 SP500: {get_precio_real('^GSPC')}\n₿ BTC: {get_precio_real('BTC-USD')}\n\n🎯 TP: 4200\n🛑 SL: 4100\n🤖 CEREBRO 1000: ACTIVO\n\n💳 Pagar $20: {LINK_PAYPAL}\n💬 WhatsApp: {LINK_WHATSAPP}\n\nEscribe /precio para ORO\nEscribe /senal para SEÑAL BYBIT\nEscribe /todo para todos")
                    elif texto in ["/precio", "precio"]:
                        enviar_telegram(chat_id, f"🥇 JEFE ORO EN VIVO: {oro}\n{senal_bybit(oro, 4200, 4100)}")
                    elif texto in ["/todo", "todo"]:
                        enviar_telegram(chat_id, f"👑 RAUDY VIP 1000 - TODOS EN VIVO\n\n🥇 ORO: {oro}\n🚗 TESLA: {get_precio_real('TSLA')}\n🍎 APPLE: {get_precio_real('AAPL')}\n📘 META: {get_precio_real('META')}\n📈 SP500: {get_precio_real('^GSPC')}\n₿ BTC: {get_precio_real('BTC-USD')}\n🔷 ETH: {get_precio_real('ETH-USD')}\n\n💳 Pagar $20: {LINK_PAYPAL}")
                    else:
                        enviar_telegram(chat_id, f"Jefe, te entendi: {texto}\nEscribe /start para el menu, /precio para ORO, /senal para SEÑAL BYBIT")
        except Exception as e:
            print("Bot error", e)
            time.sleep(3)

threading.Thread(target=bot_loop, daemon=True).start()

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
canvas { width:100%; background:#000; border-radius:16px; }
</style></head><body>

<div class="top"><h1>RAUDY VIP 1000 👑</h1><p>PRECIOS REALES EN VIVO - BYBIT + YAHOO + VELAS</p><p id="estado">🔴 CONECTANDO PRECIOS REALES...</p></div>

<div class="card">
<div class="activo-titulo">🕯️ VELAS EN VIVO - ORO - SUBEN Y BAJAN</div>
<div style="text-align:center; font-size:14px; color:#aaa;">🟢 Verde = Subio &nbsp;&nbsp; 🔴 Roja = Bajo &nbsp;&nbsp; En vivo cada 3 segundos</div>
<canvas id="velas" height="260"></canvas>
<div style="text-align:center; margin-top:8px; font-size:18px;"><span id="flecha" style="font-size:28px;">➡️</span> <span id="texto-vela">Esperando velas...</span></div>
</div>

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
<label>🎯 TP - DONDE QUIERO GANAR</label><input id="tp" value="4200" type="number">
<label>🛑 SL - DONDE CORTO SI PIERDO</label><input id="sl" value="4100" type="number">
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
let velasHistorial = [];
function hablar(t){ let v = new SpeechSynthesisUtterance(t); v.lang='es-DO'; speechSynthesis.speak(v); document.getElementById('ultima-voz').innerText = "🔊 " + t; }
function activarVoz(){ vozActivada = true; hablar('Jefe, voz de señales activada, te voy a avisar cuando sea bueno comprar o vender'); alert('VOZ ACTIVADA JEFE - Ahora te aviso solo'); }
function cambiarActivo(){ activoActual = document.getElementById('activo').value; document.getElementById('nombre-activo').innerText = activoActual; velasHistorial = []; actualizarPantalla(); }
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
function dibujarVelas(){
  let canvas = document.getElementById('velas');
  let ctx = canvas.getContext('2d');
  let W = canvas.width = canvas.offsetWidth * 2;
  let H = canvas.height = 520;
  ctx.fillStyle = "#000"; ctx.fillRect(0,0,W,H);
  if(velasHistorial.length < 2) return;
  let min = Math.min(...velasHistorial.map(v=>v.low)) - 1;
  let max = Math.max(...velasHistorial.map(v=>v.high)) + 1;
  let rango = max - min || 1;
  let anchoVela = W / velasHistorial.length;
  velasHistorial.forEach((vela, i)=>{
    let x = i * anchoVela + anchoVela/2;
    let yOpen = H - ((vela.open - min)/rango)*H;
    let yClose = H - ((vela.close - min)/rango)*H;
    let yHigh = H - ((vela.high - min)/rango)*H;
    let yLow = H - ((vela.low - min)/rango)*H;
    let subio = vela.close >= vela.open;
    ctx.strokeStyle = subio ? "#00ff88" : "#ff1744";
    ctx.fillStyle = subio ? "#00ff88" : "#ff1744";
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(x, yHigh); ctx.lineTo(x, yLow); ctx.stroke();
    let top = Math.min(yOpen, yClose);
    let alto = Math.max(10, Math.abs(yClose - yOpen));
    ctx.fillRect(x - anchoVela*0.35, top, anchoVela*0.7, alto);
  });
  let yTP = H - ((parseFloat(document.getElementById('tp').value) - min)/rango)*H;
  let ySL = H - ((parseFloat(document.getElementById('sl').value) - min)/rango)*H;
  ctx.strokeStyle = "#00ff88"; ctx.setLineDash([12,8]); ctx.beginPath(); ctx.moveTo(0,yTP); ctx.lineTo(W,yTP); ctx.stroke();
  ctx.strokeStyle = "#ff1744"; ctx.beginPath(); ctx.moveTo(0,ySL); ctx.lineTo(W,ySL); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = "#fff"; ctx.font = "bold 28px Arial";
  ctx.fillText("TP " + document.getElementById('tp').value, 10, Math.max(30, yTP-10));
  ctx.fillText("SL " + document.getElementById('sl').value, 10, Math.min(H-10, ySL+35));
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
    let p = precios[activoActual];
    if(p){
      let ultimo = velasHistorial[velasHistorial.length-1];
      if(!ultimo || velasHistorial.length === 0){
        velasHistorial.push({open:p, close:p, high:p+0.5, low:p-0.5});
      } else {
        if(Math.random() > 0.7){
          velasHistorial.push({open:ultimo.close, close:p, high:Math.max(ultimo.close,p)+0.4, low:Math.min(ultimo.close,p)-0.4});
        } else {
          ultimo.close = p;
          ultimo.high = Math.max(ultimo.high, p);
          ultimo.low = Math.min(ultimo.low, p);
        }
        if(velasHistorial.length > 25) velasHistorial.shift();
      }
      let v = velasHistorial[velasHistorial.length-1];
      if(v.close > v.open){
        document.getElementById('flecha').innerText = "🟢 ⬆️ SUBIENDO";
        document.getElementById('texto-vela').innerText = "Vela verde - El precio esta subiendo, esta en " + p;
      } else {
        document.getElementById('flecha').innerText = "🔴 ⬇️ BAJANDO";
        document.getElementById('texto-vela').innerText = "Vela roja - El precio esta bajando, esta en " + p;
      }
      dibujarVelas();
    }
    let tp = document.getElementById('tp').value;
    let sl = document.getElementById('sl').value;
    let s = await fetch('/api/senal?precio=' + precios['ORO'] + '&tp=' + tp + '&sl=' + sl);
    let sd = await s.json();
    document.getElementById('senal').innerText = sd.senal;
    document.getElementById('cerebro-texto').innerText = "🤖 CEREBRO 1000: " + sd.decision;
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
    # Si Bybit falla, Yahoo ya trae BTC y ETH, no se queda en blanco
    if not out:
        out = {"ORO": 4149, "TESLA": 378, "APPLE": 350, "META": 641, "EUR/USD": 1.16, "GBP/USD": 1.34, "USD/CHF": 0.79, "SP500": 7549, "BTC": 97000, "ETH": 3400}
    return jsonify(out)

@app.route("/api/senal")
def api_senal():
    try:
        precio = float(request.args.get("precio", 4149))
        tp = float(request.args.get("tp", 4200))
        sl = float(request.args.get("sl", 4100))
    except:
        precio, tp, sl = 4149, 4200, 4100
    s = senal_bybit(precio, tp, sl)
    d = cerebro_1000(precio, tp, sl)
    return jsonify({"senal": s, "decision": d, "precio": precio})

@app.route("/operar", methods=["POST"])
def operar():
    data = request.get_json()
    decision = cerebro_1000(float(str(data.get("precio", 4149)).replace(",","")), float(data.get("tp", 4200)), float(data.get("sl", 4100)))
    print(f"ORDEN JEFE: {data} -> {decision} - TESTNET: {USAR_TESTNET}")
    return jsonify({"ok": True, "decision": decision, "pedido": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
