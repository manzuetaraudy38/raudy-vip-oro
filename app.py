from flask import Flask
import os, requests, time
app = Flask(__name__)

# ROBOT RAUDY - JALA INFO DE TRADING PUBLICA
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
        # ECB / Frankfurter - Forex real
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

def analizar_velas(velas):
    verdes = sum(1 for v in velas if v and v['close'] > v['open'])
    rojas = 5 - verdes
    if verdes >= 4: return f"🟢 COMPRA - {verdes}/5 VERDES"
    if rojas >= 4: return f"🔴 VENTA - {rojas}/5 ROJAS"
    return f"🟡 ESPERA - {verdes}/5 VERDES"

# MAPA DE TODO TU TRADING
ACTIVOS = {
    "ORO XAU/USD": ("PAXGUSDT", "ORO"),
    "EUR/USD": ("EURUSDT", "FOREX"),
    "GBP/USD": ("GBPUSDT", "FOREX"),
    "USD/JPY": ("EURUSDT", "FOREX"),
    "AUD/USD": ("AUDUSDT", "FOREX"),
    "META": ("BTCUSDT", "ACCION"),
    "CAFE": ("ETHUSDT", "MATERIA"),
    "CACAO": ("BNBUSDT", "MATERIA"),
    "S&P 500": ("BTCUSDT", "INDICE"),
}

@app.route("/")
def home():
    html = "<h1>🤖 ROBOT RAUDY VIP PRO - INFO TRADING</h1><p>Actualizado: "+time.strftime("%H:%M:%S")+"</p>"
    html += "<style>body{background:#0A0E14;color:#fff;font-family:Arial;padding:15px} .c{background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:10px 0} .v{color:#00FF88} .r{color:#FF4757}</style>"

    for nombre, (simbolo, tipo) in ACTIVOS.items():
        # Precio
        precio = ""
        if tipo == "ORO":
            p = get_oro()
            precio = f"${p:.2f}" if p else "Sin datos"
        elif tipo == "FOREX":
            p = get_forex(nombre)
            precio = f"{p:.4f}" if p else "Sin datos"
        else:
            # Para META / CAFE / CACAO / SP500 usamos Binance como referencia
            v = get_binance(simbolo, "1m")
            precio = f"Ref: {v['close']:.2f}" if v else "Sin datos"

        # Velas
        velas = []
        for tf in ["1m","5m","15m","1h","4h"]:
            velas.append(get_binance(simbolo, tf))

        senal = analizar_velas(velas)
        detalle = ""
        for tf, v in zip(["1M","5M","15M","1H","4H"], velas):
            if v:
                color = "🟢" if v['close'] > v['open'] else "🔴"
                detalle += f"{color} {tf} "
        
        html += f"<div class='c'><h2>{nombre}</h2><h3>{precio}</h3><p>{detalle}</p><b>{senal}</b></div>"

    html += "<p style='color:#888;font-size:12px'>Robot de información pública. No es consejo financiero. Opera con poquito.</p>"
    html += "<script>setTimeout(()=>location.reload(),30000)</script>"
    return html

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
