from flask import Flask, request
import os, requests, time
app = Flask(__name__)

# --- TU CANDADO, JEFE ---
MI_CUENTA = "169771026"
MI_SERVIDOR = "XMGlobal-MT5 2"

def esta_autorizado():
    return request.args.get("cuenta", "") == MI_CUENTA

def get_oro():
    try:
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD.json", timeout=10).json()
        return float(r['items'][0]['pcurr'])
    except: return None

def get_binance(symbol, intervalo):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={intervalo}&limit=2"
        d = requests.get(url, timeout=10).json()
        v = d[-1]
        return {"open": float(v[1]), "close": float(v[4])}
    except: return None

def get_forex(par):
    try:
        d = requests.get("https://api.frankfurter.app/latest?from=EUR&to=USD,JPY,CHF,CAD,GBP,AUD", timeout=10).json()
        rates = d['rates']
        eur_usd = rates['USD']
        if par == "EUR/USD": return eur_usd
        if par == "GBP/USD": return eur_usd / rates['GBP']
        if par == "AUD/USD": return eur_usd / rates['AUD']
        if par == "USD/JPY": return rates['JPY'] / eur_usd
        if par == "USD/CHF": return rates['CHF'] / eur_usd
        if par == "USD/CAD": return rates['CAD'] / eur_usd
    except: return None

def get_bolsa(symbol_yahoo):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_yahoo}?range=1d&interval=5m"
        headers = {"User-Agent": "Mozilla/5.0"}
        d = requests.get(url, headers=headers, timeout=10).json()
        result = d['chart']['result'][0]
        meta = result['meta']
        precio = meta['regularMarketPrice']
        anterior = meta['previousClose']
        cambio = precio - anterior
        porc = (cambio / anterior * 100) if anterior else 0
        quotes = result['indicators']['quote'][0]
        closes = [c for c in quotes['close'] if c is not None]
        velas = []
        if len(closes) >= 6:
            for i in range(5):
                velas.append({"open": closes[-6+i], "close": closes[-5+i]})
        else:
            for _ in range(5):
                velas.append({"open": anterior, "close": precio})
        return {"precio": precio, "cambio": cambio, "porc": porc, "velas": velas, "max": meta.get('regularMarketDayHigh'), "min": meta.get('regularMarketDayLow')}
    except: return None

def analizar_velas(velas):
    verdes = sum(1 for v in velas if v and v['close'] > v['open'])
    if verdes >= 4: return f"🟢 COMPRA - {verdes}/5 VERDES"
    if 5 - verdes >= 4: return f"🔴 VENTA - {5-verdes}/5 ROJAS"
    return f"🟡 ESPERA - {verdes}/5 VERDES"

ACTIVOS = {
    "ORO XAU/USD": ("PAXGUSDT", "ORO", None),
    "EUR/USD": ("EURUSDT", "FOREX", None),
    "GBP/USD": ("GBPUSDT", "FOREX", None),
    "USD/JPY": ("EURUSDT", "FOREX", None),
    "USD/CHF": ("EURUSDT", "FOREX", None),
    "AUD/USD": ("AUDUSDT", "FOREX", None),
    "USD/CAD": ("EURUSDT", "FOREX", None),
    "META": (None, "BOLSA", "META"),
    "APPLE": (None, "BOLSA", "AAPL"),
    "TESLA": (None, "BOLSA", "TSLA"),
    "NVIDIA": (None, "BOLSA", "NVDA"),
    "S&P 500": (None, "BOLSA", "^GSPC"),
    "NASDAQ": (None, "BOLSA", "^IXIC"),
    "DOW JONES": (None, "BOLSA", "^DJI"),
    "CAFE": (None, "BOLSA", "KC=F"),
    "CACAO": (None, "BOLSA", "CC=F"),
    "ORO BOLSA": (None, "BOLSA", "GC=F"),
}

@app.route("/")
def home():
    if not esta_autorizado():
        return f"<body style='background:#0A0E14;color:#fff;font-family:Arial;text-align:center;padding:50px'><h1>🔒 BLOQUEADO</h1><p>Solo para RAUDY</p><p>Cuenta XM: {MI_CUENTA} - {MI_SERVIDOR}</p></body>", 403
    html = f"<h1>🤖 ROBOT RAUDY VIP PRO - BIENVENIDO RAUDY</h1><p>Cuenta: {MI_CUENTA} | Servidor: {MI_SERVIDOR} | Actualizado: "+time.strftime("%H:%M:%S")+"</p>"
    html += "<style>body{background:#0A0E14;color:#fff;font-family:Arial;padding:15px} .c{background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:10px 0} .up{color:#00FF88} .down{color:#FF4757} .badge{padding:6px 12px;border-radius:20px;font-weight:800;display:inline-block}</style>"
    for nombre, (simbolo, tipo, yahoo) in ACTIVOS.items():
        precio_txt = ""; extra = ""; velas = []
        if tipo == "ORO":
            p = get_oro()
            precio_txt = f"${p:.2f}" if p else "Sin datos"
            for tf in ["1m","5m","15m","1h","4h"]: velas.append(get_binance(simbolo, tf))
        elif tipo == "FOREX":
            p = get_forex(nombre)
            precio_txt = f"{p:.4f}" if p else "Sin datos"
            for tf in ["1m","5m","15m","1h","4h"]: velas.append(get_binance(simbolo, tf))
        elif tipo == "BOLSA":
            data = get_bolsa(yahoo)
            if not data:
                html += f"<div class='c'><h2>{nombre}</h2><p>Sin conexion, reintentando...</p></div>"
                continue
            velas = data['velas']
            color = "up" if data['porc'] >= 0 else "down"
            flecha = "▲" if data['porc'] >= 0 else "▼"
            precio_txt = f"<span class='{color}'>${data['precio']:,.2f} {flecha} {data['cambio']:+.2f} ({data['porc']:+.2f}%)</span>"
            extra = f"<p style='color:#9AA4B2;font-size:12px'>Bolsa: {yahoo} • Max: ${data['max']:,.2f} • Min: ${data['min']:,.2f}</p>"
        senal = analizar_velas(velas)
        detalle = ""
        for tf, v in zip(["1M","5M","15M","1H","4H"], velas):
            if v:
                emoji = "🟢" if v['close'] > v['open'] else "🔴"
                detalle += f"{emoji} {tf} "
        bg = "background:#00FF88;color:#000" if "COMPRA" in senal else "background:#FF4757;color:#fff" if "VENTA" in senal else "background:#1A1A1A;color:#FFD700;border:1px solid #FFD700"
        html += f"<div class='c'><h2>{nombre}</h2><h3>{precio_txt}</h3>{extra}<p>{detalle}</p><span class='badge' style='{bg}'>{senal}</span></div>"
    html += "<script>setTimeout(()=>location.reload(),30000)</script>"
    return html

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
