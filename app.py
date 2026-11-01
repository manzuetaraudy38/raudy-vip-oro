from flask import Flask
app = Flask(__name__)

PAYPAL = "https://www.paypal.me/RaudyManzueta/20"
WHATSAPP = "https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20la%20SENAL%20VIP"

# HOME - LOS 2 BOTONES
@app.route("/")
def home():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:20px;font-family:Arial'>
    <h1 style='color:gold;padding:10px'>RAUDY VIP - NIVEL DIOS</h1>
    <div style='border:2px solid gold;padding:10px;margin:10px'>ORO: $3881.04 | EUR: 1.1163 | GBP: 1.33246</div>
    <div style='background:gold;color:black;padding:15px;margin:10px;border-radius:10px'><b>ORO: SEÑAL VIP: ESPERA - 73%</b><br>LATERAL RSI 46 | MA R:3884.86 MA L:3875.17</div>
    <div style='display:flex;justify-content:center;gap:10px'>
    <div style='background:#00ff00;color:black;padding:15px;border-radius:10px'><b>EURUSD<br>COMPRA<br>84%</b></div>
    <div style='background:red;color:black;padding:15px;border-radius:10px'><b>GBPUSD<br>VENTA<br>76%</b></div>
    </div>
    <br>
    <div style='margin:15px'><a href='/' style='background:gold;color:black;padding:15px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP SEÑAL</a></div>
    <br>
    <a href='/acciones' style='color:#00ff00;font-size:18px'>VER ACCIONES USA →</a><br><br>
    <a href='{PAYPAL}' style='background:#0070ba;color:white;padding:12px 25px;border-radius:20px;text-decoration:none'>PAGAR CHF 20 PAYPAL</a>
    </body></html>
    """

# NUEVA PAGINA DE ACCIONES USA
@app.route("/acciones")
def acciones():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:20px'>
    <h1 style='color:#00ff00'>RAUDY VIP - ACCIONES USA</h1>
    <div style='background:gold;color:black;padding:15px;margin:5px'>TESLA: COMPRA 88%</div>
    <div style='background:gold;color:black;padding:15px;margin:5px'>APPLE: COMPRA 82%</div>
    <div style='background:gold;color:black;padding:15px;margin:5px'>NVIDIA: ESPERA 75%</div>
    <br>
    <a href='/tc' style='background:gold;color:black;padding:15px;border-radius:10px;text-decoration:none'>VOLVER A ORO</a>
    <a href='/' style='background:white;color:black;padding:15px;border-radius:10px;text-decoration:none;margin-left:10px'>HOME</a>
    <br><br>
    <a href='{PAYPAL}' style='background:#0070ba;color:white;padding:12px 25px;border-radius:20px;text-decoration:none'>PAGAR VIP</a>
    <br><br>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:15px;border-radius:20px;text-decoration:none'>WHATSAPP {WHATSAPP}</a>
    </body></html>
    """

@app.route("/tc")
def tc():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:20px'>
    <h1 style='color:gold'>RAUDY VIP - NIVEL DIOS /tc</h1>
    <h2>WHATSAPP CORRECTO: 076 757 40 50</h2>
    <br>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:20px 40px;border-radius:30px;text-decoration:none;font-size:22px;font-weight:bold'>WHATSAPP SEÑAL - AHORA SI ES TU NUMERO</a>
    <br><br><br>
    <a href='/' style='color:gold'>VOLVER HOME</a>
    </body></html>
    """

if __name__ == "__main__":
    app.run()
