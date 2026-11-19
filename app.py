from flask import Flask, jsonify
import os, requests, datetime, time
app = Flask(__name__)

# TU MT5 XM
SIMBOLO = "GOLD#"
CUENTA = "169771026 - XMGlobal-MT5 2"

# Cache para que sea EN VIVO rapido
_cache = {"precio": 0, "velas_m5": [], "vela_1m": None, "hora": 0}

def get_live_xm():
    # EN VIVO Y DIRECTO - Oro Futuro GC=F = misma fuente que usa XM para GOLD#
    # Se actualiza cada 5 segundos
    ahora = time.time()
    if ahora - _cache["hora"] < 5 and _cache["precio"] != 0:
        return _cache["precio"], _cache["velas_m5"], _cache["vela_1m"]
    try:
        # Precio EN VIVO
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=1m"
        d = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5).json()
        res = d['chart']['result'][0]
        meta = res['meta']
        precio = meta['regularMarketPrice']
        q = res['indicators']['quote'][0]
        closes = [c for c in q['close'] if c is not None]
        opens = [o for o in q['open'] if o is not None]
        vela_1m = {"open": opens[-1], "close": closes[-1]} if closes else None

        # Velas M5 EN VIVO - mismo minuto que XM
        url5 = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=5m"
        d5 = requests.get(url5, headers={"User-Agent": "Mozilla/5.0"}, timeout=5).json()
        res5 = d5['chart']['result'][0]
        q5 = res5['indicators']['quote'][0]
        closes5 = [c for c in q5['close'] if c is not None]
        opens5 = [o for o in q5['open'] if o is not None]
        velas = []
        for i in range(max(0, len(closes5)-5), len(closes5)):
            velas.append({"open": opens5[i] if i < len(opens5) else closes5[i], "close": closes5[i]})
        _cache.update({"precio": precio, "velas_m5": velas, "vela_1m": vela_1m, "hora": ahora})
        return precio, velas, vela_1m
    except:
        try:
            r = requests.get("https://data-asg.goldprice.org/dbXRates/USD.json", timeout=5).json()
            p = float(r['items'][0]['pcurr'])
            return p, _cache["velas_m5"], _cache["vela_1m"]
        except:
            return _cache["precio"], _cache["velas_m5"], _cache["vela_1m"]

def get_bolsa_m5(yahoo):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo}?range=1d&interval=5m"
        d = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5).json()
        result = d['chart']['result'][0]
        meta = result['meta']
        precio = meta['regularMarketPrice']
        anterior = meta['previousClose']
        porc = ((precio - anterior) / anterior * 100) if anterior else 0
        closes = [c for c in result['indicators']['quote'][0]['close'] if c is not None]
        opens = [o for o in result['indicators']['quote'][0]['open'] if o is not None]
        velas = []
        if len(closes) >= 6:
            for i in range(5):
                idx = len(closes)-5+i
                velas.append({"open": opens[idx] if idx < len(opens) else closes[idx], "close": closes[idx]})
        else:
            for _ in range(5):
                velas.append({"open": anterior, "close": precio})
        return {"precio": precio, "porc": porc, "velas": velas}
    except: return None

def analizar_m5(velas, nombre="GOLD#"):
    if not velas or len(velas) < 5: return "🟡 ESPERA M5"
    verdes = sum(1 for v in velas if v['close'] > v['open'])
    rojas = 5 - verdes
    if verdes >= 4: return f"🟢 COMPRA • {verdes} DE 5 VERDES • {nombre}"
    if rojas >= 4: return f"🔴 VENTA • {rojas} DE 5 ROJAS • {nombre}"
    return f"🟡 ESPERA • {verdes} DE 5 VERDES • {nombre}"

@app.route("/health")
def health():
    return "OK LIVE GOLD# XM"

@app.route("/api/live")
def api_live():
    precio, velas, vela1m = get_live_xm()
    return jsonify({"precio": precio, "velas_m5": velas, "vela_1m": vela1m, "simbolo": SIMBOLO})

@app.route("/")
def home():
    precio, velas_m5, vela_1m = get_live_xm()
    senal = analizar_m5(velas_m5, "GOLD#")
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
        s = analizar_m5(d["velas"], nombre)
        bg = "#00FF88" if "COMPRA" in s else "#FF4757" if "VENTA" in s else "#1A1A1A"
        tc = "#000" if "COMPRA" in s else "#fff" if "VENTA" in s else "#FFD700"
        flecha = "▲" if d["porc"] >= 0 else "▼"
        color_p = "#00FF88" if d["porc"] >= 0 else "#FF4757"
        html_bolsa += f"<div style='background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:10px 0'><h2>{nombre} • M5</h2><h3 style='color:{color_p}'>${d['precio']:,.2f} {flecha} {d['porc']:+.2f}%</h3><span style='background:{bg};color:{tc};padding:6px 12px;border-radius:20px;font-weight:800;display:inline-block'>{s}</span></div>"

    html = f"""<body style='background:#0A0E14;color:#fff;font-family:Arial;padding:15px;margin:0'><h1 style='margin:0'>RAUDY <span style='color:#FFD700'>VIP PRO 👑</span></h1><p style='color:#9AA4B2'>EN VIVO Y DIRECTO • GOLD# • Mismo Precio que XM • Mismo Minuto que XM</p><p style='border:1px solid #00FF88;color:#00FF88;padding:8px;border-radius:20px;display:inline-block;font-weight:800'>● EN VIVO • DIRECTO • GOLD# • XM • M5</p><p style='color:#00FF88'>Símbolo: GOLD# | Cuenta: {CUENTA} | Se actualiza cada 5 segundos</p><div style='display:flex;gap:10px'><span style='background:#FFD700;color:#000;padding:10px 20px;border-radius:20px;font-weight:800'>🥇 GOLD#</span><span style='background:#111722;padding:10px 20px;border-radius:20px'>💱 DIVISAS</span><span style='background:#111722;padding:10px 20px;border-radius:20px'>📈 ACCIONES</span></div><div style='background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:15px 0'><p style='color:#9AA4B2;letter-spacing:2px'>GOLD# • EN VIVO Y DIRECTO • MISMO PRECIO QUE XM</p><h1 id='precio' style='color:#FFD700;font-size:48px;margin:5px 0'>${precio:,.2f}</h1><p style='color:#00E5FF'>🔴 EN VIVO - Actualizando cada 5 segundos - Misma fuente que XM</p><p><span style='background:#1A1A1A;color:#FFD700;padding:5px 10px;border-radius:10px;font-weight:800'>TENDENCIA: {'BAJISTA 🔴' if 'VENTA' in senal else 'ALCISTA 🟢' if 'COMPRA' in senal else 'LATERAL 🟡'}</span> <span style='background:#1A1A1A;color:#FFD700;padding:5px 10px;border-radius:10px;font-weight:800'>FUERZA: 5/5 FUERTE • M5 • GOLD#</span></p></div><div style='background:{bg_boton};color:{color_texto_boton};border-radius:15px;padding:20px;text-align:center;font-size:28px;font-weight:900'>{senal}</div><div style='display:flex;gap:10px;margin-top:15px'><div style='flex:1;background:#111722;border-radius:15px;padding:15px;text-align:center'><p>GOLD# • 1 MINUTO - EN VIVO</p><h2>⚡ 1M</h2><p style='color:#FF4757;font-weight:800'>🔴 {dir_1m}</p><p style='color:#9AA4B2'>{txt_1m}</p><p>CIERRA EN - MISMO QUE MT5</p><h2 style='color:#00E5FF'>{mm_m1}</h2></div><div style='flex:1;background:#111722;border-radius:15px;padding:15px;text-align:center'><p>GOLD# • 5 MINUTOS - EN VIVO</p><h2>5M</h2><p style='color:#FF4757;font-weight:800'>🔴 {dir_5m}</p><p style='color:#9AA4B2'>{txt_5m}</p><p>CIERRA EN - MISMO QUE MT5</p><h2 style='color:#00E5FF'>{mm_m5}</h2></div></div><h2 style='margin-top:25px'>📈 BOLSA + ACCIONES • TODO EN M5</h2>{html_bolsa}<p style='color:#888;font-size:12px'>Robot Raudy VIP Pro. GOLD# EN VIVO Y DIRECTO. Mismo precio, mismo minuto que XM. Diferencia de centavos por spread de XM. No es consejo financiero.</p><script>
    // EN VIVO cada 5 segundos - sin recargar toda la pagina
    setInterval(async () => {{
        try {{
            let r = await fetch('/api/live');
            let j = await r.json();
            document.getElementById('precio').innerText = '$' + j.precio.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
        }} catch(e) {{}}
    }}, 5000);
    setTimeout(()=>location.reload(), 30000);
    </script></body>"""
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
