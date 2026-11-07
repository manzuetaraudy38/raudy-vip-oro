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

MEM = load("mem.json", {"h": [], "c": 0, "v": 0, "e": 0, "l": "Nada aun jefe."})
M5 = load("m5.json", {"v": [], "u": "Nada M5 aun.", "s": 0, "b": 0})
ZONA_H = load("zona.json", {"h": [], "toques_c": 0, "toques_v": 0, "u": "Nada zona."})
PLATS = {
    "CAPITAL": load("cap.json", {"h": [], "u": "Nada Capital.", "c": 0, "b": 0}),
    "T212": load("t212.json", {"h": [], "u": "Nada T212.", "c": 0, "b": 0, "e": 0}),
    "BINANCE": load("bin.json", {"h": [], "u": "Nada Binance.", "c": 0, "b": 0, "e": 0}),
    "ETORO": load("eto.json", {"h": [], "u": "Nada eToro.", "c": 0, "b": 0, "e": 0}),
    "MT5": load("mt5.json", {"h": [], "u": "Nada MT5.", "c": 0, "b": 0, "e": 0}),
    "XTB": load("xtb.json", {"h": [], "u": "Nada XTB.", "c": 0, "b": 0, "e": 0}),
    "COINBASE": load("coin.json", {"h": [], "u": "Nada Coinbase.", "c": 0, "b": 0, "e": 0})
}
CEREBROS = []
for i in range(1, 101):
    if i <= 15:
        rol = "ZONA - Toca y rebota"
    elif i <= 30:
        rol = "DIVISAS ZONA"
    elif i <= 45:
        rol = "BITCOIN ZONA"
    elif i <= 60:
        rol = "BINANCE"
    elif i <= 70:
        rol = "eTORO MT5"
    elif i <= 80:
        rol = "XTB COINBASE"
    elif i <= 90:
        rol = "APPLE TESLA ZONA"
    elif i <= 99:
        rol = "CAPITAL T212 ZONA"
    else:
        rol = "JEFE RAUDY ORO"
    CEREBROS.append({"id": i, "rol": rol, "estado": "VIVO", "jefe": "RAUDY ORO"})
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
    "ORO": "ORO 🥇", "EURUSD": "EUR/USD 💶", "GBPUSD": "GBP/USD 💷",
    "USDJPY": "USD/JPY 💴", "USDCHF": "USD/CHF 🇨🇭", "AUDUSD": "AUD/USD 🦘",
    "BTC": "BITCOIN ₿", "ETH": "ETHEREUM Ξ", "AAPL": "APPLE 🍎",
    "TSLA": "TESLA 🚗", "NVDA": "NVIDIA 💚", "MSFT": "MICROSOFT 🪟",
    "AMZN": "AMAZON 📦", "META": "META 👍", "GOOGL": "GOOGLE 🔍",
    "NFLX": "NETFLIX 🎬", "AMD": "AMD 🔴"
}
def yahoo(s, fb):
    try:
        u = "https://query1.finance.yahoo.com/v8/finance/chart/" + s
        r = requests.get(u, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        j = r.json()
        v = j["chart"]["result"][0]["meta"]
        return float(v["regularMarketPrice"])
    except:
        return fb
def oro_real():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=4)
        return float(r.json().get("price", 4088))
    except:
        return yahoo("GC=F", 4088)
def precio_binance():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=4)
        return float(r.json().get("price", 98000))
    except:
        return yahoo("BTC-USD", 98000)
def precio_coinbase():
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=4)
        return float(r.json()["data"]["amount"])
    except:
        return yahoo("BTC-USD", 98000)
def todos_precios():
    oro = oro_real()
    btc_b = precio_binance()
    btc_c = precio_coinbase()
    d = {
        "ORO": oro, "EURUSD": yahoo("EURUSD=X", 1.1150),
        "GBPUSD": yahoo("GBPUSD=X", 1.2750), "USDJPY": yahoo("USDJPY=X", 149.5),
        "USDCHF": yahoo("USDCHF=X", 0.8850), "AUDUSD": yahoo("AUDUSD=X", 0.6550),
        "BTC": btc_b, "BTC_COINBASE": btc_c, "BTC_BINANCE": btc_b,
        "ETH": yahoo("ETH-USD", 3400), "AAPL": yahoo("AAPL", 262),
        "TSLA": yahoo("TSLA", 340), "NVDA": yahoo("NVDA", 185),
        "MSFT": yahoo("MSFT", 495), "AMZN": yahoo("AMZN", 235),
        "META": yahoo("META", 645), "GOOGL": yahoo("GOOGL", 282),
        "NFLX": yahoo("NFLX", 765), "AMD": yahoo("AMD", 125)
    }
    return d
def zona_analiza(activo, precio, precios):
    z = ZONAS[activo]
    zc = z["c"]
    zv = z["v"]
    rango = zv - zc
    tol = rango * 0.15
    pos = (precio - zc) / rango * 100 if rango != 0 else 50
    if pos < 0:
        pos = 0
    if pos > 100:
        pos = 100
    if abs(precio - zc) <= tol:
        ZONA_H["toques_c"] += 1
        msg = "🟢 ZONA ABAJO TOCADA - COMO LA FOTO - " + NOMBRES[activo] + " toco ZONA $" + str(zc) + " REBOTE PARA ARRIBA - COMPRA YA"
        tipo = "ZONA_COMPRA"
        accion = "COMPRA"
        tp = precio + rango * 0.8
        sl = precio - rango * 0.2
    elif abs(precio - zv) <= tol:
        ZONA_H["toques_v"] += 1
        msg = "🔴 ZONA ARRIBA TOCADA - COMO LA FOTO - " + NOMBRES[activo] + " toco ZONA $" + str(zv) + " REBOTE PARA ABAJO - VENTA YA"
        tipo = "ZONA_VENTA"
        accion = "VENTA"
        tp = precio - rango * 0.8
        sl = precio + rango * 0.2
    elif precio < zc:
        msg = "🔴 " + NOMBRES[activo] + " ABAJO DE ZONA $" + str(precio) + " - Espera que vuelva a ZONA para COMPRAR"
        tipo = "DEBAJO_ZONA"
        accion = "ESPERA_BARREDOR"
        tp = zc + rango * 0.8
        sl = zc - rango * 0.2
    elif precio > zv:
        msg = "🔴 " + NOMBRES[activo] + " ARRIBA DE ZONA $" + str(precio) + " - Espera que vuelva a ZONA para VENDER"
        tipo = "ENCIMA_ZONA"
        accion = "ESPERA"
        tp = zv - rango * 0.8
        sl = zv + rango * 0.2
    else:
        msg = "🟡 " + NOMBRES[activo] + " en MEDIO DE ZONA $" + str(precio) + " - ESPERA que toque ZONA"
        tipo = "MEDIO"
        accion = "ESPERA"
        tp = zc
        sl = zv
    ZONA_H["u"] = msg
    ZONA_H["h"].append({"hora": datetime.now().strftime("%H:%M"), "a": activo, "p": precio, "t": tipo})
    ZONA_H["h"] = ZONA_H["h"][-20:]
    save("zona.json", ZONA_H)
    return {"activo": activo, "precio": precio, "zona_abajo": zc, "zona_arriba": zv, "posicion": round(pos, 1), "mensaje": msg, "tipo": tipo, "accion": accion, "tp_zona": round(tp, 4), "sl_zona": round(sl, 4)}
def zona_todos(precios):
    out = {}
    for a in ZONAS:
        if a in precios:
            out[a] = zona_analiza(a, precios[a], precios)
    return out
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
        MEM["l"] = "ORO bajo a " + str(oro) + ". Despues SUBIO."
    elif oro >= 3970:
        MEM["l"] = "ORO subio a " + str(oro) + ". Despues BAJO."
    else:
        MEM["l"] = "ORO en " + str(oro) + ". Me acuerdo jefe."
    MEM["h"].append({"hora": datetime.now().strftime("%H:%M"), "oro": oro, "d": dec})
    MEM["h"] = MEM["h"][-20:]
    save("mem.json", MEM)
def m5_aprende(p):
    M5["v"].append({"hora": datetime.now().strftime("%H:%M"), "p": p})
    M5["v"] = M5["v"][-20:]
    if len(M5["v"]) >= 3:
        a = M5["v"][-3]["p"]
        b = M5["v"][-2]["p"]
        c = M5["v"][-1]["p"]
        if c > b > a:
            M5["s"] += 1
            M5["b"] = 0
            M5["u"] = "M5 subio 3 velas " + str(a) + ">" + str(b) + ">" + str(c)
        elif c < b < a:
            M5["b"] += 1
            M5["s"] = 0
            M5["u"] = "M5 bajo 3 velas " + str(a) + ">" + str(b) + ">" + str(c)
        else:
            M5["u"] = "M5 en " + str(c) + " mezclado. ESPERA."
    save("m5.json", M5)
def plat_aprende(key, pc, pr, nombre, archivo):
    D = PLATS[key]
    if pc > 10000:
        if pc <= 95000:
            D["b"] += 1
            lec = nombre + " BARATO BTC $" + str(pc)
        elif pc >= 108000:
            D["c"] += 1
            lec = nombre + " CARO BTC $" + str(pc)
        else:
            lec = nombre + " MEDIO BTC $" + str(pc)
    else:
        if pc >= 3970:
            D["c"] += 1
            lec = nombre + " CARO ORO $" + str(pc)
        elif pc <= 3910:
            D["b"] += 1
            lec = nombre + " BARATO ORO $" + str(pc)
        else:
            lec = nombre + " MEDIO ORO $" + str(pc)
    D["u"] = lec
    D["h"].append({"hora": datetime.now().strftime("%H:%M"), "p": pc})
    D["h"] = D["h"][-20:]
    save(archivo, D)
    return lec
def calc_lote(lote, ganar, perder, precio, lado, activo):
    div = lote * 100
    if activo in ["EURUSD", "GBPUSD", "AUDUSD"]:
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
def chat_robot(msg, precios, zonas):
    m = msg.lower()
    nums = re.findall(r"\d+\.?\d*", msg)
    activo = busca_activo(m)
    precio = precios.get(activo, 4088)
    nombre = NOMBRES.get(activo, activo)
    z = zonas.get(activo, {})
    lote = 0.01
    ganar = 5.0
    perder = 2.0
    if "0.02" in msg:
        lote = 0.02
    if "0.05" in msg:
        lote = 0.05
    if "0.1" in msg:
        lote = 0.1
    if "ganar" in m and len(nums) >= 2:
        try:
            ganar = float(nums[-2])
            perder = float(nums[-1])
        except:
            pass
    if "hola" in m:
        return "Hola jefe RA
