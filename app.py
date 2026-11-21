# JEFE BOT - GRAFICO REAL - ORO 1 MINUTO
import os
from flask import Flask
app = Flask(__name__)

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:10px;margin:0}
h1{font-size:30px;margin:5px} h2{color:#FFD700;margin:5px}
.boton{display:block;padding:20px;margin:10px;border-radius:20px;font-size:26px;font-weight:bold;color:white;text-decoration:none}
.verde{background:#00C853} .rojo{background:#D50000}
.caja{background:#1a1a1a;padding:12px;border-radius:15px;margin:10px}
.voz{background:#FFD700;color:black;padding:18px;border-radius:20px;font-size:22px;font-weight:bold;border:none;width:95%}
.grafico{height:450px;margin:10px;border-radius:15px;overflow:hidden}
.robot{background:#222;padding:8px;margin:4px;border-radius:10px;display:inline-block;width:40%}
</style></head>
<body>
<h1>👑 JEFE ORO 👑</h1>
<h2>H4 MANDA - GRAFICO 1 MINUTO - PRECIO REAL</h2>

<button class="voz" onclick="hablar('Jefe Oro listo. Grafico real, precio real, cada vela un minuto.')">🔊 ACTIVAR VOZ JEFE 🔊</button>

<div class="caja"><h2>🤖 ROBOT JEFE - ORO REAL</h2><p>12 ROBOTS - 6 COMPRA - 6 VENTA - CADA VELA 1 MINUTO</p></div>

<!-- GRAFICO REAL TRADINGVIEW ORO -->
<div class="grafico">
<div class="tradingview-widget-container">
<div id="tradingview_oro"></div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>
new TradingView.widget({
"width":"100%","height":450,"symbol":"OANDA:XAUUSD",
"interval":"1","timezone":"America/Santo_Domingo",
"theme":"dark","style":"1","locale":"es",
"toolbar_bg":"#f1f3f6","enable_publishing":false,
"hide_top_toolbar":false,"save_image":false,
"container_id":"tradingview_oro"
});
</script>
</div>
</div>

<a class="boton verde" href="#" onclick="hablar('COMPRA JEFE, COMPRA. Oro para arriba, jefe. Compra ahora, jefe.');return false;">🟢 COMPRA - 6 ROBOTS</a>
<a class="boton rojo" href="#" onclick="hablar('VENTA JEFE, VENTA. Oro para abajo, jefe. Venta ahora, jefe.');return false;">🔴 VENTA - 6 ROBOTS</a>

<div class="caja"><h3>ROBOTS COMPRA</h3>
<div class="robot">🤖 COMPRA 1</div><div class="robot">🤖 COMPRA 2</div>
<div class="robot">🤖 COMPRA 3</div><div class="robot">🤖 COMPRA 4</div>
<div class="robot">🤖 COMPRA 5</div><div class="robot">🤖 COMPRA 6</div>
<h3>ROBOTS VENTA</h3>
<div class="robot">🤖 VENTA 1</div><div class="robot">🤖 VENTA 2</div>
<div class="robot">🤖 VENTA 3</div><div class="robot">🤖 VENTA 4</div>
<div class="robot">🤖 VENTA 5</div><div class="robot">🤖 VENTA 6</div>
</div>
<p>JEFE OK - ORO REAL - 1 MINUTO</p>
<script>
function hablar(t){
  var v = new SpeechSynthesisUtterance(t);
  v.lang='es-ES'; speechSynthesis.cancel(); speechSynthesis.speak(v);
}
</script>
</body></html>
"""
@app.route("/")
def home(): return HTML
@app.route("/compra")
def compra(): return "<h1 style='text-align:center'>COMPRA JEFE</h1>"
@app.route("/venta")
def venta(): return "<h1 style='text-align:center'>VENTA JEFE</h1>"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
