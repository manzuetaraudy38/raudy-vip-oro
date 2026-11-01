from flask import Flask, render_template_string
import random

app = Flask(__name__)

@app.route('/')
def inicio():
    html = """
    <body style="background:black; color:gold; text-align:center; font-family:Arial; padding:50px;">
        <h1>RAUDY VIP ORO</h1>
        <h2>Tu plataforma profesional</h2>
        <br><br>
        <a href="/tc" style="background:gold; color:black; padding:20px 40px; text-decoration:none; font-weight:bold; border-radius:10px; font-size:22px;">
            ENTRAR AL MERCADO VIP
        </a>
    </body>
    """
    return render_template_string(html)

@app.route('/tc')
def mercado():
    precio_oro = round(random.uniform(3865, 3895), 2)
    eurusd = round(random.uniform(1.1150, 1.1190), 5)
    rsi = random.randint(35, 75)
    ma_rapida = round(precio_oro + random.uniform(-5, 5), 2)
    ma_lenta = round(precio_oro + random.uniform(-8, 8), 2)
    
    if ma_rapida > ma_lenta and rsi > 52:
        senal = "COMPRA"
        color_senal = "#00ff00"
        emoji = "COMPRA"
        texto = "TENDENCIA ALCISTA - RSI %s" % rsi
        confianza = random.randint(78, 92)
    elif ma_rapida < ma_lenta and rsi < 48:
        senal = "VENTA"
        color_senal = "#ff0000"
        emoji = "VENTA"
        texto = "TENDENCIA BAJISTA - RSI %s" % rsi
        confianza = random.randint(75, 89)
    else:
        senal = "ESPERA"
        color_senal = "gold"
        emoji = "ESPERA"
        texto = "MERCADO LATERAL - RSI %s" % rsi
        confianza = random.randint(65, 75)

    html = """
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="background:#050505; margin:0; padding:10px; font-family:Arial;">
        <h2 style="color:gold; text-align:center;">RAUDY VIP MERCADO</h2>
        <div style="border:2px solid gold; border-radius:12px; padding:10px; text-align:center; color:gold; background:#111; margin-bottom:10px;">
            ORO: $%s | EURUSD: %s<br>
            <span style="font-size:11px; color:#aaa;">MA Rapida: %s | MA Lenta: %s | RSI: %s</span>
        </div>
        <div style="border:3px solid %s; background:%s; color:black; border-radius:15px; padding:15px; text-align:center; margin-bottom:10px; font-weight:bold;">
            <div style="font-size:26px;">SENAL VIP: %s</div>
            <div style="font-size:14px; margin-top:6px;">%s</div>
            <div style="font-size:18px; margin-top:8px; background:black; color:%s; display:inline-block; padding:5px 15px; border-radius:20px;">CONFIANZA: %s%%</div>
        </div>
        <div style="text-align:center; margin-bottom:10px;">
            <a href="/tc" style="background:gold; color:black; padding:12px 25px; text-decoration:none; font-weight:bold; border-radius:10px;">RECARGAR SENAL</a>
        </div>
        <div style="height:600px; border:1px solid gold; border-radius:10px;">
            <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_123&symbol=OANDA%%3AXAUUSD&interval=15&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=000&studies=[]&theme=dark&style=1&timezone=Etc%%2FUTC&studies_overrides={}&overrides={}&enabled_features=[]&disabled_features=[]&locale=es&utm_source=widget&utm_medium=widget&utm_campaign=chart&utm_term=OANDA%%3AXAUUSD" style="width:100%%; height:100%%; border:0;"></iframe>
        </div>
    </body>
    </html>
    """ % (precio_oro, eurusd, ma_rapida, ma_lenta, rsi, color_senal, color_senal, senal, texto, color_senal, confianza)
    
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
