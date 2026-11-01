from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    html = """
    <html><body style='background:black;color:white;text-align:center;padding:10px;font-family:Arial'>
    <h1 style='color:gold'>RAUDY VIP - ORO</h1>
    <div style='border:2px solid gold;padding:8px;border-radius:10px'>ORO: $3874.73 | EUR: 1.11 | GBP: 1.33</div>
    <div style='background:red;color:black;padding:12px;margin:8px;border-radius:10px;font-weight:bold'>ORO: VENTA - 88%</div>
    <div style='margin:10px'>
    <a href='/tc' style='background:gold;color:black;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20SENAL%20VIP' style='background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP</a>
    </div>
    <div style='border:2px solid gold;border-radius:10px;overflow:hidden;margin:10px;height:500px'>
    <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=15&theme=dark" style="width:100%;height:100%;" frameborder="0"></iframe>
    </div>
    <p>WHATSAPP: 076 757 40 50</p>
    <a href='/acciones' style='color:#00ff00;margin:5px'>ACCIONES</a>
    <a href='/crypto' style='color:orange;margin:5px'>CRYPTO</a>
    <br><br>
    <a href='https://www.paypal.me/RaudyManzueta/20' style='background:#0070ba;color:white;padding:12px 25px;border-radius:20px;text-decoration:none'>PAGAR CHF 20</a>
    </body></html>
    """
    return html

@app.route("/tc")
def tc():
    html = """
    <html><body style='background:black;color:white;text-align:center;padding:10px;font-family:Arial'>
    <h1 style='color:gold'>RAUDY VIP - /tc</h1>
    <div style='border:2px solid gold;padding:8px;border-radius:10px'>ORO: $3874.73 | EUR: 1.11684 | GBP: 1.33144</div>
    <div style='background:red;color:black;padding:12px;margin:8px;border-radius:10px;font-weight:bold'>ORO: SENAL VIP: VENTA - 88%</div>
    <div style='display:flex;gap:8px;padding:5px'>
    <div style='flex:1;background:gold;color:black;padding:10px;border-radius:10px'><b>EURUSD<br>ESPERA 63%</b></div>
    <div style='flex:1;background:red;color:white;padding:10px;border-radius:10px'><b>GBPUSD<br>VENTA 73%</b></div>
    </div>
    <div style='margin:10px'>
    <a href='/tc' style='background:gold;color:black;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20SENAL%20VIP' style='background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP</a>
    </div>
    <div style='border:2px solid gold;border-radius:10px;overflow:hidden;margin:10px;height:500px'>
    <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=15&theme=dark" style="width:100%;height:100%;" frameborder="0"></iframe>
    </div>
    <p>WHATSAPP: 076 757 40 50</p>
    </body></html>
    """
    return html

@app.route("/acciones")
def acciones():
    html = """
    <html><body style='background:black;color:white;text-align:center;padding:10px'>
    <h1 style='color:#00ff00'>RAUDY VIP - ACCIONES</h1>
    <div style='background:gold;color:black;padding:12px;margin:5px;border-radius:10px'>TESLA: COMPRA 88%</div>
    <div style='background:gold;color:black;padding:12px;margin:5px;border-radius:10px'>APPLE: COMPRA 82%</div>
    <div style='border:2px solid #00ff00;border-radius:10px;overflow:hidden;margin:10px;height:500px'>
    <iframe src="https://s.tradingview.com/widgetembed/?symbol=NASDAQ:TSLA&interval=15&theme=dark" style="width:100%;height:100%;" frameborder="0"></iframe>
    </div>
    <a href='/' style='color:gold'>ORO</a> | <a href='/crypto' style='color:orange'>CRYPTO</a>
    </body></html>
    """
    return html

@app.route("/crypto")
def crypto():
    html = """
    <html><body style='background:black;color:white;text-align:center;padding:10px;font-family:Arial'>
    <h1 style='color:orange'>RAUDY VIP - CRYPTO</h1>
    <div style='border:2px solid orange;padding:8px;border-radius:10px'>BTC: $112K | ETH: $3.9K | SOL: $198</div>
    <div style='background:orange;color:black;padding:12px;margin:8px;border-radius:10px;font-weight:bold'>BTC: COMPRA FUERTE - 91%</div>
    <div style='display:flex;gap:8px;padding:5px'>
    <div style='flex:1;background:gold;color:black;padding:10px;border-radius:10px'><b>ETH<br>COMPRA 87%</b></div>
    <div style='flex:1;background:red;color:white;padding:10px;border-radius:10px'><b>SOL<br>ESPERA 78%</b></div>
    </div>
    <div style='margin:10px'>
    <a href='/crypto' style='background:orange;color:black;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20SENAL%20CRYPTO' style='background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP</a>
    </div>
    <div style='border:2px solid orange;border-radius:10px;overflow:hidden;margin:10px;height:500px'>
    <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=15&theme=dark" style="width:100%;height:100%;" frameborder="0"></iframe>
    </div>
    <p>WHATSAPP: 076 757 40 50</p>
    <a href='/' style='color:gold'>ORO</a> | <a href='/acciones' style='color:#00ff00'>ACCIONES</a>
    <br><br>
    <a href='https://www.paypal.me/RaudyManzueta/20' style='background:#0070ba;color:white;padding:12px 25px;border-radius:20px;text-decoration:none'>PAGAR VIP CHF 20</a>
    </body></html>
    """
    return html

if __name__ == "__main__":
    app.run()
