from flask import Flask
app = Flask(__name__)

PAYPAL = "https://www.paypal.me/RaudyManzueta/20"
WHATSAPP = "https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20la%20SENAL%20VIP"

@app.route("/")
def home():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:20px;font-family:Arial'>
    <h1 style='color:gold'>RAUDY VIP - NIVEL DIOS</h1>
    <div style='border:2px solid gold;padding:10px;margin:10px'>ORO: $3881.04 | EUR: 1.1163 | GBP: 1.33246</div>
    <div style='background:gold;color:black;padding:15px;margin:10px;border-radius:10px'><b>ORO: SEÑAL VIP: ESPERA - 73%</b></div>
    <div style='display:flex;justify-content:center;gap:10px'>
    <div style='background:#00ff00;color:black;padding:15px;border-radius:10px'><b>EURUSD<br>COMPRA 84%</b></div>
    <div style='background:red;color:black;padding:15px;border-radius:10px'><b>GBPUSD<br>VENTA 76%</b></div>
    </div>
    <br><div style='margin:15px'>
    <a href='/' style='background:gold;color:black;padding:15px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP SEÑAL</a></div>
    <br>
    <a href='/acciones' style='color:#00ff00;margin:5px'>ACCIONES USA →</a>
    <a href='/crypto' style='color:orange;margin:5px'>CRYPTO VIP →</a>
    <a href='/tc' style='color:gold;margin:5px'>ORO /tc</a><br><br>
    <a href='{PAYPAL}' style='background:#0070ba;color:white;padding:12px 25px;border-radius:20px;text-decoration:none'>PAGAR CHF 20 PAYPAL</a>
    </body></html>
    """

@app.route("/acciones")
def acciones():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:20px'>
    <h1 style='color:#00ff00'>RAUDY VIP - ACCIONES USA</h1>
    <div style='background:gold;color:black;padding:15px;margin:5px'>TESLA: COMPRA 88%</div>
    <div style='background:gold;color:black;padding:15px;margin:5px'>APPLE: COMPRA 82%</div>
    <div style='background:gold;color:black;padding:15px;margin:5px'>NVIDIA: ESPERA 75%</div>
    <br>
    <a href='/' style='background:gold;color:black;padding:15px;border-radius:10px;text-decoration:none'>ORO</a>
    <a href='/crypto' style='background:orange;color:black;padding:15px;border-radius:10px;text-decoration:none;margin-left:10px'>CRYPTO</a>
    <br><br>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:15px;border-radius:20px;text-decoration:none'>WHATSAPP SEÑAL</a>
    </body></html>
    """

@app.route("/crypto")
def crypto():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:20px;font-family:Arial'>
    <h1 style='color:orange'>RAUDY VIP - CRYPTO</h1>
    <div style='background:orange;color:black;padding:15px;margin:8px;border-radius:10px;font-weight:bold'>BITCOIN BTC: COMPRA FUERTE 91%<br>Soporte $67,000</div>
    <div style='background:#00ff00;color:black;padding:15px;margin:8px;border-radius:10px;font-weight:bold'>ETHEREUM ETH: COMPRA 87%<br>Objetivo $4,200</div>
    <div style='background:gold;color:black;padding:15px;margin:8px;border-radius:10px;font-weight:bold'>SOLANA SOL: ESPERA 78%<br>RSI 52 - LATERAL</div>
    <br>
    <a href='/' style='background:gold;color:black;padding:15px;border-radius:10px;text-decoration:none'>VOLVER ORO</a>
    <a href='/acciones' style='background:#00ff00;color:black;padding:15px;border-radius:10px;text-decoration:none;margin-left:10px'>ACCIONES</a>
    <br><br><br>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:20px 40px;border-radius:30px;text-decoration:none;font-size:20px;font-weight:bold'>QUIERO SEÑAL CRYPTO - WHATSAPP</a>
    <br><br><br>
    <a href='{PAYPAL}' style='background:#0070ba;color:white;padding:12px 25px;border-radius:20px;text-decoration:none'>PAGAR VIP CHF 20</a>
    </body></html>
    """

@app.route("/tc")
def tc():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:20px'>
    <h1 style='color:gold'>RAUDY VIP - NIVEL DIOS /tc</h1>
    <h2>WHATSAPP: 076 757 40 50</h2>
    <br>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:20px 40px;border-radius:30px;text-decoration:none;font-size:22px;font-weight:bold'>WHATSAPP SEÑAL</a>
    <br><br><br>
    <a href='/' style='color:gold;margin:5px'>HOME</a>
    <a href='/acciones' style='color:#00ff00;margin:5px'>ACCIONES</a>
    <a href='/crypto' style='color:orange;margin:5px'>CRYPTO</a>
    </body></html>
    """

if __name__ == "__main__":
    app.run()
