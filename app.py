from flask import Flask, render_template_string
import random

app = Flask(__name__)

@app.route('/')
def inicio():
    html = """
    <body style="background:black; color:gold; text-align:center; padding:30px; font-family:Arial;">
        <h1>RAUDY VIP ORO - NIVEL DIOS</h1>
        <h2>3 Mercados VIP + WhatsApp</h2>
        <p style="color:white;">ORO - NAS100 - BTC | Señales en Vivo</p>
        <br><br>
        <a href="/tc" style="background:gold; color:black; padding:20px 40px; font-size:20px; font-weight:bold; text-decoration:none; border-radius:10px;">
            ENTRAR AL MERCADO VIP GRATIS
        </a>
        <br><br><br>
        <a href="/pagar" style="background:#25D366; color:white; padding:20px 40px; font-size:22px; font-weight:bold; text-decoration:none; border-radius:10px; display:inline-block;">
            💳 PAGAR CHF 20 VIP - ACCESO TOTAL
        </a>
        <br><br>
        <p style="color:gray;">Geneva | Pago seguro por TWINT / PayPal</p>
    </body>
    """
    return render_template_string(html)

@app.route('/tc')
def mercado():
    oro = round(random.uniform(3865, 3895), 2)
    nas = round(random.uniform(21500, 21800), 2)
    btc = round(random.uniform(67000, 69000), 2)
    html = f"""
    <body style="background:black; color:gold; text-align:center; padding:20px;">
        <h1>MERCADOS VIP EN VIVO</h1>
        <h2 style="color:white;">ORO: {oro}</h2>
        <h2 style="color:white;">NAS100: {nas}</h2>
        <h2 style="color:white;">BTC: {btc}</h2>
        <br><br>
        <a href="/" style="color:gold;">Volver</a>
    </body>
    """
    return render_template_string(html)

@app.route('/pagar')
def pagar():
    html = """
    <body style="background:black; color:white; text-align:center; padding:30px; font-family:Arial;">
        <h1 style="color:gold;">ACTIVA TU VIP ORO - CHF 20</h1>
        <p>Pago único - Acceso de por vida</p>
        <br>
        <div style="background:#222; padding:20px; border-radius:15px;">
            <h3 style="color:gold;">1. TWINT: +41 7X XXX XX XX</h3>
            <h3 style="color:gold;">2. PayPal: raudyvip@gmail.com</h3>
            <p>Concepto: VIP ORO + tu número de WhatsApp</p>
        </div>
        <br><br>
        <a href="https://wa.me/417XXXXXXXX?text=Hola%20Raudy%20ya%20pague%20CHF%2020%20VIP%20ORO" style="background:#25D366; color:white; padding:20px 40px; font-size:20px; font-weight:bold; text-decoration:none; border-radius:10px;">
            ✅ YA PAGUÉ - ENVIAR COMPROBANTE POR WHATSAPP
        </a>
        <br><br><br>
        <a href="/" style="color:gray;">Volver al inicio</a>
    </body>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
