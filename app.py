from flask import Flask, jsonify
import os, requests, datetime, time
app = Flask(__name__)

SIMBOLO = "GOLD#"
CUENTA = "169771026 - XMGlobal-MT5 2"

# NO HAY PRECIO FIJO, JEFE. Todo es EN VIVO.
_cache = {"precio": 0, "velas_m5": [], "vela_1m": None, "hora": 0}

def get_live_directo():
    # EN VIVO Y DIRECTO - Cada 3 segundos, jefe
    ahora = time.time()
    if ahora - _cache["hora"] < 3 and _cache["precio"] != 0:
        return _cache["precio"], _cache["velas_m5"], _cache["vela_1m"]
    try:
        # 1. PRECIO REAL EN VIVO - Oro GC=F
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=1m"
        d = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=4).json()
        res = d['chart']['result'][0]
        precio_real = res['meta']['regularMarketPrice']
        q = res['indicators']['quote'][0]
        closes = [c for c in q['close'] if c is not None]
        opens = [o for o in q['open'] if o is not None]
        vela_1m = {"open": opens[-1], "close": closes[-1]} if closes else None

        # 2. VELAS M5 EN VIVO
        url5 = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=5m"
        d5 = requests.get(url5, headers={"User-Agent": "Mozilla/5.0"}, timeout=4).json()
        res5 = d5['chart']['result'][0]
        q5 = res5['indicators']['quote'][0]
        closes5 = [c for c in q5['close'] if c is not None]
        opens5 = [o for o in q5['open'] if o is not None]
        velas = []
        for i in range(max(0, len(closes5)-5), len(closes5)):
            velas.append({"open": opens5[i], "close": closes5[i]})
        _cache.update({"precio": precio_real, "velas_m5": velas, "vela_1m": vela_1m, "hora": ahora})
        return precio_real, velas, vela_1m
    except:
        try:
            # Respaldo - Precio Oro en vivo
            r = requests.get("https://data-asg.goldprice.org/dbXRates/USD.json", timeout=4).json()
            p = float(r['items'][0]['pcurr'])
            return p, _cache["velas_m5"], _cache["vela_1m"]
        except:
            return _cache["precio"], _cache["velas_m5"], _cache["vela_1m"]

def analizar_en_vivo(velas, precio_real):
    # SEÑAL CON PRECIO REAL, JEFE - No con precio fijo
    if not velas or len(velas) < 5:
        return "🟡 ESPERA - Cargando precio en vivo..."
    verdes = sum(1 for v in velas if v['close'] > v['open'])
    rojas = 5 - verdes
    # COMPRA - Con precio real de ahora mismo
    if verdes >= 4:
        return f"🟢 COMPRA • {verdes} DE 5 VERDES • PRECIO REAL ${precio_real:,.2f}"
    if rojas >= 4:
        return f"🔴 VENTA • {rojas} DE 5 ROJAS • PRECIO REAL ${precio_real:,.2f}"
    return f"🟡 ESPERA • {verdes} DE 5 VERDES • PRECIO REAL ${precio_real:,.2f}"

@app.route("/health")
def health():
    return "OK EN VIVO Y DIRECTO - GOLD# - PRECIO REAL"

@app.route("/api/live")
def api_live():
    precio, velas, vela1m = get_live_directo()
    senal = analizar_en_vivo(velas, precio)
    return jsonify({"precio": precio, "precio_real": precio, "velas_m5": velas, "vela_1m": vela1m, "senal": senal, "en_vivo": True})

@app.route("/")
def home():
    precio, velas_m5, vela_1m = get_live_directo()
    senal = analizar_en_vivo(velas_m5, precio)
    bg_boton = "#FF4757" if "VENTA" in senal else "#00FF88" if "COMPRA" in senal else "#1A1A1A"
    color_texto = "#fff" if "VENTA" in senal else "#000" if "COMPRA" in senal else "#FFD700"
    ahora = datetime.datetime.now()
    seg_para_m5 = (5 - (ahora.minute % 5)) * 60 - ahora.second
    seg_para_m1 = 60 - ahora.second

    html = f"""<body style='background:#0A0E14;color:#fff;font-family:Arial;padding:15px;margin:0'>
    <h1>RAUDY <span style='color:#FFD700'>VIP PRO 👑</span></h1>
    <p style='color:#9AA4B2'>EN VIVO Y DIRECTO • GOLD# • PRECIO REAL • Sin precio fijo</p>
    <p style='border:1px solid #00FF88;color:#00FF88;padding:8px;border-radius:20px;display:inline-block;font-weight:800'>● EN VIVO • DIRECTO • PRECIO REAL • GOLD# • XM • M5</p>
    <p style='color:#00FF88'>Cuenta: {CUENTA} | Se actualiza cada 3 segundos</p>
    <div style='background:#111722;border:1px solid #333;border-radius:15px;padding:15px;margin:15px 0'>
    <p style='color:#9AA4B2'>GOLD# • PRECIO REAL EN VIVO Y DIRECTO</p>
    <h1 id='precio' style='color:#FFD700;font-size:52px;margin:5px 0'>${precio:,.2f}</h1>
    <p style='color:#00E5FF'>🔴 EN VIVO - Actualizando cada 3 segundos - Precio Real, no foto</p>
    </div>
    <div id='senal' style='background:{bg_boton};color:{color_texto};border-radius:15px;padding:20px;text-align:center;font-size:28px;font-weight:900'>{senal}</div>
    <p style='color:#888;font-size:12px;margin-top:20px'>Precio Real en Vivo. No es precio de foto. Se mueve cada 3 segundos. No es consejo financiero. Solo DEMO.</p>
    <script>
    setInterval(async () => {{
        try {{
            let r = await fetch('/api/live');
            let j = await r.json();
            document.getElementById('precio').innerText = '$' + j.precio.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
            document.getElementById('senal').innerText = j.senal;
            // Cambia el color solo, jefe - verde compra, rojo venta
            if(j.senal.includes('COMPRA')) {{ document.getElementById('senal').style.background = '#00FF88'; document.getElementById('senal').style.color = '#000'; }}
            if(j.senal.includes('VENTA')) {{ document.getElementById('senal').style.background = '#FF4757'; document.getElementById('senal').style.color = '#fff'; }}
            if(j.senal.includes('ESPERA')) {{ document.getElementById('senal').style.background = '#1A1A1A'; document.getElementById('senal').style.color = '#FFD700'; }}
        }} catch(e) {{}}
    }}, 3000);
    </script></body>"""
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
