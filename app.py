from flask import Flask, render_template_string
import random
from urllib.parse import quote
from datetime import datetime

app = Flask(__name__)

PAYPAL_LINK = "https://www.paypal.me/RaudyManzueta/20"

@app.route('/')
def inicio():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>RAUDY VIP ORO - GINEBRA</title>
    <style>
        body{{background:#000;color:#fff;font-family:Arial;margin:0;padding:0;text-align:center}}
        .header{{background:#111;border-bottom:3px solid gold;padding:30px 15px}}
        .logo{{color:gold;font-size:32px;font-weight:bold}}
        .container{{padding:20px;max-width:500px;margin:auto}}
        .card{{background:#111;border:1px solid #333;border-radius:15px;padding:20px;margin:15px 0}}
        .btn-gold{{display:block;background:gold;color:black;padding:18px;font-weight:bold;text-decoration:none;border-radius:12px;font-size:18px;margin:10px 0}}
        .btn-paypal{{display:block;background:#0070BA;color:white;padding:22px;font-weight:bold;text-decoration:none;border-radius:15px;font-size:20px;margin:20px 0;border:3px solid white}}
    </style>
    </head>
    <body>
        <div class="header"><div class="logo">RAUDY VIP ORO</div><div style="color:white;">GINEBRA - SEÑALES VIP 90%</div></div>
        <div class="container">
            <div class="card">
                <h2 style="color:gold;">QUE INCLUYE VIP CHF 20</h2>
                <p style="text-align:left;line-height:28px;">
                ✅ ORO XAU/USD diario<br>
                ✅ EUR/USD y GBP/USD<br>
                ✅ Entrada, SL y TP<br>
                ✅ 3-5 señales por día<br>
                ✅ Grupo VIP WhatsApp<br>
                ✅ Soporte Ginebra
                </p>
            </div>
            <a href="/tc" class="btn-gold">VER SEÑALES DEMO GRATIS</a>
            <a href="{PAYPAL_LINK}" class="btn-paypal">💳 PAGAR VIP CHF 20 CON PAYPAL</a>
            <p style="color:#0070BA;font-weight:bold;">Pago seguro: paypal.me/RaudyManzueta/20</p>
        </div>
    </body>
    </html>
    """)
