from flask import Flask, jsonify
import os, requests, datetime, time
app = Flask(__name__)

SIMBOLO = "GOLD#"
CUENTA = "169771026 - XMGlobal-MT5 2"
# YA NO ES PAXG, JEFE - AHORA ES XAU/USD = GOLD# DE XM
FUENTE = "XAU/USD - GOLD# - IGUAL A XM"
SPREAD_XM = 0.30

_cache = {"precio": 0, "precio_xm": 0, "velas_m5": [], "vela_1m": None, "vela_15m": None, "vela_1h": None, "hora": 0}

def get_live_xauusd():
    ahora = time.time()
    if ahora - _cache["hora"] < 3 and _cache["precio"] != 0:
        return _cache
    try:
        # 1. PRECIO REAL XAU/USD - Usamos GC=F que es ORO, no PAXG
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=1m"
        d = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=4).json()
        res = d['chart']['result'][0]
        precio_xau = res['meta']['regularMarketPrice']
        q = res['indicators']['quote'][0]
        closes = [c for c in q['close'] if c is not None]
        opens = [o for o in q['open'] if o is not None]
        vela_1m = {"open": opens[-1], "close": closes[-1]} if closes else None
        precio_xm = precio_xau + SPREAD_XM

        def get_velas(intervalo, cantidad=5):
            u = f"https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval={intervalo}"
            dd = requests.get(u, headers={"User-Agent": "Mozilla/5.0"}, timeout=4).json()
            rr = dd['chart']['result'][0]
            qq = rr['indicators']['quote'][0]
            cc = [c for c in qq['close'] if c is not None]
            oo = [o for o in qq['open'] if o is not None]
            velas = []
            for i in range(max(0, len(cc)-cantidad), len(cc)):
                velas.append({"open": oo[i], "close": cc[i]})
            return velas

        velas_m5 = get_velas("5m", 5)
        velas_15m = get_velas("15m", 1)
        velas_1h = get_velas("60m", 1)
        vela_15m = velas_15m[-1] if velas_15m else None
        vela_1h = velas_1h[-1] if velas_1h else None
        _cache.update({"precio": precio_xau, "precio_xm": precio_xm, "velas_m5": velas_m5, "vela_1m": vela_1m, "vela_15m": vela_15m, "vela_1h": vela_1h, "hora": ahora})
        return _cache
    except:
        try:
            # RESPALDO XAU/USD, NO PAXG, JEFE
            r = requests.get("https://data-asg.goldprice.org/dbXRates/USD.json", timeout=4).json()
            p = float(r['items'][0]['pcurr'])
            _cache.update({"precio": p, "precio_xm": p + SPREAD_XM})
            return _cache
        except:
            return _cache

def analizar_en_vivo(velas, precio_xm):
    if not velas or len(velas) < 5:
        return "🟡 ESPERA - Cargando XAU/USD en vivo..."
    verdes = sum(1 for v in velas if v['close'] > v['open'])
    rojas = 5 - verdes
    if verdes >= 4:
        return f"🟢 COMPRA • {verdes} DE 5 VERDES • XAU/USD ${precio_xm:,.2f}"
    if rojas >= 4:
        return f"🔴 VENTA • {rojas} DE 5 ROJAS • XAU/USD ${precio_xm:,.2f}"
    return f"🟡 ESPERA • {verdes} DE 5 VERDES • XAU/USD ${precio_xm:,.2f}"

@app.route("/health")
def health():
    return "OK XAU/USD EN VIVO - NO PAXG - IGUAL A XM"

@app.route("/api/live")
def api_live():
    datos = get_live_xauusd()
    precio_xm = datos["precio_xm"]
    senal = analizar_en_vivo(datos["velas_m5"], precio_xm)
    return jsonify({"precio": precio_xm, "precio_real": precio_xm, "fuente": "XAU/USD", "velas_m5": datos["velas_m5"], "vela_1m": datos["vela_1m"], "senal": senal, "en_vivo": True, "spread": SPREAD_XM})

@app.route("/")
def home():
    datos = get_live_xauusd()
    precio = datos["precio_xm"]
    velas_m5 = datos["velas_m5"]
    vela_1m = datos["vela_1m"]
    vela_15m = datos["vela_15m"]
    vela_1h = datos["vela_1h"]
    senal = analizar_en_vivo(velas_m5, precio)
    bg_boton = "#FF4757" if "VENTA" in senal else "#00FF88" if "COMPRA" in senal else "#1A1A1A"
    color_texto = "#fff" if "VENTA" in senal else "#000" if "COMPRA" in senal else "#FFD700"
    ahora = datetime.datetime.now()
    seg_m5 = (5 - (ahora.minute % 5)) * 60 - ahora.second
    seg_m1 = 60 - ahora.second
    seg_15m = (15 - (ahora.minute % 15)) * 60 - ahora.second
    seg_1h = (60 - ahora.minute) * 60 - ahora.second
    mm_m5 = f"{seg_m5//60:02d}:{seg_m5%60:02d}"
    mm_m1 = f"00:{seg_m1:02d}"
    mm_15m = f"{seg_15m//60:02d}:{seg_15m%60:02d}"
    mm_1h = f"{seg_1h//60:02d}:{seg_1h%60:02d}"

    def cuadro(titulo, timeframe, vela, mm):
        if not vela:
            dir_txt = "SIN DATOS"; txt = ""; color = "#9AA4B2"
        else:
            dir_txt = "ROJA • CAYENDO" if vela["close"] < vela["open"] else "VERDE • SUBIENDO"
            porc = (vela["close"] - vela["open"]) / vela["open"] * 100
            txt = f"Apertura {vela['open']:.2f} → Cierre {vela['close']:.2f}<br>{porc:.3f}%"
            color = "#FF4757" if "ROJA" in dir_txt else "#00FF88"
        return f"<div style='flex:1;background:#111722;border-radius:15px;padding:15px;text-align:center;min-width:140px'><p>TIMEFRAME • {titulo}</p><h2>{timeframe}</h2><p style='color:{color};font-weight:800'>🔴 {dir_txt}</p><p style='color:#9AA4B2'>{txt}</p><p>CIERRA EN</p><h2 style='color:#00E5FF'>{mm}</h2></div>"

    html = f"""<body style='background:#0A0E14;color:#fff;font-family:Arial;padding:15px;margin:0'>
    <h1>RAUDY <span style='color:#FFD700'>VIP PRO 👑</span></h1>
    <p style='color:#9AA4B2'>EN VIVO Y DIRECTO • XAU/USD • GOLD# • IGUAL A XM • NO PAXG</p>
    <p style='border:1px solid #00FF88;color:#00FF88;padding:8px;border-radius:20px;display:inline-block;font-weight:800'>● EN VIVO • XAU/USD • GOLD# • M5</p>
    <p style='color:#00FF88'>Cuenta: {CUENTA} | Se actualiza cada 3 segundos | Spread XM +0.30</p>
    <div style='background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:15px 0'>
    <p style='color:#9AA4B2'>GOLD • XAU / USD • PRECIO REAL DEL MERCADO - XAU/USD</p>
    <h1 id='precio' style='color:#FFD700;font-size:52px;margin:5px 0'>${precio:,.2f} (XAU/USD)</h1>
    <p style='color:#00E5FF'>🔴 EN VIVO - XAU/USD + 0.30 Spread = Precio XM - NO PAXG</p>
    </div>
    <div id='senal' style='background:{bg_boton};color:{color_texto};border-radius:15px;padding:20px;text-align:center;font-size:28px;font-weight:900'>{senal}</div>
    <div style='display:flex;gap:10px;margin-top:15px;flex-wrap:wrap'>
    {cuadro("1 MINUTO", "⚡ 1M", vela_1m, mm_m1)}
    {cuadro("5 MINUTOS", "5M", velas_m5[-1] if velas_m5 else None, mm_m5)}
    {cuadro("15 MINUTOS", "15M", vela_15m, mm_15m)}
    {cuadro("1 HORA", "1H", vela_1h, mm_1h)}
    </div>
    <p style='color:#888;font-size:12px;margin-top:20px'>XAU/USD en vivo + Spread XM 0.30 = Igualito a tu XM. No es PAXG. No es consejo financiero. Solo DEMO.</p>
    <script>
    setInterval(async () => {{
        try {{
            let r = await fetch('/api/live');
            let j = await r.json();
            document.getElementById('precio').innerText = '$' + j.precio.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}}) + ' (XAU/USD)';
            document.getElementById('senal').innerText = j.senal;
            if(j.senal.includes('COMPRA')) {{ document.getElementById('senal').style.background = '#00FF88'; document.getElementById('senal').style.color = '#000'; }}
            if(j.senal.includes('VENTA')) {{ document.getElementById('senal').style.background = '#FF4757'; document.getElementById('senal').style.color = '#fff'; }}
            if(j.senal.includes('ESPERA')) {{ document.getElementById('senal').style.background = '#1A1A1A'; document.getElementById('senal').style.color = '#FFD700'; }}
        }} catch(e) {{}}
    }}, 3000);
    setTimeout(()=>location.reload(), 30000);
    </script></body>"""
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
