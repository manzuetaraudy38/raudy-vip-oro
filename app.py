from flask import Flask, render_template_string
import random

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template_string("""
    <body style="background:black; color:gold; text-align:center; font-family:Arial; padding:50px;">
        <h1>RAUDY VIP ORO</h1>
        <h2>Bienvenido a tu plataforma VIP</h2>
        <br>
        <a href="/tc" style="background:gold; color:black; padding:20px 40px; text-decoration:none; font-weight:bold; border-radius:10px; font-size:20px;">
            VER MERCADO COMPLETO
        </a>
    </body>
    """)

@app.route('/tc')
def mercado():
    precio_oro = round(random.uniform(3870, 3885), 2)
    eurusd = round(random.uniform(1.11, 1.12), 5)
    gbpusd = round(random.uniform(1.33, 1.34), 5)
    
    senal = random.choice(["COMPRA", "VENTA", "ESPERA"])
    if senal == "COMPRA":
        color_senal = "#00ff00"
        emoji = "🟢"
        texto = "COMPRA - TENDENCIA ALCISTA"
    elif senal == "VENTA":
        color_senal = "#ff0000"
        emoji = "🔴"
        texto = "VENTA - TENDENCIA BAJISTA"
    else:
        color_senal = "gold"
        emoji = "🟡"
        texto = "ESPERA - MERCADO LATERAL"

    return render_template_string(f"""
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="background:black; margin:0; padding:10px; font-family:Arial;">
        <h2 style="color:gold; text-align:center;">RAUDY VIP MERCADO</h2>
        <div style="border:2px solid gold; border-radius:15px; padding:10px; text-align:center; color:gold; margin-bottom:10px;">
            ORO: ${precio_oro}<br>
            EURUSD: {eurusd}<br>
            GBPUSD: {gbpusd}
        </div>
        <div style="border:3px solid {color_senal}; background:{color_senal}; color:black; border-radius:15px; padding:15px; text-align:center; margin-bottom:10px; font-weight:bold;">
            <div style="font-size:28px;">{emoji} SENAL VIP: {senal} {emoji}</div>
            <div style="font-size:16px; margin-top:5px;">{texto}</div>
        </div>
        <div style="height:600px;">
            <div class="tradingview-widget-container">
              <div id="tradingview_chart" style="height:600px;"></div>
              <script type="text/javascript" src="https://s.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget({{
                "autosize": true,
                "symbol": "OANDA:XAUUSD",
                "interval": "15",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "es",
                "container_id": "tradingview_chart"
              }});
              </script>
            </div>
        </div>
        <div style="text-align:center; margin-top:15px;">
            <a href="/" style="background:gold; color:black; padding:15px 30px; text-decoration:none; font-weight:bold; border-radius:10px;">
                VOLVER AL INICIO
            </a>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
