from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>body{background:#0a0a0a;color:gold;text-align:center;font-family:Arial;padding:20px}
    .box{border:2px solid gold;border-radius:20px;padding:20px;margin:15px 0;background:#111}
    .btn{background:gold;color:black;padding:15px 30px;border-radius:15px;font-weight:bold;text-decoration:none;display:inline-block;margin-top:20px}
    </style></head><body>
    <h1>👑 RAUDY VIP ORO 👑</h1><p style="color:#0f0">● LIVE ✅</p>
    <div class="box"><h2>ORO: $3876.40</h2><p>Nivel compra VIP: 3890</p></div>
    <div class="box"><p>EURUSD: 1.11658 | GBPUSD: 1.33853</p></div>
    <div class="box"><p>BOT ACTIVO 24/7</p></div>
    <a class="btn" href="/tc">VER MERCADO COMPLETO</a>
    </body></html>
    """)

@app.route('/tc')
def mercado():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>body{background:#000;color:gold;font-family:Arial;margin:0;padding:10px}
    h2{text-align:center}
    .info{background:#111;border:2px solid gold;border-radius:15px;padding:15px;margin:10px 0;text-align:center}
    .btn{background:gold;color:black;padding:12px 25px;border-radius:10px;font-weight:bold;text-decoration:none;display:inline-block;text-align:center}
    </style></head><body>
    <h2>🔥 RAUDY VIP MERCADO 🔥</h2>
    <div class="info">💰 ORO: $3876.40<br>EURUSD: 1.11658<br>GBPUSD: 1.33853</div>
    <div class="tradingview-widget-container" style="height:600px">
      <div id="tradingview_chart" style="height:600px"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({"autosize": true,"symbol": "OANDA:XAUUSD","interval": "15","timezone": "Etc/UTC","theme": "dark","style": "1","locale": "es","toolbar_bg": "#f1f3f6","enable_publishing": false,"allow_symbol_change": true,"container_id": "tradingview_chart"});
      </script>
    </div>
    <div style="text-align:center;margin-top:20px"><a class="btn" href="/">⬅ VOLVER AL INICIO</a></div>
    </body></html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
