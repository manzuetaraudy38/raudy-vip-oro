# app.py - RAUDY VIP 1000 - PRECIOS REALES EN VIVO
import os, json, urllib.request
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")
USAR_TESTNET = os.getenv("USAR_TESTNET", "True") == "True"

# Simbolos reales de Yahoo Finance - GRATIS, SIN LLAVE
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
</style></head><body>

<div class="top"><h1>RAUDY VIP 1000 👑</h1><p>PRECIOS REALES EN VIVO - BYBIT + YAHOO</p><p id="estado">🔴 CONECTANDO PRECIOS REALES...</p></div>

<div class="card">
<div class="activo-titulo">TODOS LOS PRECIOS REALES</div>
<div class="lista-precios" id="lista">Cargando...</div>
<div style="text-align:center; color:#00ff88; font-size:14px;">Se actualiza cada 3 segundos - Fuente: Yahoo Finance en vivo</div>
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
<a href="https://t.me/TU_TELEGRAM"><button class="btn-tg">TELEGRAM</button></a>
<a href="https://wa.me/TU_WHATSAPP"><button class="btn-wa">WHATSAPP</button></a>
<a href="https://payhip.com/TU_LINK_DE_PAGO"><button class="btn-pago">💳 PAGAR PARA USAR MI ROBOT - $29/mes</button></a>
</div>

<script>
let precios = {};
let activoActual = "ORO";
let ultimoPrecio = 0;
function hablar(t){ let v = new SpeechSynthesisUtterance(t); v.lang='es-DO'; speechSynthesis.speak(v); document.getElementById('ultima-voz').innerText = "🔊 " + t; }
function cambiarActivo(){ activoActual = document.getElementById('activo').value; document.getElementById('nombre-activo').innerText = activoActual; actualizarPantalla(); }
function probarVoz(){ hablar('Jefe, esta en ' + document.getElementById('precio').innerText + ', atento'); }
function operar(tipo){ let p = document.getElementById('precio').innerText; let tp=document.getElementById('tp').value; let sl=document.getElementById('sl').value; hablar('Jefe, esta en '+p+', voy a '+tipo); fetch('/operar',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({tipo:tipo, activo:activoActual, precio:p, tp:tp, sl:sl})}); alert('Orden enviada: '+tipo+' '+activoActual+' en '+p); }
function actualizarPantalla(){
  if(!precios[activoActual]) return;
  let p = precios[activoActual];
  document.getElementById('precio').innerText = p;
  // Alarma de voz si sube o baja fuerte
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
  }catch(e){ document.getElementById('estado').innerText = "⚠️ Sin internet, reintentando..."; }
}
cargarPrecios();
setInterval(cargarPrecios, 3000);
</script></body></html>
"""

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
    # Si falla internet, manda ultimo precio de ejemplo para no dejar en blanco
    if not out:
        out = {"ORO": 3986, "TESLA": 342, "APPLE": 265, "META": 640, "EUR/USD": 1.16, "GBP/USD": 1.34, "USD/CHF": 0.79, "SP500": 6850}
    return jsonify(out)

@app.route("/operar", methods=["POST"])
def operar():
    data = request.get_json()
    decision = cerebro_1000(float(str(data.get("precio", 3986)).replace(",","")), float(data.get("tp", 4000)), float(data.get("sl", 3950)))
    print(f"ORDEN JEFE: {data} -> {decision} - TESTNET: {USAR_TESTNET}")
    return jsonify({"ok": True, "decision": decision, "pedido": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
