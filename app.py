from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>body{background:#0a0a0a;color:gold;text-align:center;font-family:Arial;padding:20px}
    .box{border:2px solid gold;border-radius:20px;padding:20px;margin:15px 0;background:#111}
    .btn{background:gold;color:black;padding:15px 30px;border-radius:15px;font-weight:bold;text-decoration:none;display:inline-block;margin-top:20px}
    </style></head><body>
    <h1>👑 RAUDY VIP ORO 👑</h1><p style="color:#0f0">● LIVE ✅</p>
    <div class="box"><h2>ORO: $3876.40</h2><p>Nivel compra VIP: 3890</p></div>
    <div class="box"><p>EURUSD: 1.11658 | GBPUSD: 1.33853</p></div>
    <div class="box"><p>BOT ACTIVO 24/7</p></div>
    <a class="btn" href="/tc">VER MERCADO COMPLETO</a>
    </body></html>
    """)

@app.route('/tc')
def mercado():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>body{background:#000;color:gold;font-family:Arial;margin:0;padding:10px}
    h2{text-align:center}
    .info{background:#111;border:2px solid gold;border-radius:15px;padding:15px;margin:10px 0;text-align:center}
    .btn{background:gold;color:black;padding:12px 25px;border-radius:10px;font-weight:bold;text-decoration:none;display:inline-block;text-align:center}
    </style></head><body>
    <h2>🔥 RAUDY VIP MERCADO 🔥</h2>
    <div class="info">💰 ORO: $3876.40<br>EURUSD: 1.11658<br>GBPUSD: 1.33853</div>
    <div class="tradingview-widget-container" style="height:600px">
      <div id="tradingview_chart" style="height:600px"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({"autosize": true,"symbol": "OANDA:XAUUSD","interval": "15","timezone": "Etc/UTC","theme": "dark","style": "1","locale": "es","toolbar_bg": "#f1f3f6","enable_publishing": false,"allow_symbol_change": true,"container_id": "tradingview_chart"});
      </script>
    </div>
    <div style="text-align:center;margin-top:20px"><a class="btn" href="/">⬅ VOLVER AL INICIO</a></div>
    </body></html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RAUDY VIP 1000</title>
<style>
body{margin:0;font-family:Arial;background:#0a0a0a;color:#fff;padding:12px}
.top{background:gold;color:#000;padding:16px;border-radius:16px;text-align:center}
.top h1{margin:0;font-size:30px}
.card{background:#1a1a1a;border-radius:18px;padding:16px;margin-top:12px;border:2px solid #333}
.big{font-size:55px;font-weight:bold;text-align:center;color:#00ff88}
.cen{text-align:center;font-size:16px}
.btn{width:100%;padding:18px;font-size:22px;font-weight:bold;border:none;border-radius:14px;margin-top:10px}
.verde{background:#00c853;color:#fff}
.rojo{background:#d50000;color:#fff}
.morado{background:#7b1fa2;color:#fff}
.azul{background:#00bcd4;color:#fff}
.naranja{background:#ff9800;color:#000}
.oro{background:gold;color:#000}
input,select{width:100%;padding:14px;font-size:20px;border-radius:12px;border:none;margin-top:8px}
</style></head><body>
<div class="top"><h1>RAUDY VIP 1000</h1><p>CALIDAD TOTAL - EN VIVO</p><p id="estado">CONECTANDO...</p></div>
<div class="card">
<h2 style="text-align:center">BOT AUTO - CALIDAD TOTAL</h2>
<p class="cen">RSI: <b id="rsi" style="color:gold">--</b> | MACD: <b id="macd" style="color:#00bcd4">--</b></p>
<p class="cen">Bollinger: <b id="boll" style="color:#ff9800">--</b> | Doble: <b id="doble" style="color:#00ff88">--</b></p>
<p class="cen">Balance: <b id="balance" style="color:#00ff88">$1000</b></p>
<p class="cen" id="bot-est">BOT APAGADO</p>
<p class="cen" id="perf">Ganadas: 0 | Perdidas: 0</p>
<p class="cen" style="background:#000;padding:8px;border-radius:10px">RIESGO 1:2 - Gano $20 | Pierdo $10</p>
<button class="btn morado" id="btn-bot" onclick="toggleBot()">PRENDER BOT AUTO</button>
<button class="btn azul" onclick="hacerBack()">BACKTEST REAL</button>
<p class="cen" id="back-res" style="background:#000;padding:10px;border-radius:10px">Sin backtest todavia</p>
</div>
<div class="card">
<h2 style="text-align:center">ORO EN VIVO</h2>
<div class="big" id="precio">----</div>
<p class="cen" id="cerebro">CEREBRO: ESPERA</p>
<p class="cen" id="senal">SENAL: ESPERA</p>
<button class="btn naranja" onclick="activarVoz()">ACTIVAR VOZ</button>
</div>
<div class="card">
<h2 style="text-align:center">ELIGE ACTIVO</h2>
<select id="activo" onchange="cambiar()"><option value="ORO">ORO</option><option value="TESLA">TESLA</option><option value="APPLE">APPLE</option><option value="META">META</option><option value="EUR/USD">EUR/USD</option><option value="BTC">BTC</option></select>
<p class="cen">TP</p><input id="tp" value="4200" type="number">
<p class="cen">SL</p><input id="sl" value="4100" type="number">
<button class="btn verde" onclick="operar('COMPRAR')">COMPRAR</button>
<button class="btn rojo" onclick="operar('VENDER')">VENDER</button>
</div>
<div class="card">
<h2 style="text-align:center">PRECIOS</h2>
<p class="cen" id="lista">Cargando...</p>
</div>
<div class="card">
<h2 style="text-align:center">HABLAME JEFE</h2>
<a href="https://t.me/raudy_vip_oro_bot"><button class="btn" style="background:#0088cc;color:#fff">TELEGRAM</button></a>
<a href="https://wa.me/41767574050"><button class="btn" style="background:#25D366;color:#fff">WHATSAPP</button></a>
<a href="https://paypal.me/RaudyManzueta/20"><button class="btn oro">PAGAR $20 - PAYPAL</button></a>
</div>
<script>
let precios={};let act="ORO";let voz=false;
function hablar(t){let v=new SpeechSynthesisUtterance(t);v.lang='es-DO';speechSynthesis.speak(v);}
function activarVoz(){voz=true;hablar('Jefe voz activada');alert('VOZ ACTIVADA');}
function cambiar(){act=document.getElementById('activo').value;actualizar();}
function operar(t){hablar('Jefe voy a '+t);alert('Orden '+t+' '+act);}
async function toggleBot(){let r=await fetch('/api/bot_auto',{method:'POST'});let d=await r.json();document.getElementById('btn-bot').innerText=d.activo?'APAGAR BOT':'PRENDER BOT';document.getElementById('bot-est').innerText=d.ult;hablar(d.activo?'Bot prendido':'Bot apagado');}
async function hacerBack(){document.getElementById('back-res').innerText='Probando con datos reales...';let r=await fetch('/api/backtest');let d=await r.json();document.getElementById('back-res').innerHTML='Modo '+d.modo+'<br>Final $'+d.balance_final+'<br>Ganadas '+d.ganadas+' Perdidas '+d.perdidas+' Win '+d.winrate+'%';hablar('Backtest listo '+d.balance_final+' dolares');}
function actualizar(){if(precios[act]){document.getElementById('precio').innerText=precios[act];}}
async function cargar(){try{let r=await fetch('/api/precios');precios=await r.json();document.getElementById('estado').innerText='EN VIVO '+new Date().toLocaleTimeString();let h='';for(let k in precios){h+=k+': '+precios[k]+'<br>';}document.getElementById('lista').innerHTML=h;actualizar();let s=await fetch('/api/senal');let sd=await s.json();document.getElementById('cerebro').innerText='CEREBRO: '+sd.decision;document.getElementById('senal').innerText='SENAL: '+sd.decision;document.getElementById('rsi').innerText=sd.rsi;document.getElementById('macd').innerText=sd.macd;document.getElementById('boll').innerText=sd.bollinger;document.getElementById('doble').innerText=sd.doble;let b=await fetch('/api/bot_auto');let bd=await b.json();document.getElementById('balance').innerText='$'+bd.balance;document.getElementById('bot-est').innerText=bd.ult;document.getElementById('perf').innerText='Ganadas: '+bd.ganadas+' | Perdidas: '+bd.perdidas;}catch(e){document.getElementById('estado').innerText='Sin internet...';}}
cargar();setInterval(cargar,3000);
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/api/precios")
def api_precios():
    oro = precio("GC=F") or 4149
    tes = precio("TSLA") or 378
    apl = precio("AAPL") or 350
    met = precio("META") or 641
    eur = precio("EURUSD=X") or 1.16
    return jsonify({
        "ORO": oro,
        "TESLA": tes,
        "APPLE": apl,
        "META": met,
        "EUR/USD": eur,
        "BTC": 90000
    })

@app.route("/api/senal")
def api_senal():
    oro = precio("GC=F") or 4149
    dec = cerebro(oro, HIST)
    rr = rsi(HIST)
    mc = macd(HIST)
    bb = boll(HIST)
    dd = doble(HIST)
    txt = "CONFIRMADO" if dd else "ESPERA"
    return jsonify({
        "precio": oro,
        "decision": dec,
        "rsi": round(rr, 1),
        "macd": "SUBIENDO" if mc > 0 else "BAJANDO",
        "bollinger": bb,
        "doble": txt
    })

@app.route("/api/bot_auto", methods=["GET", "POST"])
def api_bot():
    if request.method == "POST":
        BOT["activo"] = not BOT["activo"]
        if BOT["activo"]:
            BOT["ult"] = "BOT PRENDIDO - Dinero falso"
        else:
            BOT["ult"] = "BOT APAGADO"
    return jsonify(BOT)

@app.route("/api/backtest")
def api_back():
    return jsonify(backtest())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
