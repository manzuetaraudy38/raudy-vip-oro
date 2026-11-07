from flask import Flask
from flask import jsonify, request
import requests, json, os, re
from datetime import datetime
app = Flask(__name__)

def load(n, d):
    try:
        if os.path.exists(n):
            return json.load(open(n))
    except:
        pass
    return d

def save(n, d):
    try:
        json.dump(d, open(n, "w"))
    except:
        pass

C = load("c.json", {
    "h": [], "c": 0, "v": 0,
    "e": 0, "l": "Nada aun jefe."
})
M5 = load("m5.json", {
    "v": [], "u": "Nada M5 aun.",
    "s": 0, "b": 0
})
CAP = load("cap.json", {
    "h": [], "u": "Nada Capital aun.",
    "c": 0, "b": 0
})
T212 = load("t212.json", {
    "h": [], "u": "Nada T212 aun.",
    "c": 0, "b": 0, "e": 0
})

def yahoo(s, fb):
    try:
        u = "https://query1.finance.yahoo.com"
        u += "/v8/finance/chart/" + s
        r = requests.get(u, headers={
            "User-Agent": "Mozilla/5.0"
        }, timeout=5)
        j = r.json()
        return float(j["chart"]["result"][0]["meta"]["regularMarketPrice"])
    except:
        return fb

def oro_real():
    try:
        r = requests.get(
            "https://api.gold-api.com/price/XAU",
            timeout=4)
        return float(r.json().get("price", 4088))
    except:
        return yahoo("GC=F", 4088)

def aprende(oro, orden):
    if "COMPRA" in orden or oro <= 3910:
        C["c"] += 1
        dec = "COMPRA"
    elif "VENTA" in orden or oro >= 3970:
        C["v"] += 1
        dec = "VENTA"
    else:
        C["e"] += 1
        dec = "ESPERA"
    if oro <= 3910:
        C["l"] = "ORO bajo a " + str(oro) + ". Despues SUBIO."
    elif oro >= 3970:
        C["l"] = "ORO subio a " + str(oro) + ". Despues BAJO."
    else:
        C["l"] = "ORO en " + str(oro) + ". Me acuerdo."
    C["h"].append({
        "hora": datetime.now().strftime("%H:%M"),
        "oro": oro, "d": dec
    })
    C["h"] = C["h"][-20:]
    save("c.json", C)

def m5_aprende(p):
    M5["v"].append({
        "hora": datetime.now().strftime("%H:%M"),
        "p": p
    })
    M5["v"] = M5["v"][-20:]
    if len(M5["v"]) >= 3:
        a = M5["v"][-3]["p"]
        b = M5["v"][-2]["p"]
        c = M5["v"][-1]["p"]
        if c > b > a:
            M5["s"] += 1
            M5["b"] = 0
            M5["u"] = "M5 subio 3 velas "
            M5["u"] += str(a) + ">" + str(b) + ">" + str(c)
            M5["u"] += ". Despues BAJO. No compres arriba."
        elif c < b < a:
            M5["b"] += 1
            M5["s"] = 0
            M5["u"] = "M5 bajo 3 velas "
            M5["u"] += str(a) + ">" + str(b) + ">" + str(c)
            M5["u"] += ". Despues SUBIO. Preparate COMPRA."
        else:
            M5["u"] = "M5 en " + str(c) + " mezclado. ESPERA."
    save("m5.json", M5)

def broker_aprende(D, pc, pr, nombre):
    dif = round(pc - pr, 2)
    if pc >= 3970:
        D["c"] += 1
        lec = nombre + " CARO $" + str(pc) + ". No compres."
    elif pc <= 3910:
        D["b"] += 1
        lec = nombre + " BARATO $" + str(pc) + ". SI compras."
    else:
        if "e" in D:
            D["e"] += 1
        lec = nombre + " MEDIO $" + str(pc) + ". ESPERA."
    D["u"] = lec
    D["h"].append({
        "hora": datetime.now().strftime("%H:%M"),
        "p": pc, "dif": dif
    })
    D["h"] = D["h"][-20:]
    return lec

def chat_robot(msg, oro, pc, pt):
    m = msg.lower()
    nums = re.findall(r"\d+\.?\d*", msg)
    q = float(nums[0]) if nums else 0
    if "hola" in m:
        return "Hola jefe. Dime: Quiero comprar a 3910"
    if "212" in m:
        return "Trading 212: $" + str(pt) + ". " + T212["u"]
    if "capital" in m:
        return "Capital.com: $" + str(pc) + ". " + CAP["u"]
    if "m5" in m:
        return "M5: " + M5["u"]
    if "stop" in m:
        return "STOP: Si entras 3910 pon STOP 3880. Si entras 3970 venta pon STOP 4000."
    if "gano" in m or "tengo" in m:
        d = float(nums[0]) if nums else 20
        g = round(d * 60 / 3910, 2)
        return "Con $" + str(d) + " en 3910 a 3970 ganas $" + str(g)
    if "compr" in m:
        if q == 0:
            return "Dime a que precio. Ej: Quiero comprar a 3910"
        if q <= 3940:
            return "SI JEFE COMPRA a $" + str(q) + " BARATO. ORO ahora $" + str(oro)
        if q >= 3970:
            return "NO JEFE a $" + str(q) + " CARO. Espera 3910."
        return "ESPERA jefe. Quieres " + str(q) + " espera 3910. ORO $" + str(oro)
    if "vend" in m:
        return "VENTA en 3970. ORO ahora $" + str(oro)
    return "Te entendi jefe: " + msg + ". ORO $" + str(oro) + " | T212 $" + str(pt) + " | Capital $" + str(pc)

def bancos():
    ev = [{
        "e": "FED Tasa USA", "i": "ALTO",
        "ef": "Si sube tasa ORO BAJA"
    }, {
        "e": "NFP Empleo USA", "i": "ALTO",
        "ef": "Empleo fuerte ORO BAJA"
    }, {
        "e": "CPI Inflacion", "i": "ALTO",
        "ef": "Inflacion alta ORO SUBE"
    }]
    return {
        "alerta": "SIN NOTICIA FUERTE",
        "riesgo": "VERDE",
        "eventos": ev
    }

def datos():
    oro = oro_real()
    d = {
        "ORO": oro,
        "NVDA": yahoo("NVDA", 185),
        "AAPL": yahoo("AAPL", 262),
        "TSLA": yahoo("TSLA", 340),
        "MSFT": yahoo("MSFT", 495),
        "AMZN": yahoo("AMZN", 235),
        "META": yahoo("META", 645),
        "GOOGL": yahoo("GOOGL", 282)
    }
    return d

# HTML en partes cortas para que no se rompa
H = []
H.append("<!DOCTYPE html><html lang='es'><head>")
H.append("<meta charset='UTF-8'>")
H.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
H.append("<title>RAUDY VIP</title>")
H.append("<style>body{background:#050505;color:#fff;font-family:Arial;text-align:center;margin:0}")
H.append("header{background:#FFD700;color:#000;padding:15px}")
H.append(".box{margin:10px;padding:15px;border-radius:15px;border:3px solid #FFD700}")
H.append(".m5{border-color:#00FF88}.cap{border-color:#00FFFF}.t212{border-color:#00FF88}")
H.append(".chat{border-color:#FFD700}.sl{border-color:#FF4444}")
H.append("input{width:100%;padding:12px;margin:4px 0;border-radius:10px;background:#111;color:#fff}")
H.append("button{width:100%;padding:14px;border-radius:15px;font-weight:bold;margin-top:5px}")
H.append(".grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}")
H.append(".robot{background:#1a1a1a;padding:10px;border-radius:12px}")
H.append("</style></head><body>")
H.append("<header><h1>👑 RAUDY VIP ⚡☄️</h1><p>JEFE RAUDY MANZUETA</p></header>")
H.append("<div class='box'><h2>🧠 CEREBRO</h2><p id='c1'>Cargando...</p><p id='c2'></p></div>")
H.append("<div class='box m5'><h2>🧠 CEREBRO M5</h2><p id='m1'></p><p id='m2'></p><p id='m3'></p></div>")
H.append("<div class='box cap'><h2>🏦 CEREBRO CAPITAL.COM</h2><p id='cap1'></p><p id='cap2'></p><p id='cap3'></p></div>")
H.append("<div class='box t212'><h2>🟢 CEREBRO TRADING 212</h2><p id='t1'></p><p id='t2'></p><p id='t3'></p></div>")
H.append("<div class='box chat'><h2>💬 CHAT - ESCRIBELE AL ROBOT</h2>")
H.append("<input id='chat' placeholder='Ej: Quiero comprar a 3910'>")
H.append("<button onclick='enviarChat()' style='background:#FFD700'>💬 ENVIAR</button>")
H.append("<p id='chatR' style='background:#111;padding:12px;border-radius:10px'>🤖 Hola jefe...</p>")
H.append("<button onclick=\"ej('Quiero comprar a 3910)')\" style='background:#00FF88'>✅ Quiero comprar a 3910</button>")
H.append("<button onclick=\"ej('Trading 212)')\" style='background:#00FFFF'>🟢 Trading 212</button>")
H.append("<button onclick=\"ej('Tengo 20 cuanto gano)')\" style='background:#FFD700'>💰 Tengo 20 cuanto gano</button></div>")
H.append("<div class='box'><h2>🤖 PREGUNTALE</h2>")
H.append("<input id='pq' type='number' placeholder='Ej 4070'>")
H.append("<button onclick='preg()' style='background:#00FF88'>🤖 PREGUNTAR</button><p id='pr'></p></div>")
H.append("<div class='box'><h2>🧮 CALCULADORA</h2>")
H.append("<input id='cd' type='number' value='20'>")
H.append("<input id='ce' type='number' value='3910'>")
H.append("<input id='cs' type='number' value='3970'>")
H.append("<button onclick='calc()' style='background:#FFD700'>🧮 CALCULAR</button><p id='cr'></p></div>")
H.append("<div class='box sl'><h2>🛑 STOP LOSS</h2>")
H.append("<input id='sd' type='number' value='20'>")
H.append("<input id='sr' type='number' value='5'>")
H.append("<input id='se' type='number' value='3910'>")
H.append("<input id='ss' type='number' value='3970'>")
H.append("<button onclick='sl()' style='background:#FF4444;color:#fff'>🛑 CALCULAR STOP</button><p id='slr'></p></div>")
H.append("<div class='box'><h2>👑 JEFE 40</h2><p id='j1'></p><p id='j2'></p></div>")
H.append("<div class='box'><h2>🏦 BANCOS</h2><p id='b1'></p><p id='b2'></p></div>")
H.append("<div class='box'><h2>🛰️ SATELITE USA</h2><p id='s1'></p><p id='s2'></p></div>")
H.append("<div class='box'><h2>🤖 40 ROBOTS</h2><div class='grid' id='grid'></div></div>")
H.append("<p>RAUDY VIP 2026 - WhatsApp 0767574050</p>")
H.append("<script>")
H.append("let robots=[];")
H.append("for(let i=1;i<=39;i++){robots.push(i)}")
H.append("let g=document.getElementById('grid');")
H.append("robots.forEach(n=>{let d=document.createElement('div');")
H.append("d.className='robot';")
H.append("d.innerHTML='<h3>Robot '+n+'</h3><p id=m'+n+'>Buscando...</p>';")
H.append("g.appendChild(d)});")
H.append("function hablar(t){try{let u=new SpeechSynthesisUtterance(t);u.lang='es-ES';speechSynthesis.speak(u)}catch(e){}}")
H.append("async function enviarChat(){let t=document.getElementById('chat').value;")
H.append("if(!t){document.getElementById('chatR').innerHTML='Escribe algo jefe';return}")
H.append("document.getElementById('chatR').innerHTML='Pensando...';")
H.append("let r=await fetch('/api/chat?msg='+encodeURIComponent(t));")
H.append("let d=await r.json();")
H.append("document.getElementById('chatR').innerHTML='🤖 '+d.respuesta;hablar(d.respuesta)}")
H.append("function ej(t){document.getElementById('chat').value=t;enviarChat()}")
H.append("async function preg(){let p=document.getElementById('pq').value;")
H.append("let r=await fetch('/api/preguntale?precio='+p);")
H.append("let d=await r.json();")
H.append("document.getElementById('pr').innerHTML='🤖 '+d.respuesta}")
H.append("function calc(){let d=parseFloat(document.getElementById('cd').value);")
H.append("let e=parseFloat(document.getElementById('ce').value);")
H.append("let s=parseFloat(document.getElementById('cs').value);")
H.append("let g=d*Math.abs(s-e)/e;")
H.append("document.getElementById('cr').innerHTML='Ganas $'+g.toFixed(2)+' Total $'+(d+g).toFixed(2)}")
H.append("function sl(){let d=parseFloat(document.getElementById('sd').value);")
H.append("let r=parseFloat(document.getElementById('sr').value);")
H.append("let e=parseFloat(document.getElementById('se').value);")
H.append("let s=parseFloat(document.getElementById('ss').value);")
H.append("let stop=e-Math.abs(s-e)/2;")
H.append("let g=r*2;")
H.append("document.getElementById('slr').innerHTML='ENTRADA $'+e+' STOP $'+stop.toFixed(0)+' BOTIN $'+s+' Ganas $'+g}")
H.append("async function up(){try{")
H.append("let r=await fetch('/api/satelite_usa');let d=await r.json();")
H.append("document.getElementById('c1').innerHTML=d.cerebro.mensaje;")
H.append("document.getElementById('c2').innerHTML=d.cerebro.leccion;")
H.append("document.getElementById('m1').innerHTML=d.cerebro_m5.mensaje;")
H.append("document.getElementById('m2').innerHTML=d.cerebro_m5.leccion;")
H.append("document.getElementById('m3').innerHTML='Velas: '+d.cerebro_m5.velas.map(v=>v.p).join(' -> ');")
H.append("document.getElementById('cap1').innerHTML=d.cerebro_capital.mensaje;")
H.append("document.getElementById('cap2').innerHTML=d.cerebro_capital.leccion;")
H.append("document.getElementById('cap3').innerHTML='Capital $'+d.capital.precio+' '+d.capital.recomendacion;")
H.append("document.getElementById('t1').innerHTML=d.cerebro_t212.mensaje;")
H.append("document.getElementById('t2').innerHTML=d.cerebro_t212.leccion;")
H.append("document.getElementById('t3').innerHTML='T212 $'+d.t212.precio+' '+d.t212.recomendacion;")
H.append("document.getElementById('j1').innerHTML=d.jefe.orden;")
H.append("document.getElementById('j2').innerHTML=d.jefe.mensaje;")
H.append("document.getElementById('b1').innerHTML=d.bancos.alerta;")
H.append("document.getElementById('b2').innerHTML=d.bancos.eventos.map(e=>e.e+' - '+e.ef).join('<br>');")
H.append("document.getElementById('s1').innerHTML='ORO $'+d.ORO+' NVDA $'+d.NVDA+' TSLA $'+d.TSLA;")
H.append("document.getElementById('s2').innerHTML='APPLE $'+d.AAPL+' MSFT $'+d.MSFT;")
H.append("robots.forEach(n=>{let el=document.getElementById('m'+n);")
H.append("if(el)el.innerHTML='ORO $'+d.ORO+' - '+d.jefe.orden})")
H.append("}catch(e){}}")
H.append("setInterval(up,15000);up();")
H.append("</script></body></html>")
HTML = "".join(H)

@app.route("/")
def home():
    return HTML

@app.route("/api/satelite_usa")
def sat():
    d = datos()
    oro = d["ORO"]
    if oro <= 3910:
        orden = "COMPRA"
    elif oro >= 3970:
        orden = "VENTA"
    else:
        orden = "ESPERA"
    aprende(oro, orden)
    m5_aprende(oro)
    cap = {"precio": oro, "recomendacion": "ESPERA"}
    cap["recomendacion"] = "BARATO" if oro <= 3910 else ("CARO" if oro >= 3970 else "ESPERA")
    broker_aprende(CAP, oro, oro, "Capital.com")
    save("cap.json", CAP)
    t212 = {"precio": oro, "recomendacion": cap["recomendacion"]}
    broker_aprende(T212, oro, oro, "Trading 212")
    save("t212.json", T212)
    jefe = {
        "orden": "🟢 PERMISO" if orden != "ESPERA" else "🟡 ESPERA",
        "mensaje": "JEFE DICE: ORO $" + str(oro) + " - " + orden
    }
    return jsonify({
        **d, "cerebro": {
            "mensaje": "Me acuerdo de " + str(C["c"] + C["v"] + C["e"]) + " jugadas",
            "leccion": C["l"]
        },
        "cerebro_m5": {
            "mensaje": "M5 - " + str(len(M5["v"])) + " velas",
            "leccion": M5["u"],
            "velas": M5["v"][-5:]
        },
        "cerebro_capital": {
            "mensaje": "Capital - " + str(len(CAP["h"])) + " jugadas",
            "leccion": CAP["u"]
        },
        "cerebro_t212": {
            "mensaje": "T212 - " + str(len(T212["h"])) + " jugadas",
            "leccion": T212["u"]
        },
        "capital": cap, "t212": t212,
        "jefe": jefe, "bancos": bancos()
    })

@app.route("/api/chat")
def api_chat():
    msg = request.args.get("msg", "")
    oro = oro_real()
    r = chat_robot(msg, oro, oro, oro)
    return jsonify({"respuesta": r})

@app.route("/api/preguntale")
def api_preg():
    try:
        pq = float(request.args.get("precio", 4070))
        pa = oro_real()
        if pq <= 3940:
            res = "SI JEFE COMPRA a $" + str(pq) + " BARATO"
        elif pq >= 3970:
            res = "NO JEFE a $" + str(pq) + " CARO espera 3910"
        else:
            res = "ESPERA jefe espera 3910. ORO ahora $" + str(pa)
        return jsonify({"respuesta": res, "precio_actual": pa})
    except:
        return jsonify({"respuesta": "Escribe numero Ej 4070"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
