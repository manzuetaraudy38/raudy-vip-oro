from flask import Flask, request
import os, requests, time, datetime
app = Flask(__name__)
MI_CUENTA = "169771026"
MI_SERVIDOR = "XMGlobal-MT5 2"
def esta_autorizado():
    return request.args.get("cuenta", "") == MI_CUENTA
def get_m5_binance(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=6"
        d = requests.get(url, timeout=10).json()
        velas = []
        for v in d[-5:]:
            velas.append({"open": float(v[1]), "close": float(v[4])})
        return velas
    except: return None
def get_1m_binance(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=2"
        d = requests.get(url, timeout=10).json()
        v = d[-1]
        return {"open": float(v[1]), "close": float(v[4])}
    except: return None
def get_oro():
    try:
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD.json", timeout=10).json()
        return float(r['items'][0]['pcurr'])
    except: return None
def get_bolsa_m5(yahoo):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo}?range=1d&interval=5m"
        d = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
        result = d['chart']['result'][0]
        meta = result['meta']
        precio = meta['regularMarketPrice']
        anterior = meta['previousClose']
        porc = ((precio - anterior) / anterior * 100) if anterior else 0
        closes = [c for c in result['indicators']['quote'][0]['close'] if c is not None]
        velas = []
        if len(closes) >= 6:
            for i in range(5):
                velas.append({"open": closes[-6+i], "close": closes[-5+i]})
        else:
            for _ in range(5):
                velas.append({"open": anterior, "close": precio})
        return {"precio": precio, "porc": porc, "velas": velas}
    except: return None
def analizar_m5(velas):
    if not velas or len(velas) < 5: return "🟡 ESPERA M5"
    verdes = sum(1 for v in velas if v['close'] > v['open'])
    rojas = 5 - verdes
    if verdes >= 4: return f"🟢 COMPRA • {verdes} DE 5 VERDES • Oro"
    if rojas >= 4: return f"🔴 VENTA • {rojas} DE 5 ROJAS • Oro"
    return f"🟡 ESPERA • {verdes} DE 5 VERDES • Oro"
@app.route("/health")
def health():
    return "OK M5"
@app.route("/")
def home():
    if not esta_autorizado():
        return f"<body style='background:#0A0E14;color:#fff;font-family:Arial;text-align:center;padding:50px'><h1>🔒 BLOQUEADO</h1><p>Solo RAUDY - {MI_CUENTA}</p><p>Entra con ?cuenta=169771026</p></body>", 403
    velas_m5 = get_m5_binance("PAXGUSDT")
    vela_1m = get_1m_binance("PAXGUSDT")
    precio_paxg = get_oro()
    precio_mostrar = precio_paxg if precio_paxg else 0
    senal = analizar_m5(velas_m5)
    bg_boton = "#FF4757" if "VENTA" in senal else "#00FF88" if "COMPRA" in senal else "#1A1A1A"
    color_texto_boton = "#fff" if "VENTA" in senal else "#000" if "COMPRA" in senal else "#FFD700"
    ahora = datetime.datetime.now()
    seg_para_m5 = (5 - (ahora.minute % 5)) * 60 - ahora.second
    seg_para_m1 = 60 - ahora.second
    mm_m5 = f"{seg_para_m5//60:02d}:{seg_para_m5%60:02d}"
    mm_m1 = f"00:{seg_para_m1:02d}"
    if vela_1m:
        dir_1m = "ROJA • CAYENDO" if vela_1m["close"] < vela_1m["open"] else "VERDE • SUBIENDO"
        porc_1m = (vela_1m["close"] - vela_1m["open"]) / vela_1m["open"] * 100
        txt_1m = f"Apertura {vela_1m['open']:.2f} → Cierre {vela_1m['close']:.2f}<br>{porc_1m:.3f}%"
    else:
        dir_1m = "SIN DATOS"; txt_1m = ""
    if velas_m5:
        dir_5m = "ROJA • CAYENDO" if velas_m5[-1]["close"] < velas_m5[-1]["open"] else "VERDE • SUBIENDO"
        porc_5m = (velas_m5[-1]["close"] - velas_m5[-1]["open"]) / velas_m5[-1]["open"] * 100
        txt_5m = f"Apertura {velas_m5[-1]['open']:.2f} → Cierre {velas_m5[-1]['close']:.2f}<br>{porc_5m:.3f}%"
    else:
        dir_5m = "SIN DATOS"; txt_5m = ""
    ACTIVOS = {"META": "META", "APPLE": "AAPL", "TESLA": "TSLA", "NVIDIA": "NVDA", "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "DOW JONES": "^DJI", "CAFE": "KC=F", "CACAO": "CC=F", "ORO BOLSA": "GC=F"}
    html_bolsa = ""
    for nombre, yahoo in ACTIVOS.items():
        d = get_bolsa_m5(yahoo)
        if not d: continue
        s = analizar_m5(d["velas"]).replace("Oro", nombre)
        bg = "#00FF88" if "COMPRA" in s else "#FF4757" if "VENTA" in s else "#1A1A1A"
        tc = "#000" if "COMPRA" in s else "#fff" if "VENTA" in s else "#FFD700"
        flecha = "▲" if d["porc"] >= 0 else "▼"
        color_p = "#00FF88" if d["porc"] >= 0 else "#FF4757"
        html_bolsa += f"<div style='background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:10px 0'><h2>{nombre} • M5</h2><h3 style='color:{color_p}'>${d['precio']:,.2f} {flecha} {d['porc']:+.2f}%</h3><span style='background:{bg};color:{tc};padding:6px 12px;border-radius:20px;font-weight:800;display:inline-block'>{s}</span></div>"
    html = f"""<body style='background:#0A0E14;color:#fff;font-family:Arial;padding:15px;margin:0'><h1 style='margin:0'>RAUDY <span style='color:#FFD700'>VIP PRO 👑</span></h1><p style='color:#9AA4B2'>Professional Trading Signals • ORO + DIVISAS + ACCIONES • Real Market Data</p><p style='border:1px solid #00FF88;color:#00FF88;padding:8px;border-radius:20px;display:inline-block;font-weight:800'>● LIVE • MERCADO REAL • PROFESIONAL • M5 SINCRONIZADO CON MT5</p><p style='color:#00FF88'>Cuenta: {MI_CUENTA} | Servidor: {MI_SERVIDOR} | Temporalidad: M5 (5 minutos)</p><div style='display:flex;gap:10px'><span style='background:#FFD700;color:#000;padding:10px 20px;border-radius:20px;font-weight:800'>🥇 ORO</span><span style='background:#111722;padding:10px 20px;border-radius:20px'>💱 DIVISAS</span><span style='background:#111722;padding:10px 20px;border-radius:20px'>📈 ACCIONES</span></div><div style='background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:15px 0'><p style='color:#9AA4B2;letter-spacing:2px'>GOLD • XAU / USD • PRECIO REAL DEL MERCADO</p><h1 style='color:#FFD700;font-size:42px;margin:5px 0'>${precio_mostrar:,.2f}</h1><p style='color:#00E5FF'>Conectando con mercado mundial... M5 = Igual que tu MT5</p><p><span style='background:#1A1A1A;color:#FFD700;padding:5px 10px;border-radius:10px;font-weight:800'>TENDENCIA: {'BAJISTA 🔴' if 'VENTA' in senal else 'ALCISTA 🟢' if 'COMPRA' in senal else 'LATERAL 🟡'}</span> <span style='background:#1A1A1A;color:#FFD700;padding:5px 10px;border-radius:10px;font-weight:800'>FUERZA: 5/5 FUERTE • M5</span></p></div><div style='background:{bg_boton};color:{color_texto_boton};border-radius:15px;padding:20px;text-align:center;font-size:28px;font-weight:900'>{senal}</div><div style='display:flex;gap:10px;margin-top:15px'><div style='flex:1;background:#111722;border-radius:15px;padding:15px;text-align:center'><p>TIMEFRAME • 1 MINUTO</p><h2>⚡ 1M</h2><div style='background:#FF4757;height:120px;border-radius:15px;margin:10px'></div><p style='color:#FF4757;font-weight:800'>🔴 {dir_1m}</p><p style='color:#9AA4B2'>{txt_1m}</p><p>CIERRA EN</p><h2 style='color:#00E5FF'>{mm_m1}</h2></div><div style='flex:1;background:#111722;border-radius:15px;padding:15px;text-align:center'><p>TIMEFRAME • 5 MINUTOS</p><h2>5M</h2><div style='background:#FF4757;height:120px;border-radius:15px;margin:10px'></div><p style='color:#FF4757;font-weight:800'>🔴 {dir_5m}</p><p style='color:#9AA4B2'>{txt_5m}</p><p>CIERRA EN</p><h2 style='color:#00E5FF'>{mm_m5}</h2></div></div><h2 style='margin-top:25px'>📈 BOLSA + ACCIONES • TODO EN M5</h2>{html_bolsa}<p style='color:#888;font-size:12px'>Robot Raudy VIP Pro. Señal principal = M5. Misma frecuencia que tu MT5 en M5. No es consejo financiero.</p><script>setTimeout(()=>location.reload(),30000)</script></body>"""
    return html
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
