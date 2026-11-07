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
