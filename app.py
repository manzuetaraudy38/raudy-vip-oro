# JEFE BOT - 5 GRAFICOS - TODO VERDE = COMPRA - JEFE ORO
import os
from flask import Flask, request, jsonify
app = Flask(__name__)
ultima = {"accion": "ESPERANDO", "precio": "", "hora": ""}

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>JEFE ORO - 5 GRAFICOS</title>
<style>
body{background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:8px;margin:0}
h1{font-size:30px;margin:5px} h2{color:#FFD700;margin:5px}
.voz{background:#FFD700;color:black;padding:18px;border-radius:20px;font-size:20px;font-weight:bold;border:none;width:95%}
#senal{font-size:28px;font-weight:bold;padding:18px;border-radius:20px;margin:10px;background:#333}
.caja{background:#1a1a1a;padding:10px;border-radius:15px;margin:10px}
.grafico{height:300px;margin:10px;border-radius:15px;overflow:hidden;background:#111}
.titulo{font-size:22px;font-weight:bold;padding:10px}
.verde{color:#00FF00} .rojo{color:#FF5252}
</style></head>
<body>
<h1>👑 JEFE ORO 👑</h1>
<h2>5 GRAFICOS - TODO VERDE = COMPRA</h2>

<button class="voz" onclick="activar()">🔊 ACTIVAR VOZ JEFE 🔊</button>
<div id="senal">⏳ ESPERANDO... MIRA LOS 5 GRAFICOS, JEFE</div>

<div class="caja">
<h2>REGLA JEFE 👑</h2>
<p>🟢🟢🟢🟢🟢 TODO VERDE = COMPRA JEFE</p>
<p>🔴🔴🔴🔴🔴 TODO ROJO = VENTA JEFE</p>
<p>🟢🔴 MEZCLADO = ESPERA JEFE, NO TOQUES NADA</p>
</div>

<div class="titulo">1️⃣ GRAFICO 1 MINUTO - JEFE</div>
<div class="grafico"><div id="tv1"></div></div>

<div class="titulo">2️⃣ GRAFICO 5 MINUTOS - JEFE</div>
<div class="grafico"><div id="tv5"></div></div>

<div class="titulo">3️⃣ GRAFICO 15 MINUTOS - JEFE</div>
<div class="grafico"><div id="tv15"></div></div>

<div class="titulo">4️⃣ GRAFICO 1 HORA - JEFE</div>
<div class="grafico"><div id="tv60"></div></div>

<div class="titulo">5️⃣ GRAFICO 4 HORAS - JEFE GRANDE 👑</div>
<div class="grafico"><div id="tv240"></div></div>

<p>JEFE OK - ORO REAL - 5 TIEMPOS</p>

<script src="https://s3.tradingview.com/tv.js"></script>
<script>
function crear(id, intervalo){
  new TradingView.widget({"width":"100%","height":300,"symbol":"OANDA:XAUUSD","interval":intervalo,"timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":id});
}
crear("tv1","1"); crear("tv5","5"); crear("tv15","15"); crear("tv60","60"); crear("tv240","240");
var vozOn=false; var ultimaHablada="";
function hablar(t){ var v=new SpeechSynthesisUtterance(t); v.lang='es-ES'; speechSynthesis.cancel(); speechSynthesis.speak(v); }
function activar(){ vozOn=true; hablar('Jefe Oro listo. Cinco graficos, jefe. Uno, cinco, quince, una hora, cuatro horas. Cuando todo este verde, compra, jefe. Cuando todo este rojo, venta, jefe.'); }
async function revisar(){
  try{
    var r=await fetch('/senal'); var d=await r.json();
    var caja=document.getElementById('senal');
    if(d.accion=='COMPRA'){ caja.innerHTML='🟢 COMPRA JEFE 🟢<br>Precio: '+d.precio; caja.style.background='#00C853'; }
    if(d.accion=='VENTA'){ caja.innerHTML='🔴 VENTA JEFE 🔴<br>Precio: '+d.precio; caja.style.background='#D50000'; }
    if(d.accion!='ESPERANDO' && vozOn && d.hora!=ultimaHablada){
      ultimaHablada=d.hora;
      if(d.accion=='COMPRA') hablar('COMPRA JEFE, COMPRA. Todo verde, jefe.');
      if(d.accion=='VENTA') hablar('VENTA JEFE, VENTA. Todo rojo, jefe.');
    }
  }catch(e){}
}
setInterval(revisar, 5000); revisar();
</script>
</body></html>
"""

@app.route("/")
def home(): return HTML
@app.route("/senal")
def senal(): return jsonify(ultima)
@app.route("/webhook", methods=["POST"])
def webhook():
    global ultima
    try:
        datos = request.get_json(force=True)
        accion = str(datos.get("accion","")).upper()
        if accion in ["COMPRA","VENTA"]:
            ultima = {"accion": accion, "precio": str(datos.get("precio","")), "hora": str(datos.get("hora",""))}
            return jsonify({"ok": True, "jefe": ultima})
    except Exception as e: print(e)
    return jsonify({"ok": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
