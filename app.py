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

MEM = load("mem.json", {
    "h": [], "c": 0, "v": 0, "e": 0,
    "l": "Nada aun jefe."
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

CEREBROS = []
for i in range(1, 101):
    if i <= 15:
        rol = "M5 ORO"
    elif i <= 30:
        rol = "DIVISAS EUR GBP JPY"
    elif i <= 45:
        rol = "BITCOIN BTC ETH"
    elif i <= 60:
        rol = "Capital.com"
    elif i <= 75:
        rol = "Trading 212"
    elif i <= 85:
        rol = "APPLE TESLA NVDA"
    elif i <= 99:
        rol = "MEJORES ACCIONES"
    else:
        rol = "JEFE RAUDY ORO"
    CEREBROS.append({
        "id": i, "rol": rol,
        "estado": "VIVO",
        "jefe": "RAUDY ORO"
    })

# ZONAS PARA TODO
ZONAS = {
    "ORO": {"c": 3910, "v": 3970},
    "EURUSD": {"c": 1.1150, "v": 1.1250},
    "GBPUSD": {"c": 1.2700, "v": 1.2850},
    "USDJPY": {"c": 148.00, "v": 151.00},
    "USDCHF": {"c": 0.8800, "v": 0.8950},
    "AUDUSD": {"c": 0.6500, "v": 0.6650},
    "BTC": {"c": 95000, "v": 108000},
    "ETH": {"c": 3200, "v": 3800},
    "AAPL": {"c": 255, "v": 270},
    "TSLA": {"c": 330, "v": 355},
    "NVDA": {"c": 180, "v": 195},
    "MSFT": {"c": 490, "v": 505},
    "AMZN": {"c": 230, "v": 245},
    "META": {"c": 640, "v": 660},
    "GOOGL": {"c": 280, "v": 292},
    "NFLX": {"c": 750, "v": 790},
    "AMD": {"c": 120, "v": 135}
}

NOMBRES = {
    "ORO": "ORO 🥇",
    "EURUSD": "EUR/USD 💶",
    "GBPUSD": "GBP/USD 💷",
    "USDJPY": "USD/JPY 💴",
    "USDCHF": "USD/CHF 🇨🇭",
    "AUDUSD": "AUD/USD 🦘",
    "BTC": "BITCOIN ₿",
    "ETH": "ETHEREUM Ξ",
    "AAPL": "APPLE 🍎",
    "TSLA": "TESLA 🚗",
    "NVDA": "NVIDIA 💚",
    "MSFT": "MICROSOFT 🪟",
    "AMZN": "AMAZON 📦",
    "META": "META 👍",
    "GOOGL": "GOOGLE 🔍",
    "NFLX": "NETFLIX 🎬",
    "AMD": "AMD 🔴"
}

def yahoo(s, fb):
    try:
        u = "https://query1.finance.yahoo.com"
        u += "/v8/finance/chart/" + s
        r = requests.get(u, headers={
            "User-Agent": "Mozilla/5.0"
        }, timeout=5)
        j = r.json()
        v = j["chart"]["result"][0]["meta"]
        return float(v["regularMarketPrice"])
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

def todos_precios():
    oro = oro_real()
    d = {
        "ORO": oro,
        "EURUSD": yahoo("EURUSD=X", 1.1150),
        "GBPUSD": yahoo("GBPUSD=X", 1.2750),
        "USDJPY": yahoo("USDJPY=X", 149.5),
        "USDCHF": yahoo("USDCHF=X", 0.8850),
        "AUDUSD": yahoo("AUDUSD=X", 0.6550),
        "BTC": yahoo("BTC-USD", 98000),
        "ETH": yahoo("ETH-USD", 3400),
        "AAPL": yahoo("AAPL", 262),
        "TSLA": yahoo("TSLA", 340),
        "NVDA": yahoo("NVDA", 185),
        "MSFT": yahoo("MSFT", 495),
        "AMZN": yahoo("AMZN", 235),
        "META": yahoo("META", 645),
        "GOOGL": yahoo("GOOGL", 282),
        "NFLX": yahoo("NFLX", 765),
        "AMD": yahoo("AMD", 125)
    }
    return d

def aprende(oro, orden):
    if "COMPRA" in orden or oro <= 3910:
        MEM["c"] += 1
        dec = "COMPRA"
    elif "VENTA" in orden or oro >= 3970:
        MEM["v"] += 1
        dec = "VENTA"
    else:
        MEM["e"] += 1
        dec = "ESPERA"
    if oro <= 3910:
        MEM["l"] = "ORO bajo a " + str(oro)
        MEM["l"] += ". Despues SUBIO."
    elif oro >= 3970:
        MEM["l"] = "ORO subio a " + str(oro)
        MEM["l"] += ". Despues BAJO."
    else:
        MEM["l"] = "ORO en " + str(oro)
        MEM["l"] += ". Me acuerdo jefe."
    MEM["h"].append({
        "hora": datetime.now().strftime("%H:%M"),
        "oro": oro, "d": dec
    })
    MEM["h"] = MEM["h"][-20:]
    save("mem.json", MEM)

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
            M5["u"] += str(a) + ">" + str(b)
            M5["u"] += ">" + str(c)
            M5["u"] += ". Despues BAJO."
        elif c < b < a:
            M5["b"] += 1
            M5["s"] = 0
            M5["u"] = "M5 bajo 3 velas "
            M5["u"] += str(a) + ">" + str(b)
            M5["u"] += ">" + str(c)
            M5["u"] += ". Despues SUBIO."
        else:
            M5["u"] = "M5 en " + str(c)
            M5["u"] += " mezclado. ESPERA."
    save("m5.json", M5)

def broker_aprende(D, pc, pr, nombre):
    if pc >= 3970:
        D["c"] += 1
        lec = nombre + " CARO $" + str(pc)
    elif pc <= 3910:
        D["b"] += 1
        lec = nombre + " BARATO $" + str(pc)
    else:
        if "e" in D:
            D["e"] += 1
        lec = nombre + " MEDIO $" + str(pc)
    D["u"] = lec
    D["h"].append({
        "hora": datetime.now().strftime("%H:%M"),
        "p": pc
    })
    D["h"] = D["h"][-20:]
    return lec

def calc_lote(lote, ganar, perder, precio, lado, activo):
    # ORO y ACCIONES: 0.01 = $1 por $1
    # DIVISAS: 0.01 = $1 por 0.0001? simplificado jefe
    # BTC: 0.01 = $1 por $1
    div = lote * 100
    if activo in ["EURUSD", "GBPUSD", "AUDUSD"]:
        # en divisas 0.01 lote = $0.10 por pip
        # para ganar $5 necesitas 50 pips = 0.0050
        d_tp = ganar * 0.001
        d_sl = perder * 0.001
    elif activo in ["USDJPY", "USDCHF"]:
        d_tp = ganar * 0.01
        d_sl = perder * 0.01
    else:
        if div == 0:
            div = 1
        d_tp = ganar / div
        d_sl = perder / div
    if lado == "COMPRA":
        tp = precio + d_tp
        sl = precio - d_sl
    else:
        tp = precio - d_tp
        sl = precio + d_sl
    return tp, sl, d_tp, d_sl

def busca_activo(m):
    if "bitcoin" in m or "btc" in m:
        return "BTC"
    if "ethereum" in m or "eth" in m:
        return "ETH"
    if "euro" in m or "eur" in m:
        return "EURUSD"
    if "libra" in m or "gbp" in m:
        return "GBPUSD"
    if "yen" in m or "jpy" in m:
        return "USDJPY"
    if "franco" in m or "chf" in m:
        return "USDCHF"
    if "aud" in m or "austral" in m:
        return "AUDUSD"
    if "apple" in m or "aapl" in m:
        return "AAPL"
    if "tesla" in m or "tsla" in m:
        return "TSLA"
    if "nvidia" in m or "nvda" in m:
        return "NVDA"
    if "microsoft" in m or "msft" in m:
        return "MSFT"
    if "amazon" in m or "amzn" in m:
        return "AMZN"
    if "meta" in m:
        return "META"
    if "google" in m or "googl" in m:
        return "GOOGL"
    if "netflix" in m or "nflx" in m:
        return "NFLX"
    if "amd" in m:
        return "AMD"
    return "ORO"

def chat_robot(msg, precios):
    m = msg.lower()
    nums = re.findall(r"\d+\.?\d*", msg)
    activo = busca_activo(m)
    precio = precios.get(activo, 4088)
    nombre = NOMBRES.get(activo, activo)
    lote = 0.01
    ganar = 5.0
    perder = 2.0
    if "0.02" in msg:
        lote = 0.02
    if "0.05" in msg:
        lote = 0.05
    if "0.1" in msg:
        lote = 0.1
    if "0.5" in msg:
        lote = 0.5
    if "1 lote" in m or "1.0" in msg:
        lote = 1.0
    if "ganar" in m and len(nums) >= 2:
        try:
            ganar = float(nums[-2])
            perder = float(nums[-1])
        except:
            pass
    if "hola" in m:
        return "Hola jefe RAUDY ORO. 100 cerebros en vivo. Tengo DIVISAS BITCOIN APPLE TESLA ACCIONES. Dime: compro 0.01 bitcoin para ganar 5 y perder 2"
    if "212" in m:
        return "Trading 212 jefe: ORO $" + str(precios["ORO"]) + ". " + T212["u"]
    if "capital" in m:
        return "Capital.com jefe: ORO $" + str(precios["ORO"]) + ". " + CAP["u"]
    if "m5" in m:
        return "M5 jefe: " + M5["u"]
    if "mejor" in m or "mejores" in m:
        return "Jefe las mejores hoy: ORO $" + str(precios["ORO"]) + " BTC $" + str(precios["BTC"]) + " APPLE $" + str(precios["AAPL"]) + " TESLA $" + str(precios["TSLA"]) + " NVDA $" + str(precios["NVDA"]) + ". Dime cual quieres y te digo TP SL."
    if "cuanto puedo comprar" in m or "a cuanto compro" in m or "a cuanto puedo compra" in m:
        z = ZONAS[activo]
        return "Jefe puedes COMPRAR " + nombre + " en " + str(z["c"]) + ". Ahora $" + str(precio) + ". Si baja a " + str(z["c"]) + " COMPRA."
    if "cuanto puedo vender" in m or "a cuanto vendo" in m or "a cuanto puedo vende" in m:
        z = ZONAS[activo]
        return "Jefe puedes VENDER " + nombre + " en " + str(z["v"]) + ". Ahora $" + str(precio) + ". Si sube a " + str(z["v"]) + " VENTA."
    if "donde pongo" in m and ("tp" in m or "sl" in m):
        tp, sl, dt, ds = calc_lote(0.01, 5, 2, precio, "COMPRA", activo)
        r = "Jefe " + nombre + " en $" + str(precio) + " 0.01 para ganar $5 perder $2: "
        r += "COMPRA $" + str(round(precio, 4)) + " TP $" + str(round(tp, 4))
        r += " SL $" + str(round(sl, 4)) + ". 100 cerebros en vivo."
        return r
    if "compr" in m:
        if "ganar" in m or "gana" in m or "perder" in m:
            z = ZONAS[activo]
            entrada = z["c"] if precio > z["c"] and precio < z["v"] else precio
            if precio <= z["c"]:
                entrada = precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "COMPRA", activo)
            r = "Jefe RAUDY LISTO 100 cerebros en vivo: "
            r += "COMPRA " + nombre + " " + str(lote) + " lote en " + str(round(entrada, 4))
            r += " TP " + str(round(tp, 4)) + " ganas $" + str(ganar)
            r += " SL " + str(round(sl, 4)) + " pierdes $" + str(perder)
            r += ". Ahora $" + str(precio) + ". M5: " + M5["u"]
            return r
        if len(nums) > 0:
            q = float(nums[0])
            z = ZONAS[activo]
            if q <= z["c"] + 1:
                return "SI JEFE COMPRA " + nombre + " a " + str(q) + " BARATO. Ahora $" + str(precio)
            return "ESPERA jefe espera " + str(z["c"]) + ". " + nombre + " ahora $" + str(precio)
        return "Dime: compro 0.01 bitcoin para ganar 5 y perder 2"
    if "vend" in m:
        if "ganar" in m or "perder" in m:
            z = ZONAS[activo]
            entrada = z["v"] if precio > z["c"] and precio < z["v"] else precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "VENTA", activo)
            r = "Jefe VENTA " + nombre + " " + str(lote) + " en " + str(round(entrada, 4))
            r += " TP " + str(round(tp, 4)) + " ganas $" + str(ganar)
            r += " SL " + str(round(sl, 4)) + " pierdes $" + str(perder)
            return r
        return "VENTA " + nombre + " en " + str(ZONAS[activo]["v"]) + " jefe. Ahora $" + str(precio)
    if "tp" in m or "sl" in m:
        tp, sl, dt, ds = calc_lote(lote, ganar, perder, precio, "COMPRA", activo)
        return "Jefe " + nombre + " TP " + str(round(tp, 4)) + " SL " + str(round(sl, 4)) + " con 0.01 en $" + str(precio)
    return "Te entendi jefe: " + msg + ". " + nombre + " en vivo $" + str(precio) + ". Dime: compro 0.01 para ganar 5 y perder 2"

H = []
H.append("<!DOCTYPE html><html lang='es'><head>")
H.append("<meta charset='UTF-8'>")
H.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
H.append("<title>RAUDY VIP 100 TODO MERCADO</title>")
H.append("<style>body{background:#050505;color:#fff;font-family:Arial;text-align:center;margin:0}")
H.append("header{background:#FFD700;color:#000;padding:15px}")
H.append(".box{margin:10px;padding:15px;border-radius:15px;border:3px solid #FFD700}")
H.append(".m5{border-color:#00FF88}.cap{border-color:#00FFFF}.t212{border-color:#00FF88}")
H.append(".chat{border-color:#FFD700}.sl{border-color:#FF4444}.vivo{border-color:#00FF88}")
H.append(".divisas{border-color:#00FFFF}.btc{border-color:#FFA500}.acc{border-color:#00FF88}")
H.append("input{width:100%;padding:12px;margin:4px 0;border-radius:10px;background:#111;color:#fff}")
H.append("button{width:100%;padding:14px;border-radius:15px;font-weight:bold;margin-top:5px}")
H.append(".grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px}")
H.append(".robot{background:#1a1a1a;padding:8px;border-radius:12px;font-size:12px}")
H.append(".luz{width:14px;height:14px;border-radius:50%;background:#00FF88;margin:auto}")
H.append(".act{background:#1a1a1a;border:1px solid #333;padding:8px;border-radius:12px;font-size:12px}")
H.append("</style></head><body>")
H.append("<header><h1>👑 RAUDY VIP 100 CEREBROS ⚡</h1>")
H.append("<p>JEFE: RAUDY ORO - TODO EL MERCADO EN VIVO 🟢</p>")
H.append("<p id='vivo'>🟢 EN VIVO...</p></header>")
H.append("<div class='box vivo'><h2>🟢 EN VIVO EN DIRECTO</h2><p id='vivo2'>Conectando...</p>")
H.append("<p>Se actualiza solo cada 5 segundos.</p></div>")
H.append("<div class='box'><h2>🧠 CEREBRO JEFE</h2><p id='c1'></p><p id='c2'></p></div>")
H.append("<div class='box m5'><h2>🧠 CEREBRO M5</h2><p id='m1'></p><p id='m2'></p><p id='m3'></p></div>")
H.append("<div class='box cap'><h2>🏦 CAPITAL.COM</h2><p id='cap1'></p><p id='cap2'></p></div>")
H.append("<div class='box t212'><h2>🟢 TRADING 212</h2><p id='t1'></p><p id='t2'></p></div>")
H.append("<div class='box chat'><h2>💬 CHAT LOTE 0.01 - TODO MERCADO</h2>")
H.append("<p>Escribe: compro 0.01 bitcoin para ganar 5 y perder 2</p>")
H.append("<input id='chat' placeholder='Ej: compro 0.01 bitcoin para ganar 5 y perder 2'>")
H.append("<button onclick='enviarChat()' style='background:#FFD700'>💬 ENVIAR</button>")
H.append("<p id='chatR' style='background:#111;padding:12px;border-radius:10px;text-align:left'>🤖 Hola jefe...</p>")
H.append("<button onclick=\"ej('compro 0.01 para ganar 5 y perder 2)')\" style='background:#00FF88'>✅ ORO 0.01 ganar 5 perder 2</button>")
H.append("<button onclick=\"ej('compro 0.01 bitcoin para ganar 5 y perder 2)')\" style='background:#FFA500'>₿ BITCOIN 0.01 ganar 5 perder 2</button>")
H.append("<button onclick=\"ej('compro 0.01 euro para ganar 5 y perder 2)')\" style='background:#00FFFF'>💶 EUR/USD 0.01 ganar 5 perder 2</button>")
H.append("<button onclick=\"ej('compro 0.01 apple para ganar 5 y perder 2)')\" style='background:#00FF88'>🍎 APPLE 0.01 ganar 5 perder 2</button>")
H.append("<button onclick=\"ej('compro 0.01 tesla para ganar 5 y perder 2)')\" style='background:#FF4444;color:#fff'>🚗 TESLA 0.01 ganar 5 perder 2</button>")
H.append("<button onclick=\"ej('a cuanto puedo comprar bitcoin)')\" style='background:#FFD700'>🟢 a cuanto compro bitcoin</button>")
H.append("<button onclick=\"ej('cuales son las mejores acciones)')\" style='background:#00FFFF'>📈 mejores acciones</button></div>")
H.append("<div class='box divisas'><h2>💶 DIVISAS EN VIVO</h2><p id='divisas'></p></div>")
H.append("<div class='box btc'><h2>₿ BITCOIN + ETH EN VIVO</h2><p id='crypto'></p></div>")
H.append("<div class='box acc'><h2>📈 MEJORES ACCIONES EN VIVO</h2><p id='acciones'></p></div>")
H.append("<div class='box sl'><h2>🛑 CALCULADORA LOTE 0.01</h2>")
H.append("<select id='selAct'><option value='ORO'>ORO</option><option value='BTC'>BITCOIN</option><option value='EURUSD'>EUR/USD</option><option value='AAPL'>APPLE</option><option value='TSLA'>TESLA</option><option value='NVDA'>NVDA</option></select>")
H.append("<input id='lote' type='number' value='0.01' step='0.01'>")
H.append("<input id='ganar' type='number' value='5'>")
H.append("<input id='perder' type='number' value='2'>")
H.append("<input id='entrada' type='number' value='3910'>")
H.append("<button onclick='calcLote()' style='background:#FF4444;color:#fff'>🛑 CALCULAR TP SL</button>")
H.append("<p id='loteR' style='background:#111;padding:12px;border-radius:10px'></p></div>")
H.append("<div class='box'><h2>👑 JEFE 100 - RAUDY ORO</h2><p id='j1'></p><p id='j2'></p></div>")
H.append("<div class='box'><h2>🛰️ SATELITE EN VIVO</h2><p id='s1'></p><p id='s2'></p></div>")
H.append("<h2>🧠 LOS 100 CEREBROS EN VIVO</h2>")
H.append("<div class='grid' id='grid'></div>")
H.append("<p>RAUDY VIP 2026 - WhatsApp 0767574050</p>")
H.append("<script>")
H.append("let g=document.getElementById('grid');")
H.append("for(let i=1;i<=100;i++){let d=document.createElement('div');")
H.append("d.className='robot';")
H.append("let rol='M5';")
H.append("if(i>15 && i<=30) rol='DIVISAS';")
H.append("if(i>30 && i<=45) rol='BITCOIN';")
H.append("if(i>45 && i<=60) rol='Capital.com';")
H.append("if(i>60 && i<=75) rol='Trading 212';")
H.append("if(i>75 && i<=85) rol='APPLE TESLA';")
H.append("if(i>85 && i<100) rol='MEJORES ACCIONES';")
H.append("if(i==100) rol='JEFE RAUDY ORO';")
H.append("d.innerHTML='<div class=luz></div><b>Cerebro '+i+'</b><br>'+rol+'<br><span id=m'+i+'>VIVO</span>';")
H.append("g.appendChild(d)}")
H.append("function hablar(t){try{let u=new SpeechSynthesisUtterance(t);u.lang='es-ES';speechSynthesis.speak(u)}catch(e){}}")
H.append("async function enviarChat(){let t=document.getElementById('chat').value;")
H.append("if(!t){document.getElementById('chatR').innerHTML='Escribe algo jefe';return}")
H.append("document.getElementById('chatR').innerHTML='🤖 Pensando en vivo...';")
H.append("let r=await fetch('/api/chat?msg='+encodeURIComponent(t));")
H.append("let d=await r.json();")
H.append("document.getElementById('chatR').innerHTML='🤖 '+d.respuesta;hablar(d.respuesta)}")
H.append("function ej(t){document.getElementById('chat').value=t;enviarChat()}")
H.append("async function calcLote(){let lote=parseFloat(document.getElementById('lote').value);")
H.append("let ganar=parseFloat(document.getElementById('ganar').value);")
H.append("let perder=parseFloat(document.getElementById('perder').value);")
H.append("let ent=parseFloat(document.getElementById('entrada').value);")
H.append("let act=document.getElementById('selAct').value;")
H.append("let r=await fetch('/api/lote?lote='+lote+'&ganar='+ganar+'&perder='+perder+'&entrada='+ent+'&activo='+act);")
H.append("let d=await r.json();")
H.append("document.getElementById('loteR').innerHTML=d.respuesta;hablar(d.respuesta)}")
H.append("async function up(){try{")
H.append("let r=await fetch('/api/satelite_usa?v='+Date.now());let d=await r.json();")
H.append("document.getElementById('vivo').innerHTML='🟢 EN VIVO '+d.hora+' - ORO $'+d.ORO+' BTC $'+d.BTC;")
H.append("document.getElementById('vivo2').innerHTML='ORO $'+d.ORO+' BTC $'+d.BTC+' EUR $'+d.EURUSD+' EN VIVO 100 cerebros';")
H.append("document.getElementById('c1').innerHTML=d.cerebro.mensaje;")
H.append("document.getElementById('c2').innerHTML=d.cerebro.leccion;")
H.append("document.getElementById('m1').innerHTML=d.cerebro_m5.mensaje;")
H.append("document.getElementById('m2').innerHTML=d.cerebro_m5.leccion;")
H.append("document.getElementById('m3').innerHTML='Velas: '+d.cerebro_m5.velas.map(v=>v.p).join(' -> ');")
H.append("document.getElementById('cap1').innerHTML=d.cerebro_capital.mensaje;")
H.append("document.getElementById('cap2').innerHTML=d.cerebro_capital.leccion;")
H.append("document.getElementById('t1').innerHTML=d.cerebro_t212.mensaje;")
H.append("document.getElementById('t2').innerHTML=d.cerebro_t212.leccion;")
H.append("document.getElementById('divisas').innerHTML='EUR/USD $'+d.EURUSD+' | GBP/USD $'+d.GBPUSD+' | USD/JPY $'+d.USDJPY+' | USD/CHF $'+d.USDCHF+' | AUD/USD $'+d.AUDUSD;")
H.append("document.getElementById('crypto').innerHTML='BTC $'+d.BTC+' | ETH $'+d.ETH;")
H.append("document.getElementById('acciones').innerHTML='APPLE $'+d.AAPL+' | TESLA $'+d.TSLA+' | NVDA $'+d.NVDA+' | MSFT $'+d.MSFT+' | AMZN $'+d.AMZN+' | META $'+d.META+' | GOOGLE $'+d.GOOGL+' | NFLX $'+d.NFLX+' | AMD $'+d.AMD;")
H.append("document.getElementById('j1').innerHTML=d.jefe.orden;")
H.append("document.getElementById('j2').innerHTML=d.jefe.mensaje;")
H.append("document.getElementById('s1').innerHTML='ORO $'+d.ORO+' BTC $'+d.BTC+' EUR $'+d.EURUSD;")
H.append("document.getElementById('s2').innerHTML='APPLE $'+d.AAPL+' TESLA $'+d.TSLA;")
H.append("for(let i=1;i<=100;i++){let el=document.getElementById('m'+i);")
H.append("if(el)el.innerHTML='VIVO $'+d.ORO+' - '+d.jefe.orden}")
H.append("}catch(e){}}")
H.append("setInterval(up,5000);up();")
H.append("</script></body></html>")
HTML = "".join(H)

@app.route("/")
def home():
    return HTML

@app.route("/api/satelite_usa")
def sat():
    d = todos_precios()
    oro = d["ORO"]
    if oro <= 3910:
        orden = "COMPRA"
    elif oro >= 3970:
        orden = "VENTA"
    else:
        orden = "ESPERA"
    aprende(oro, orden)
    m5_aprende(oro)
    broker_aprende(CAP, oro, oro, "Capital.com")
    save("cap.json", CAP)
    broker_aprende(T212, oro, oro, "Trading 212")
    save("t212.json", T212)
    jefe = {
        "orden": "🟢 PERMISO" if orden != "ESPERA" else "🟡 ESPERA",
        "mensaje": "JEFE RAUDY ORO DICE: ORO $" + str(oro) + " - " + orden + " - 100 cerebros en vivo"
    }
    return jsonify({
        **d,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "cerebro": {
            "mensaje": "100 cerebros recuerdan " + str(MEM["c"] + MEM["v"] + MEM["e"]) + " jugadas",
            "leccion": MEM["l"]
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
        "jefe": jefe,
        "cerebros": CEREBROS,
        "total_cerebros": 100
    })

@app.route("/api/chat")
def api_chat():
    msg = request.args.get("msg", "")
    precios = todos_precios()
    r = chat_robot(msg, precios)
    return jsonify({"respuesta": r})

@app.route("/api/lote")
def api_lote():
    try:
        lote = float(request.args.get("lote", 0.01))
        ganar = float(request.args.get("ganar", 5))
        perder = float(request.args.get("perder", 2))
        ent = float(request.args.get("entrada", 3910))
        act = request.args.get("activo", "ORO")
        tp, sl, dt, ds = calc_lote(lote, ganar, perder, ent, "COMPRA", act)
        r = "COMPRA " + act + " " + str(lote)
        r += " en " + str(ent)
        r += " TP " + str(round(tp, 4)) + " ganas $" + str(ganar)
        r += " SL " + str(round(sl, 4)) + " pierdes $" + str(perder)
        r += ". 100 cerebros en vivo jefe."
        return jsonify({"respuesta": r, "tp": tp, "sl": sl})
    except:
        return jsonify({"respuesta": "Escribe lote 0.01 ganar 5 perder 2"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
