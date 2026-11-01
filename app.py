from flask import Flask
import random

app = Flask(__name__)
PAYPAL_LINK = "https://www.paypal.me/RaudyManzueta/20"

# PAGINA PRINCIPAL CON 2 BOTONES
@app.route("/")
def home():
    return f"""
    <html><body style='background:black;color:gold;text-align:center;padding-top:50px;font-family:Arial'>
    <h1>RAUDY VIP - NIVEL DIOS</h1>
    <a href='/tc' style='background:gold;color:black;padding:20px 40px;text-decoration:none;font-size:22px;border-radius:10px;margin:10px;display:inline-block'>💰 VIP ORO</a><br><br>
    <a href='/acciones' style='background:#00ff00;color:black;padding:20px 40px;text-decoration:none;font-size:22px;border-radius:10px;margin:10px;display:inline-block'>📈 VIP ACCIONES USA</a><br><br><br>
    <a href='{PAYPAL_LINK}' style='background:#0070ba;color:white;padding:15px 30px;text-decoration:none;border-radius:10px'>PAGAR VIP CHF 20 - {PAYPAL_LINK}</a>
    <p style='color:white;margin-top:30px'>Educativo, no asesoría financiera. Trading con riesgo.</p>
    </body></html>
    """

# TU PAGINA DE ORO (LA QUE YA TIENES - NO TOCAMOS LOGICA)
@app.route("/tc")
def tc():
    oro = 3874.73
    senal = "VENTA - 88%" if oro < 3890 else "COMPRA - 90%"
    color = "red" if "VENTA" in senal else "green"
    return f"""
    <html><body style='background:black;color:white;text-align:center'>
    <h1 style='color:gold'>RAUDY VIP - NIVEL DIOS</h1>
    <div style='border:2px solid gold;padding:10px;color:gold'>ORO: ${oro} | EUR: 1.11684 | GBP: 1.33144</div>
    <div style='background:{color};padding:15px;margin:15px 0;font-size:22px;color:black;font-weight:bold'>ORO: SENAL VIP: {senal}<br><span style='font-size:14px'>BAJISTA RSI 37 | MA R:3870.87 MA L:3881.87</span></div>
    <a href='/' style='color:gold'>← Volver</a> | <a href='{PAYPAL_LINK}' style='background:#0070ba;color:white;padding:10px 20px;text-decoration:none;border-radius:10px'>PAGAR VIP CHF 20</a>
    </body></html>
    """

# NUEVA PAGINA DE ACCIONES
@app.route("/acciones")
def acciones():
    acciones_lista = ["AAPL $255.30 VENTA 65%", "TSLA $410.20 COMPRA 75%", "NVDA $180.50 ESPERA 60%"]
    html_acc = "".join([f"<div style='background:gold;color:black;padding:10px;margin:10px;border-radius:10px'>{a}</div>" for a in acciones_lista])
    return f"""
    <html><body style='background:black;color:white;text-align:center'>
    <h1 style='color:#00ff00'>RAUDY VIP - ACCIONES USA</h1>
    {html_acc}
    <p>Señales AAPL, TSLA, NVDA, SPY, META</p>
    <a href='/' style='color:gold'>← Volver ORO</a><br><br>
    <a href='{PAYPAL_LINK}' style='background:#0070ba;color:white;padding:15px 30px;text-decoration:none;border-radius:10px'>PAGAR VIP COMBO CHF 30</a>
    </body></html>
    """

if __name__ == "__main__":
    app.run()
