from flask import Flask
app = Flask(__name__)

PAYPAL = "https://www.paypal.me/RaudyManzueta/20"
WHATSAPP = "https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20la%20SENAL%20VIP"
NUMERO_TEXTO = "076 757 40 50"

@app.route("/")
def home():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:10px;font-family:Arial;margin:0'>
    <h1 style='color:gold;margin:10px'>RAUDY VIP - NIVEL DIOS</h1>
    <div style='border:2px solid gold;padding:8px;border-radius:10px;margin:10px;color:gold;font-weight:bold'>
    ORO: $3874.73 | EUR: 1.11684 | GBP: 1.33144
    </div>
    <div style='background:red;color:black;padding:12px;margin:8px;border-radius:15px;font-weight:bold'>
    ORO: SEÑAL VIP: VENTA - 88%<br><span style='font-size:12px'>BAJISTA RSI 37 | MA R:3870.87 MA L:3881.87</span>
    </div>
    <div style='display:flex;gap:8px;padding:5px'>
    <div style='flex:1;background:gold;color:black;padding:15px;border-radius:10px'><b>EURUSD<br>ESPERA<br>63%</b></div>
    <div style='flex:1;background:red;color:white;padding:15px;border-radius:10px'><b>GBPUSD<br>VENTA<br>73%</b></div>
    </div>
    <div style='margin:10px'>
    <a href='/' style='background:gold;color:black;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP SEÑAL</a>
    </div>
    <div style='border:2px solid gold;border-radius:10px;overflow:hidden;margin:10px;height:480px'>
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_gold&symbol=OANDA%3AXAUUSD&interval=15&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=black&studies=[]&theme=dark&style=1&timezone=Europe%2FZurich&locale=es&colorTheme=dark&width=100%&height=100%" style="width:100%;height:100%;" frameborder="0" scrolling="no"></iframe>
    </div>
    <div style='margin:15px'>
    <a href='/acciones' style='color:#00ff00;margin:5px;text-decoration:none'>ACCIONES →</a>
    <a href='/crypto' style='color:orange;margin:5px;text-decoration:none'>CRYPTO →</a>
    <a href='/tc' style='color:gold;margin:5px;text-decoration:none'>/tc</a>
    </div>
    <a href='{PAYPAL}' style='background:#0070ba;color:white;padding:12px 25px;border-radius:20px;text-decoration:none'>PAGAR CHF 20 PAYPAL</a>
    <br><br>
    </body></html>
    """

@app.route("/tc")
def tc():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:10px;font-family:Arial;margin:0'>
    <h1 style='color:gold;margin:10px'>RAUDY VIP - NIVEL DIOS</h1>
    <div style='border:2px solid gold;padding:8px;border-radius:10px;margin:10px;color:gold;font-weight:bold'>
    ORO: $3874.73 | EUR: 1.11684 | GBP: 1.33144
    </div>
    <div style='background:red;color:black;padding:12px;margin:8px;border-radius:15px;font-weight:bold'>
    ORO: SEÑAL VIP: VENTA - 88%<br><span style='font-size:12px'>BAJISTA RSI 37 | MA R:3870.87 MA L:3881.87</span>
    </div>
    <div style='display:flex;gap:8px;padding:5px'>
    <div style='flex:1;background:gold;color:black;padding:15px;border-radius:10px'><b>EURUSD<br>ESPERA<br>63%</b></div>
    <div style='flex:1;background:red;color:white;padding:15px;border-radius:10px'><b>GBPUSD<br>VENTA<br>73%</b></div>
    </div>
    <div style='margin:10px'>
    <a href='/tc' style='background:gold;color:black;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP SEÑAL</a>
    </div>
    <div style='border:2px solid gold;border-radius:10px;overflow:hidden;margin:10px;height:500px'>
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_tc&symbol=OANDA%3AXAUUSD&interval=15&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=black&studies=[]&theme=dark&style=1&timezone=Europe%2FZurich&locale=es&colorTheme=dark&width=100%&height=100%" style="width:100%;height:100%;" frameborder="0" scrolling="no"></iframe>
    </div>
    <p style='color:gray;font-size:12px'>WHATSAPP: {NUMERO_TEXTO}</p>
    </body></html>
    """

@app.route("/acciones")
def acciones():
    return f"""
    <html><body style='background:black;color:white;text-align:center;padding:10px;font-family:Arial;margin:0'>
    <h1 style='color:#00ff00;margin:10px'>RAUDY VIP - ACCIONES USA</h1>
    <div style='background:gold;color:black;padding:12px;margin:8px;border-radius:10px;font-weight:bold'>TESLA TSLA: COMPRA 88%</div>
    <div style='background:gold;color:black;padding:12px;margin:8px;border-radius:10px;font-weight:bold'>APPLE AAPL: COMPRA 82%</div>
    <div style='background:#00ff00;color:black;padding:12px;margin:8px;border-radius:10px;font-weight:bold'>NVIDIA NVDA: COMPRA 90%</div>
    <div style='margin:10px'>
    <a href='/acciones' style='background:#00ff00;color:black;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold'>RECARGAR</a>
    <a href='{WHATSAPP}' style='background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;font-weight:bold;margin-left:10px'>WHATSAPP SEÑAL</a>
    </div>
    <div style='border:2px solid #00ff00;border-radius:
