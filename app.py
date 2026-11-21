# JEFE BOT - AVISA SOLO - TRADINGVIEW - 1 Y 2
import os
from flask import Flask, request, jsonify
app = Flask(__name__)

# Aqui guardamos la ultima señal
ultima = {"accion": "ESPERANDO", "precio": "", "hora": ""}

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:10px}
h1{font-size:30px} h2{color:#FFD700}
.boton{display:block;padding:20px;margin:10px;border-radius:20px;font-size:26px;font-weight:bold;color:white;text-decoration:none}
.verde{background:#00C853} .rojo{background:#D50000}
.caja{background:#1a1a1a;padding:12px;border-radius:15px;margin:10px}
.voz{background:#FFD700;color:black;padding:18px;border-radius:20px;font-size:22px;font-weight:bold;border:none;width:95%}
.grafico{height:450px;margin:10px;border-radius:15px;overflow:hidden}
#senal{font-size:32px;font-weight:bold;padding:20px;border-radius:20px;margin:10px;background:#333}
</style></head>
<body>
<h1>👑 JEFE ORO 👑</h1>
<h2>H4 MANDA - AVISA SOLO - TRADINGVIEW</h2>
<button class="voz" onclick="activar()">🔊 ACTIVAR VOZ - PARA QUE TE AVISE SOLO 🔊</button>
<p>JEFE, DALE A ESE BOTON AMARILLO 1 VEZ, JEFE. DESPUES DEJA EL CELULAR ABIERTO, JEFE. EL SOLO TE VA A HABLAR, JEFE.</p>
<div id="senal">⏳ ESPERANDO SEÑAL DE TRADINGVIEW...</div>
<div class="caja"><h2>🤖 12 ROBOTS - 6 COMPRA - 6 VENTA</h2><p>H4 MANDA - 1 MINUTO</p></div>
<div class="grafico"><div class="tradingview-widget-container"><div id="tv"></div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>new TradingView.widget({"width":"100%","height":450,"symbol":"OANDA:XAUUSD","interval":"1","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"tv"});</script>
</div></div>
<a class="boton verde" href="#" onclick="probar('COMPRA');return false;">🟢 PROBAR COMPRA</a>
<a class="boton rojo" href="#" onclick="probar('VENTA');return false;">🔴 PROBAR VENTA</a>
<p>JEFE OK - AVISA SOLO</p>
<script>
var vozOn=false; var ultimaHablada="";
function hablar(t){ var v=new SpeechSynthesisUtterance(t); v.lang='es-ES'; speechSynthesis.cancel(); speechSynthesis.speak(v); }
function activar(){ vozOn=true; hablar('Jefe Oro listo. Ahora te aviso solo, jefe. Cuando TradingView diga compra o venta, yo te lo digo, jefe.'); }
function probar(a){ hablar(a+' JEFE, '+a+'. Prueba, jefe.'); }
async function revisar(){
  try{
    var r=await fetch('/senal'); var d=await r.json();
    var caja=document.getElementById('senal');
    if(d.accion=='COMPRA'){ caja.innerHTML='🟢 COMPRA JEFE 🟢<br>'+d.precio; caja.style.background='#00C853'; }
    if(d.accion=='VENTA'){ caja.innerHTML='🔴 VENTA JEFE 🔴<br>'+d.precio; caja.style.background='#D50000'; }
    if(d.accion!='ESPERANDO' && vozOn && d.hora!=ultimaHablada){
      ultimaHablada=d.hora;
      if(d.accion=='COMPRA') hablar('COMPRA JEFE, COMPRA. Oro para arriba, jefe. Compra ahora, jefe.');
      if(d.accion=='VENTA') hablar('VENTA JEFE, VENTA. Oro para abajo, jefe. Venta ahora, jefe.');
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
            print("JEFE SEÑAL:", ultima)
            return jsonify({"ok": True, "jefe": ultima})
    except Exception as e:
        print(e)
    return jsonify({"ok": False})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
