# JEFE BOT - BONITO - 12 ROBOTS
import os
from flask import Flask

app = Flask(__name__)

HTML = """
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:20px}
h1{font-size:32px;margin:5px}
h2{color:#FFD700}
.boton{display:block;padding:25px;margin:15px;border-radius:20px;font-size:28px;font-weight:bold;color:white;text-decoration:none}
.verde{background:#00C853}
.rojo{background:#D50000}
.caja{background:#1a1a1a;padding:15px;border-radius:15px;margin:15px}
.robot{background:#222;padding:10px;margin:5px;border-radius:10px;display:inline-block;width:40%}
</style></head>
<body>
<h1>👑 JEFE ORO 👑</h1>
<h2>H4 MANDA - JEFE</h2>
<div class="caja"><h2>12 ROBOTS ACTIVOS</h2>
<p>6 COMPRA - 6 VENTA</p>
</div>
<a class="boton verde" href="/compra">🟢 COMPRA - 6 ROBOTS</a>
<a class="boton rojo" href="/venta">🔴 VENTA - 6 ROBOTS</a>
<div class="caja">
<h3>ROBOTS COMPRA</h3>
<div class="robot">🤖 COMPRA 1</div><div class="robot">🤖 COMPRA 2</div>
<div class="robot">🤖 COMPRA 3</div><div class="robot">🤖 COMPRA 4</div>
<div class="robot">🤖 COMPRA 5</div><div class="robot">🤖 COMPRA 6</div>
<h3>ROBOTS VENTA</h3>
<div class="robot">🤖 VENTA 1</div><div class="robot">🤖 VENTA 2</div>
<div class="robot">🤖 VENTA 3</div><div class="robot">🤖 VENTA 4</div>
<div class="robot">🤖 VENTA 5</div><div class="robot">🤖 VENTA 6</div>
</div>
<p>JEFE OK - LIVE - RENDER</p>
</body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/compra")
def compra():
    return "<h1 style='text-align:center;font-size:50px'>🟢 COMPRA JEFE 🟢<br><a href='/'>VOLVER</a></h1>"

@app.route("/venta")
def venta():
    return "<h1 style='text-align:center;font-size:50px'>🔴 VENTA JEFE 🔴<br><a href='/'>VOLVER</a></h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
