from flask import Flask, render_template_string
import random
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template_string("""
    <body style="background:black;color:gold;text-align:center;padding:40px 20px;font-family:Arial;">
        <h1>RAUDY VIP ORO - GINEBRA</h1>
        <h2 style="color:white;">SEÑALES VIP 90%</h2>
        <br><br>
        <a href="/tc" style="background:gold;color:black;padding:20px 40px;font-weight:bold;text-decoration:none;border-radius:15px;font-size:20px;">VER SEÑALES</a>
        <br><br><br><br>
        <a href="https://www.paypal.me/RaudyManzueta/20" style="background:#0070BA;color:white;padding:20px 40px;font-weight:bold;text-decoration:none;border-radius:15px;font-size:20px;">💳 PAGAR CHF 20 PAYPAL</a>
    </body>
    """)

@app.route('/tc')
def tc():
    oro = round(random.uniform(3875, 3895), 2)
    senal = random.choice(["VENTA","COMPRA"])
    porc = random.randint(80, 89)
    color = "red" if senal=="VENTA" else "#00ff00"
    mensaje = f
