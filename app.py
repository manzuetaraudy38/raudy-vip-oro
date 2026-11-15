from flask import Flask
import os, requests, time
app = Flask(__name__)

# ROBOT BOLSA - RAUDY VIP PRO
# Jala info real de Yahoo Finance (Bolsa de USA)

TICKERS = {
    "META": "META",
    "APPLE": "AAPL",
    "TESLA": "TSLA",
    "NVIDIA": "NVDA",
    "MICROSOFT": "MSFT",
    "AMAZON": "AMZN",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI",
    "ORO": "GC=F",
    "CAFE": "KC=F",
    "CACAO": "CC=F",
}

def get_bolsa(symbol):
    try:
        # Yahoo Finance API - Bolsa real
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1m"
        headers = {"User-Agent": "Mozilla/5.0"}
        d = requests.get(url, headers=headers, timeout=10).json()
        meta = d['chart']['result'][0]['meta']
        precio = meta['regularMarketPrice']
        anterior = meta['previousClose']
        cambio = precio - anterior
        porc = (cambio / anterior * 100) if anterior else 0

        # Velas del dia para señal
        timestamps = d['chart']['result'][0]['timestamp']
        quotes = d['chart']['result'][0]['indicators']['quote'][0]
        closes = [c for c in quotes['close'] if c is not None]
        if len(closes) >= 5:
            # Ultimos 5 precios para ver tendencia
            ultimos = closes[-5:]
            verdes = sum(1 for i in range(1, len(ultimos)) if ultimos[i] > ultimos[i-1])
        else:
            verdes = 3

        return {
            "precio": precio,
            "cambio": cambio,
            "porc": porc,
            "verdes": verdes,
            "max": meta.get('regularMarketDayHigh'),
            "min": meta.get('regularMarketDayLow'),
        }
    except Exception as e:
        return None

@app.route("/")
def home():
    html = """
    <style>
    body{background:#0A0E14;color:#fff;font-family:Arial;padding:15px;margin:0}
    h1{font-size:24px} .top{background:#111722;padding:15px;border-radius:15px;border:1px solid #FFD700}
    .c{background:#111722;border:1px solid #1E2A3A;border-radius:15px;padding:15px;margin:10px 0}
    .up{color:#00FF88} .down{color:#FF4757}
    .badge{padding:5px 10px;border-radius:20px;font-weight:800;font-size:12px}
    </style>
    <div class='top'><h1>🤖 ROBOT BOLSA • RAUDY VIP PRO 👑</h1>
    <p>Info real de Wall Street • Yahoo Finance • Actualizado: """ + time.strftime("%H:%M:%S") + """</p>
    <p>● LIVE • BOLSA DE NEW YORK</p></div>
    """

    for nombre, symbol in TICKERS.items():
        data = get_bolsa(symbol)
        if not data:
            html += f"<div class='c'><h2>{nombre}</h2><p>Sin conexión, reintentando...</p></div>"
            continue

        color = "up" if data['porc'] >= 0 else "down"
        flecha = "🟢 ▲" if data['porc'] >= 0 else "🔴 ▼"
        if data['verdes'] >= 3:
            senal = "🟢 COMPRA - TENDENCIA ALCISTA"
            bg = "#00FF88;color:#000"
        elif data['verdes'] <= 1:
            senal = "🔴 VENTA - TENDENCIA BAJISTA"
            bg = "#FF4757;color:#fff"
        else:
            senal = "🟡 ESPERA - MERCADO MIXTO"
            bg = "#1A1A1A;color:#FFD700;border:1px solid #FFD700"

        html += f"""
        <div class='c'>
        <h2>{nombre} <span style='font-size:12px;color:#888'>{symbol}</span></h2>
        <h1 class='{color}'>{flecha} ${data['precio']:,.2f}</h1>
        <p class='{color}'>{data['cambio']:+.2f} ({data['porc']:+.2f}%) hoy</p>
        <p style='color:#9AA4B2;font-size:12px'>Máximo día: ${data['max']:,.2f} • Mínimo día: ${data['min']:,.2f}</p>
        <div class='badge' style='background:{bg}'>{senal}</div>
        </div>
        """

    html += "<p style='color:#888;font-size:11px'>Robot de información pública de la Bolsa. Fuente: Yahoo Finance. No es consejo financiero. Opera con poquito.</p>"
    html += "<script>setTimeout(()=>location.reload(),30000)</script>"
    return html

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
