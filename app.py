from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ESTE ES EL CEREBRO DEL ROBOT, JEFE
PRODUCTOS = {
    "reloj": {"nombre": "⌚ RELOJ VIP ORO", "precio_compra": 19.99, "precio_venta_robot": 12.00},
    "cadena": {"nombre": "⛓️ CADENA ORO VIP", "precio_compra": 29.99, "precio_venta_robot": 18.00},
    "lentes": {"nombre": "🕶️ LENTES VIP", "precio_compra": 14.99, "precio_venta_robot": 8.00},
    "gorra": {"nombre": "🧢 GORRA VIP", "precio_compra": 15.99, "precio_venta_robot": 9.00},
}
PEDIDOS = []
COMPRAS_ROBOT = []

HTML = """
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ROBOT RAUDY VIP ORO</title><style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}
h1{color:#FFD700;font-size:32px}
.card{background:#111;border:2px solid #FFD700;border-radius:15px;padding:18px;margin:14px auto;max-width:380px}
button{background:#FFD700;color:#000;border:none;padding:13px;font-size:16px;font-weight:bold;border-radius:10px;width:100%;margin-top:8px}
.btn-verde{background:#25D366;color:#fff}
.price{color:#00FF00;font-size:22px;font-weight:bold}
input,select{width:100%;padding:12px;margin:6px 0;border-radius:8px;border:1px solid #FFD700;background:#222;color:#fff}
.chat{background:#111;border:2px solid #00FF00;border-radius:15px;padding:15px;max-width:380px;margin:20px auto;text-align:left}
.msg{background:#222;padding:10px;border-radius:10px;margin:8px 0}
</style></head><body>
<h1>🤖👑 ROBOT RAUDY VIP ORO 👑🤖</h1><p>EL ROBOT VENDE Y COMPRA SOLO, JEFE</p>

<div class="chat"><h3 style="color:#00FF00">🤖 CHATEA CON EL ROBOT</h3>
<div id="chat"><div class="msg">🤖 Hola jefe! Soy el Robot Raudy. Escribe: <b>quiero comprar reloj</b> o <b>quiero vender cadena</b></div></div>
<input id="texto" placeholder="Escribe aqui... ej: quiero comprar reloj"><button onclick="hablar()" class="btn-verde">ENVIAR AL ROBOT</button></div>

<h2>🛒 EL ROBOT TE VENDE</h2>
{% for key,p in productos.items() %}
<div class="card"><h2>{{p.nombre}}</h2><p class="price">${{p.precio_compra}}</p>
<form action="/comprar" method="post"><input name="producto" value="{{key}}" hidden><input name="nombre" placeholder="Tu nombre" required><input name="whatsapp" placeholder="Tu WhatsApp" required><button>🛒 COMPRAR CON EL ROBOT</button></form></div>
{% endfor %}

<h2>💰 EL ROBOT TE COMPRA A TI</h2>
<div class="card"><p>¿Tienes algo para venderle a Raudy? El robot te lo compra!</p>
<form action="/vender" method="post">
<select name="producto" required><option value="">Que vas a vender?</option>
{% for key,p in productos.items() %}<option value="{{key}}">{{p.nombre}} - El robot te paga ${{p.precio_venta_robot}}</option>{% endfor %}</select>
<input name="nombre" placeholder="Tu nombre" required><input name="whatsapp" placeholder="Tu WhatsApp" required><input name="estado" placeholder="Como esta? Ej: Nuevo, Usado bueno" required>
<button class="btn-verde">💰 VENDERLE AL ROBOT</button></form></div>

<p><a style="color:#FFD700" href="/admin">VER PEDIDOS (Solo Raudy)</a></p>
<p>© 2026 ROBOT RAUDY VIP ORO</p>
<script>
async function hablar(){
 let t=document.getElementById('texto').value; if(!t) return;
 document
