from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP ORO</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;padding:20px}
h1{color:#FFD700;font-size:40px}
.card{background:#111;border:2px solid #FFD700;border-radius:15px;padding:20px;margin:15px auto;max-width:400px}
button{background:#FFD700;color:#000;border:none;padding:15px 25px;font-size:18px;font-weight:bold;border-radius:10px;width:100%}
a{color:#FFD700}
</style>
</head>
<body>
<h1>👑 RAUDY VIP ORO 👑</h1>
<p>Tu tienda VIP está EN VIVO</p>

<div class="card">
<h2>🔥 OFERTA VIP</h2>
<p>Producto Premium - Calidad Oro</p>
<h2>$19.99</h2>
<button onclick="alert('¡Gracias por tu compra, JEFE!')">COMPRAR AHORA</button>
</div>

<div class="card">
<h2>⭐ PRODUCTO 2</h2>
<p>Lo mejor para ti</p>
<h2>$29.99</h2>
<button onclick="alert('¡Gracias, JEFE!')">COMPRAR AHORA</button>
</div>

<p>WhatsApp: <a href="https://wa.me/18090000000">Escríbenos</a></p>
<p>© 2026 Raudy VIP Oro</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
