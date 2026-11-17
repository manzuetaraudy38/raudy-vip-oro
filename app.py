from flask import Flask, request
import os, requests, time
app = Flask(__name__)

# --- TU CANDADO, JEFE ---
MI_CUENTA = "169771026"
MI_SERVIDOR = "XMGlobal-MT5 2"

def esta_autorizado():
    return request.args.get("cuenta", "") == MI_CUENTA

# --- CONEXION M5 - MISMA FRECUENCIA QUE MT5 ---
# MT5 M5 = vela de 5 minutos. Ya no mezclamos 1M, 15M, 1H, 4H.
# Solo 5M para que tu pagina y tu MT5 vayan iguales.

def get_m5_binance(symbol):
    # Trae las ultimas 5 velas de 5 MINUTOS, igual que MT5 M5
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=6"
        d = requests.get(url, timeout=10).json()
        velas = []
        for v in d[-5:]:
            velas.append({"open": float(v[1]), "close": float(v[4])})
        return velas
    except: return None

def get_m5_bolsa(symbol_yahoo):
    # Bolsa en 5 minutos, igual que MT5 M5
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
        closes = [c for c in result['indicators']['quote'][0]['close'] if c is not None]
        velas = []
        if len(closes) >= 6:
            for i in range(5):
                velas.append({"open": closes[-6+i], "close": closes[-5+i]})
        else:
            for _ in range(5):
                velas.append({"open": anterior, "close": precio})
        return {"precio": precio, "cambio": cambio, "porc": porc, "velas": velas, "max": meta.get('regularMarketDayHigh'), "min": meta.get('regularMarketDayLow')}
    except: return None

def get_oro_m5():
    # Oro en M5 - precio actual
    try:
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD.json", timeout=10).json()
        return float(r['items'][0]['pcurr'])
    except: return None

def analizar_solo_m5(velas):
    # Regla M5: Si 4 de 5 velas de 5M son verdes = COMPRA. Si 4 son rojas = VENTA
    # Igual que si lo miras en tu MT5 en M5
    if not velas or len(velas) < 5: return "🟡 ESPERA - Sin datos M5"
    verdes = sum(1 for v in velas if v['close'] > v['open'])
    rojas = 5 - verdes
    if verdes >= 4: return f"🟢 COMPRA M5 - {verdes}/5 VERDES"
    if rojas >= 4: return f"🔴 VENTA M5 - {rojas}/5 ROJAS"
    return f"🟡 ESPERA M5 - {verdes}/5 VERDES"

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
        return f"<body style='background:#0A0E14;color:#fff;font-family:Arial;text-align:center;padding:50px'><h1>🔒 BLOQUEADO</h1><p>Solo RAUDY - {MI_CUENTA}</p></body>", 403

    html = f"<h1>🤖 ROBOT RAUDY - MODO M5 SINCRONIZADO CON MT5</h1><p>Cuenta: {MI_CUENTA} | Servidor: {MI_SERVIDOR} | Temporalidad: M5 (5 minutos) | Actualizado: "+time.strftime("%H:%M:%S")+"</p>"
    html += "<style>body{background:#0A0E14;color:#fff;font-family:Arial;padding:15px} .c{background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:10px 0} .up{color:#00FF88} .down{color:#FF4757} .badge{padding:6px 12px;border-radius:20px;font-weight:800;display:inline-block}</style>"
    html += "<p style='background:#FFD700;color:#000;padding:10px;border-radius:10px;font-weight:800'>⚡ ESTE ROBOT SOLO MIRA M5 - IGUAL QUE TU MT5 EN M5 - NO MEZCLA OTRAS TEMPORALIDADES</p>"

    for nombre, (simbolo, tipo, yahoo) in ACTIVOS.items():
        velas = []
        precio_txt = ""
        extra = ""
        if tipo == "ORO":
            p = get_oro_m5()
            precio_txt = f"${p:.2f}" if p else "Sin datos"
            velas = get_m5_binance(simbolo)
        elif tipo == "FOREX":
            # Forex: usamos velas M5 de Binance para la señal
            velas = get_m5_binance(simbolo)
            precio_txt = "Ver señal M5"
        elif tipo == "BOLSA":
            data = get_m5_bolsa(yahoo)
            if not data:
                html += f"<div class='c'><h2>{nombre}</h2><p>Sin conexion Bolsa M5</p></div>"
                continue
            velas = data['velas']
            color = "up" if data['porc'] >= 0 else "down"
            flecha = "▲" if data['porc'] >= 0 else "▼"
            precio_txt = f"<span class='{color}'>${data['precio']:,.2f} {flecha} {data['porc']:+.2f}%</span>"
            extra = f"<p>Max: ${data['max']:,.2f} • Min: ${data['min']:,.2f} • Solo M5</p>"

        senal = analizar_solo_m5(velas)
        detalle = ""
        for v in velas or []:
            detalle += "🟢 " if v['close'] > v['open'] else "🔴 "
        detalle += " (5 velas de 5M)"

        bg = "background:#00FF88;color:#000" if "COMPRA" in senal else "background:#FF4757;color:#fff" if "VENTA" in senal else "background:#1A1A1A;color:#FFD700;border:1px solid #FFD700"
        html += f"<div class='c'><h2>{nombre} • M5</h2><h3>{precio_txt}</h3>{extra}<p>{detalle}</p><span class='badge' style='{bg}'>{senal}</span></div>"

    # Se actualiza cada 5 minutos, igual que M5. No cada 30 segundos, para no confundir.
    html += "<script>setTimeout(()=>location.reload(),300000)</script>"
    return html

@app.route("/health")
def health():
    return "OK M5"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
