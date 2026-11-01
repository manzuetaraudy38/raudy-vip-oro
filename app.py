from flask import Flask
app = Flask(__name__)

PAYPAL = "https://www.paypal.me/RaudyManzueta/20"

# HOME - LOS 2 BOTONES
@app.route("/")
def home():
    return f"""
    <body style='background:black;color:gold;text-align:center;padding-top:30px;font-family:Arial'>
    <h1>RAUDY VIP - NIVEL DIOS</h1>
    <a href='/tc' style='background:gold;color:black;padding:20px 40px;text-decoration:none;font-size:20px;border-radius:10px;margin:10px;display:inline-block'>💰 VIP ORO</a><br><br>
    <a href='/acciones' style='background:#00ff00;color:black;padding:20px 40px;text-decoration:none;font-size:20px;border-radius:10px;margin:10px;display:inline-block'>📈 VIP ACCIONES USA</a><br><br>
    <a href='{PAYPAL}' style='background:#0070ba;color:white;padding:15px 30px;text-decoration:none;border-radius:10px'>PAGAR VIP</a>
    </body>
    """

# TU PAGINA DE ORO (LA QUE YA TE FUNCIONA)
@app.route("/tc")
def tc():
    return f"""
    <html><body style='background:black;color:white;text-align:center;font-family:Arial;margin:0'>
    <h1 style='color:gold;padding:10px'>RAUDY VIP - NIVEL DIOS</h1>
    <div style='border:2px solid gold;padding:10px;color:gold;margin:10px;border-radius:10px'>ORO: $3890.97 | EUR: 1.1174 | GBP: 1.33297</div>
    <div style='background:gold;padding:15px;margin:10px;font-size:20px;color:black;font-weight:bold;border-radius:10px'>ORO: SENAL VIP: ESPERA - 62%<br><span style='font-size:13px'>LATERAL RSI 70 | MA R:3892.28 MA L:3892.99</span></div>
    <div style='display:flex;justify-content:space-around;margin:10px'><div style='background:#00ff00;color:black;padding:15px;border-radius:10px;width:40%'><b>EURUSD</b><br>COMPRA<br>79%</div><div style='background:red;color:white;padding:15px;border-radius:10px;width:40%'><b>GBPUSD</b><br>VENTA<br>74%</div></div>
    <div style='margin:15px'><a href='/' style='background:gold;color:black;padding:10px 20px;text-decoration:none;border-radius:5px;margin:5px'>RECARGAR</a><a href='https://wa.me/41766000000' style='background:#00ff00;color:black;padding:10px 20px;text-decoration:none;border-radius:5px;margin:5px'>WHATSAPP SENAL</a></div>
    <a href='/acciones' style='color:#00ff00;font-size:18px'>Ir a ACCIONES USA →</a><br><br>
    <a href='{PAYPAL}' style='color:#0070ba'>PAGAR VIP</a>
    </body></html>
    """

# NUEVA PAGINA DE ACCIONES USA
@app.route("/acciones")
def acciones():
    return f"""
    <html><body style='background:black;color:white;text-align:center;font-family:Arial'>
    <h1 style='color:#00ff00'>RAUDY VIP - ACCIONES USA</h1>
    <div style='background:gold;color:black;padding:12px;margin:10px;border-radius:10px;font-weight:bold'>AAPL $255.30 → VENTA 65% - BAJISTA</div>
    <div style='background:gold;color:black;padding:12px;margin:10px;border-radius:10px;font-weight:bold'>TSLA $410.20 → COMPRA 75% - ALCISTA</div>
    <div style='background:gold;color:black;padding:12px;margin:10px;border-radius:10px;font-weight:bold'>NVDA $180.50 → ESPERA 60% - LATERAL</div>
    <div style='background:gold;color:black;padding:12px;margin:10px;border-radius:10px;font-weight:bold'>SPY $580.00 → COMPRA 80% - ALCISTA</div>
    <div style='background:gold;color:black;padding:12px;margin:10px;border-radius:10px;font-weight:bold'>META $480.00 → VENTA 70% - BAJISTA</div>
    <br>
    <a href='/tc' style='background:gold;color:black;padding:10px 20px;text-decoration:none;border-radius:5px;margin:5px'>← VOLVER ORO</a>
    <a href='/' style='background:white;color:black;padding:10px 20px;text-decoration:none;border-radius:5px;margin:5px'>HOME</a>
    <br><br>
    <a href='{PAYPAL}' style='background:#0070ba;color:white;padding:15px 30px;text-decoration:none;border-radius:10px'>PAGAR COMBO CHF 30</a>
    </body></html>
    """

if __name__ == "__main__":
    app.run()
