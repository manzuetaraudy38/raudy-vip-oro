import os, json, urllib.request, urllib.parse
import threading, time, random, math
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify
app = Flask(__name__)
TELE_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELE_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")
BROKER_KEY = os.environ.get("BROKER_KEY", "")
BOT = {"activo": False, "balance": 1000.0}
BOT["ganadas"] = 0
BOT["perdidas"] = 0
BOT["hist"] = []
BOT["ult"] = "BOT APAGADO"
BOT["pos"] = None
BOT["entrada"] = 0
BOT["perdidas_dia"] = 0
BOT["dia"] = ""
BOT["operaciones_dia"] = 0
BOT["modo"] = "PRACTICA - Dinero falso"
HIST = []
TP_GAN = 20.0
SL_PER = 10.0
MAX_PERDIDAS_DIA = 3
MAX_PERDIDA_DIA_DINERO = 30.0
ULTIMO_ID = [0]

def telegram(msg, chat_id=None):
    try:
        if not TELE_TOKEN:
            return
        cid = chat_id or TELE_CHAT
        if not cid:
            return
        txt = urllib.parse.quote(msg)
        u = "https://api.telegram.org/bot" + TELE_TOKEN + "/sendMessage?chat_id=" + str(cid) + "&text=" + txt
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        urllib.request.urlopen(req, timeout=5).read()
    except:
        pass

def precio(sym):
    try:
        u = "https://query1.finance.yahoo.com/v8/finance/chart/" + sym + "?interval=1m&range=1d"
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read().decode())
            m = d["chart"]["result"][0]["meta"]
            return float(m.get("regularMarketPrice"))
    except:
        return None

def precios_pasado():
    try:
        u = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1h&range=1mo"
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            d = json.loads(r.read().decode())
            res = d["chart"]["result"][0]
            cl = res["indicators"]["quote"][0]["close"]
            return [float(x) for x in cl if x is not None]
    except:
        return []

def rsi(pr, n=14):
    if len(pr) < n + 1:
        return 50
    g = 0
    p = 0
    for i in range(1, n + 1):
        diff = pr[-i] - pr[-i-1]
        if diff > 0:
            g += diff
        else:
            p += abs(diff)
    if p == 0:
        return 100
    rs = (g / n) / (p / n)
    return 100 - (100 / (1 + rs))

def ema(pr, n):
    if len(pr) < n:
        return sum(pr) / len(pr)
    k = 2 / (n + 1)
    e = sum(pr[:n]) / n
    for x in pr[n:]:
        e = x * k + e * (1 - k)
    return e

def macd(pr):
    if len(pr) < 26:
        return 0
    return ema(pr, 12) - ema(pr, 26)

def boll(pr):
    if len(pr) < 20:
        return "MEDIO"
    ult = pr[-20:]
    med = sum(ult) / len(ult)
    var = sum((x - med) ** 2 for x in ult) / len(ult)
    dv = math.sqrt(var)
    sup = med + 2 * dv
    inf = med - 2 * dv
    act = pr[-1]
    if act <= inf + dv * 0.2:
        return "BARATO"
    if act >= sup - dv * 0.2:
        return "CARO"
    if act < med:
        return "BARATO"
    return "CARO"

def tendencia(pr):
    if len(pr) < 10:
        return "LADO"
    a = sum(pr[-5:]) / 5
    b = sum(pr[-10:-5]) / 5
    if a > b:
        return "SUBIENDO"
    if a < b:
        return "BAJANDO"
    return "LADO"

def doble(pr):
    if len(pr) < 30:
        return False
    largo = tendencia(pr[-30:])
    if largo == "SUBIENDO":
        return True
    return False

def noticias_peligrosas():
    ahora = datetime.now(timezone.utc) + timedelta(hours=1)
    h = ahora.hour
    m = ahora.minute
    dia_semana = ahora.weekday()
    if dia_semana >= 5:
        return True
    if h == 14 and m >= 25:
        return True
    if h == 15 and m <= 5:
        return True
    if h == 15 and m >= 55:
        return True
    if h == 16 and m <= 10:
        return True
    if h == 8 and m >= 25 and m <= 45:
        return True
    return False

def cerebro(precio_oro, lista):
    lista.append(precio_oro)
    if len(lista) > 60:
        lista.pop(0)
    v = 0
    r = rsi(lista)
    t = tendencia(lista)
    mc = macd(lista)
    b = boll(lista)
    d = doble(lista)
    if r < 30:
        v += 200
    if r > 70:
        v -= 200
    if t == "SUBIENDO":
        v += 150
    if t == "BAJANDO":
        v -= 150
    if mc > 0:
        v += 200
    if mc < 0:
        v -= 200
    if b == "BARATO":
        v += 250
    if b == "CARO":
        v -= 250
    if d:
        v += 300
    if v >= 400:
        return "COMPRAR"
    if v <= -400:
        return "VENDER"
    return "ESPERA"

def backtest():
    pr = precios_pasado()
    if len(pr) < 50:
        pr = []
        p = 4150
        for i in range(200):
            p += random.uniform(-12, 12)
            pr.append(p)
        modo = "SIMULADO"
    else:
        modo = "REAL"
    bal = 1000
    g = 0
    pe = 0
    for i in range(30, len(pr) - 5):
        lista = pr[max(0, i-30):i]
        votos = 0
        if rsi(lista) < 45:
            votos += 1
        if macd(lista) > 0:
            votos += 1
        if boll(lista) == "BARATO":
            votos += 1
        if doble(lista):
            votos += 1
        if votos >= 3:
            ent = pr[i]
            sal = pr[min(len(pr)-1, i+5)]
            gan = sal - ent
            if gan > 0 and gan > TP_GAN:
                gan = TP_GAN
            if gan < 0 and gan < -SL_PER:
                gan = -SL_PER
            bal += gan
            if gan >= 0:
                g += 1
            else:
                pe += 1
    tot = g + pe
    wr = (g / tot * 100) if tot > 0 else 0
    return {"modo": modo, "balance_final": round(bal, 2), "ganadas": g, "perdidas": pe, "winrate": round(wr, 1), "mensaje": "Gana 20 pierde 10"}

def enviar_orden_real(tipo, precio_oro):
    if not BROKER_KEY:
        return False
    try:
        telegram("BROKER REAL: Intentaria " + tipo + " en " + str(precio_oro))
        return True
    except:
        return False

def bot_motor():
    while True:
        try:
            hoy = datetime.now().strftime("%Y-%m-%d")
            if BOT["dia"] != hoy:
                BOT["dia"] = hoy
                BOT["perdidas_dia"] = 0
                BOT["operaciones_dia"] = 0
            if BOT["activo"]:
                oro = precio("GC=F") or 4078
                dec = cerebro(oro, HIST)
                if BOT["perdidas_dia"] >= MAX_PERDIDAS_DIA:
                    BOT["activo"] = False
                    BOT["ult"] = "FRENO: 3 perdidas hoy, me apago"
                    telegram("FRENO JEFE: Perdi 3 veces hoy, me apague para protegerte. Balance " + str(BOT["balance"]))
                    time.sleep(10)
                    continue
                es_noticia = noticias_peligrosas()
                if es_noticia and BOT["pos"] is None:
                    BOT["ult"] = "PAUSA NOTICIAS - Espero"
                else:
                    if dec == "COMPRAR":
                        if BOT["pos"] is None:
                            BOT["pos"] = "COMPRAR"
                            BOT["entrada"] = oro
                            BOT["operaciones_dia"] += 1
                            BOT["ult"] = "BOT COMPRO en " + str(oro)
                            telegram("JEFE COMPRE ORO en " + str(oro) + " Balance " + str(BOT["balance"]))
                            if BROKER_KEY:
                                enviar_orden_real("COMPRAR", oro)
                                BOT["modo"] = "REAL - Dinero real"
                    if BOT["pos"] == "COMPRAR":
                        oro2 = precio("GC=F") or BOT["entrada"]
                        gan = oro2 - BOT["entrada"]
                        cerrar = False
                        motivo = ""
                        sl_dinamico = -10
                        if gan >= 10:
                            sl_dinamico = 5
                        if gan >= 20:
                            cerrar = True
                            motivo = "TP Gane 20"
                        if gan <= sl_dinamico:
                            cerrar = True
                            if sl_dinamico == 5:
                                motivo = "TRAILING Asegure 5"
                            else:
                                motivo = "SL Perdi 10"
                        if cerrar:
                            if gan > 20:
                                gan = 20
                            if gan < -10:
                                gan = -10
                            BOT["balance"] += gan
                            if gan >= 0:
                                BOT["ganadas"] += 1
                            else:
                                BOT["perdidas"] += 1
                                BOT["perdidas_dia"] += 1
                            BOT["ult"] = motivo + " Balance " + str(BOT["balance"])
                            telegram("JEFE " + motivo + " en " + str(oro2) + " Balance " + str(BOT["balance"]) + " Ganadas " + str(BOT["ganadas"]) + " Perdidas " + str(BOT["perdidas"]))
                            BOT["pos"] = None
            time.sleep(10)
        except:
            time.sleep(5)

# OREJAS - ESCUCHA TELEGRAM Y RESPONDE
def telegram_escuchar():
    while True:
        try:
            if not TELE_TOKEN:
                time.sleep(10)
                continue
            u = "https://api.telegram.org/bot" + TELE_TOKEN + "/getUpdates?offset=" + str(ULTIMO_ID[0]+1) + "&timeout=10"
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.loads(r.read().decode())
                for up in d.get("result", []):
                    ULTIMO_ID[0] = up["update_id"]
                    msg = up.get("message", {})
                    texto = msg.get("text", "").lower()
                    chat = str(msg.get("chat", {}).get("id", ""))
                    if not chat:
                        continue
                    oro = precio("GC=F") or 4065
                    if "/start" in texto:
                        telegram("Hola JEFE Soy VIP ORO Raudy Escribe /precio para ORO, /senal para SENAL, /todo para todo", chat)
                    elif "/precio" in texto or "/todo" in texto:
                        telegram("JEFE ORO AHORA: " + str(oro) + " Balance: " + str(BOT["balance"]) + " Bot: " + ("PRENDIDO" if BOT["activo"] else "APAGADO") + " Ganadas: " + str(BOT["ganadas"]) + " Perdidas: " + str(BOT["perdidas"]), chat)
                    elif "/senal" in texto:
                        dec = cerebro(oro, HIST)
                        telegram("JEFE SENAL: " + dec + " ORO: " + str(oro) + " RSI: " + str(round(rsi(HIST),1)) + " MACD: " + ("SUBIENDO" if macd(HIST) > 0 else "BAJANDO") + " Bollinger: " + boll(HIST) + " Doble: " + ("CONFIRMADO" if doble(HIST) else "ESPERA"), chat)
                    elif texto.strip() != "":
                        telegram("JEFE escribe /precio para ver el oro, /senal para la senal", chat)
        except:
            time.sleep(5)
threading.Thread(target=telegram_escuchar, daemon=True).start()
threading.Thread(target=bot_motor, daemon=True).start()

HTML = """
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RAUDY VIP PRO</title>
<style>
body{margin:0;font-family:Arial;background:#0a0a0a;color:#fff;padding:12px}
.top{background:gold;color:#000;padding:16px;border-radius:16px;text-align:center}
.top h1{margin:0;font-size:30px}
.card{background:#1a1a1a;border-radius:18px;padding:16px;margin-top:12px;border:2px solid #333}
.big{font-size:55px;font-weight:bold;text-align:center;color:#00ff88}
.cen{text-align:center;font-size:16px}
.btn{width:100%;padding:18px;font-size:22px;font-weight:bold;border:none;border-radius:14px;margin-top:10px}
.verde{background:#00c853;color:#fff}
.rojo{background:#d50000;color:#fff}
.morado{background:#7b1fa2;color:#fff}
.azul{background:#00bcd4;color:#fff}
.naranja{background:#ff9800;color:#000}
.oro{background:gold;color:#000}
input,select{width:100%;padding:14px;font-size:20px;border-radius:12px;border:none;margin-top:8px}
</style></head><body>
<div class="top"><h1>RAUDY VIP PRO</h1><p>PROFESIONAL - EN VIVO</p><p id="estado">CONECTANDO...</p></div>
<div class="card">
<h2 style="text-align:center">BOT AUTO - PROFESIONAL</h2>
<p class="cen">RSI: <b id="rsi" style="color:gold">--</b> | MACD: <b id="macd" style="color:#00bcd4">--</b></p>
<p class="cen">Bollinger: <b id="boll" style="color:#ff9800">--</b> | Doble: <b id="doble" style="color:#00ff88">--</b></p>
<p class="cen">Balance: <b id="balance" style="color:#00ff88">$1000</b></p>
<p class="cen" id="bot-est">BOT APAGADO</p>
<p class="cen" id="perf">Ganadas: 0 | Perdidas: 0</p>
<p class="cen" id="pro-info" style="background:#000;padding:8px;border-radius:10px">PRO: Telegram | Freno 3 perdidas | Sin noticias | Trailing | Broker listo</p>
<p class="cen" style="background:#000;padding:8px;border-radius:10px">RIESGO 1:2 - Gano $20 | Pierdo $10 | Trailing asegura $5</p>
<button class="btn morado" id="btn-bot" onclick="toggleBot()">PRENDER BOT AUTO</button>
<button class="btn azul" onclick="hacerBack()">BACKTEST REAL</button>
<p class="cen" id="back-res" style="background:#000;padding:10px;border-radius:10px">Sin backtest todavia</p>
</div>
<div class="card">
<h2 style="text-align:center">ORO EN VIVO</h2>
<div class="big" id="precio">----</div>
<p class="cen" id="cerebro">CEREBRO: ESPERA</p>
<p class="cen" id="senal">SENAL: ESPERA</p>
<button class="btn naranja" onclick="activarVoz()">ACTIVAR VOZ</button>
</div>
<div class="card">
<h2 style="text-align:center">ELIGE ACTIVO</h2>
<select id="activo" onchange="cambiar()"><option value="ORO">ORO</option><option value="TESLA">TESLA</option><option value="APPLE">APPLE</option><option value="META">META</option><option value="EUR/USD">EUR/USD</option><option value="BTC">BTC</option></select>
<p class="cen">TP</p><input id="tp" value="4200" type="number">
<p class="cen">SL</p><input id="sl" value="4100" type="number">
<button class="btn verde" onclick="operar('COMPRAR')">COMPRAR</button>
<button class="btn rojo" onclick="operar('VENDER')">VENDER</button>
</div>
<div class="card">
<h2 style="text-align:center">PRECIOS</h2>
<p class="cen" id="lista">Cargando...</p>
</div>
<div class="card">
<h2 style="text-align:center">HABLAME JEFE</h2>
<a href="https://t.me/raudy_vip_oro_bot"><button class="btn" style="background:#0088cc;color:#fff">TELEGRAM</button></a>
<a href="https://wa.me/41767574050"><button class="btn" style="background:#25D366;color:#fff">WHATSAPP</button></a>
<a href="https://paypal.me/RaudyManzueta/20"><button class="btn oro">PAGAR $20 - PAYPAL</button></a>
</div>
<script>
let precios={};let act="ORO";let voz=false;
function hablar(t){let v=new SpeechSynthesisUtterance(t);v.lang='es-DO';speechSynthesis.speak(v);}
function activarVoz(){voz=true;hablar('Jefe voz activada');alert('VOZ ACTIVADA');}
function cambiar(){act=document.getElementById('activo').value;actualizar();}
function operar(t){hablar('Jefe voy a '+t);alert('Orden '+t+' '+act);}
async function toggleBot(){let r=await fetch('/api/bot_auto',{method:'POST'});let d=await r.json();document.getElementById('btn-bot').innerText=d.activo?'APAGAR BOT AUTO':'PRENDER BOT AUTO';document.getElementById('bot-est').innerText=d.ult;hablar(d.activo?'Bot prendido':'Bot apagado');}
async function hacerBack(){document.getElementById('back-res').innerText='Probando con datos reales...';let r=await fetch('/api/backtest');let d=await r.json();document.getElementById('back-res').innerHTML='Modo '+d.modo+'<br>Final $'+d.balance_final+'<br>Ganadas '+d.ganadas+' Perdidas '+d.perdidas+' Win '+d.winrate+'%';hablar('Backtest listo '+d.balance_final+' dolares');}
function actualizar(){if(precios[act]){document.getElementById('precio').innerText=precios[act];}}
async function cargar(){try{let r=await fetch('/api/precios');precios=await r.json();document.getElementById('estado').innerText='EN VIVO '+new Date().toLocaleTimeString();let h='';for(let k in precios){h+=k+': '+precios[k]+'<br>';}document.getElementById('lista').innerHTML=h;actualizar();let s=await fetch('/api/senal');let sd=await s.json();document.getElementById('cerebro').innerText='CEREBRO: '+sd.decision;document.getElementById('senal').innerText='SENAL: '+sd.decision;document.getElementById('rsi').innerText=sd.rsi;document.getElementById('macd').innerText=sd.macd;document.getElementById('boll').innerText=sd.bollinger;document.getElementById('doble').innerText=sd.doble;let b=await fetch('/api/bot_auto');let bd=await b.json();document.getElementById('balance').innerText='$'+bd.balance;document.getElementById('bot-est').innerText=bd.ult;document.getElementById('perf').innerText='Ganadas: '+bd.ganadas+' | Perdidas: '+bd.perdidas;document.getElementById('btn-bot').innerText=bd.activo?'APAGAR BOT AUTO':'PRENDER BOT AUTO';}catch(e){document.getElementById('estado').innerText='Sin internet...';}}
cargar();setInterval(cargar,3000);
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/api/precios")
def api_precios():
    oro = precio("GC=F") or 4149
    tes = precio("TSLA") or 378
    apl = precio("AAPL") or 350
    met = precio("META") or 641
    eur = precio("EURUSD=X") or 1.16
    return jsonify({"ORO": oro, "TESLA": tes, "APPLE": apl, "META": met, "EUR/USD": eur, "BTC": 90000})

@app.route("/api/senal")
def api_senal():
    oro = precio("GC=F") or 4149
    dec = cerebro(oro, HIST)
    rr = rsi(HIST)
    mc = macd(HIST)
    bb = boll(HIST)
    dd = doble(HIST)
    txt = "CONFIRMADO" if dd else "ESPERA"
    return jsonify({"precio": oro, "decision": dec, "rsi": round(rr, 1), "macd": "SUBIENDO" if mc > 0 else "BAJANDO", "bollinger": bb, "doble": txt, "noticias": noticias_peligrosas()})

@app.route("/api/bot_auto", methods=["GET", "POST"])
def api_bot():
    if request.method == "POST":
        BOT["activo"] = not BOT["activo"]
        if BOT["activo"]:
            BOT["ult"] = "BOT PRENDIDO - Dinero falso"
            telegram("JEFE Bot prendido - Modo practica")
        else:
            BOT["ult"] = "BOT APAGADO"
            BOT["pos"] = None
    return jsonify(BOT)

@app.route("/api/backtest")
def api_back():
    return jsonify(backtest())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
