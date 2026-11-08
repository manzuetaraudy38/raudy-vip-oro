from flask import Flask
from flask import jsonify, request
import requests, json, os, re, urllib.parse
from datetime import datetime
app = Flask(__name__)

# ===== TU LINK BROKER PARA QR =====
LINK_BROKER = "https://www.bybit.com/invite?ref=RAUDYORO"
NOMBRE_BROKER_QR = "BYBIT - RAUDY ORO"

# ===== CONFIG M5 - METATRADER 5 =====
M5_CONFIG = {
    "plataforma": "MT5",
    "timeframe": "M5",
    "simbolo": "XAUUSD",
    "activa": True,
    "jefe": "RAUDY ORO"
}

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
M5_ZONA = load("m5_zona.json", {"h": [], "senales": 0, "u": "Nada M5 ZONA aun."})
ZONA_H = load("zona.json", {"h": [], "toques_c": 0, "toques_v": 0, "u": "Nada zona."})

# ===== NUEVO - OPERACIONES DEL ROBOT - NO BORRA NADA VIEJO =====
OPS = load("ops.json", {"h": [], "abiertas": [], "cerradas": [], "auto": True, "ganado": 0, "perdido": 0, "u": "Robot esperando zona..."})
GRAFICO = load("grafico.json", {"velas": []})

PLATS = {
    "CAPITAL": load("cap.json", {"h": [], "u": "Nada Capital.", "c": 0, "b": 0}),
    "T212": load("t212.json", {"h": [], "u": "Nada T212.", "c": 0, "b": 0, "e": 0}),
    "BINANCE": load("bin.json", {"h": [], "u": "Nada Binance.", "c": 0, "b": 0, "e": 0}),
    "ETORO": load("eto.json", {"h": [], "u": "Nada eToro.", "c": 0, "b": 0, "e": 0}),
    "MT5": load("mt5.json", {"h": [], "u": "Nada MT5.", "c": 0, "b": 0, "e": 0}),
    "XTB": load("xtb.json", {"h": [], "u": "Nada XTB.", "c": 0, "b": 0, "e": 0}),
    "COINBASE": load("coin.json", {"h": [], "u": "Nada Coinbase.", "c": 0, "b": 0, "e": 0}),
    "BYBIT": load("bybit.json", {"h": [], "u": "Nada Bybit.", "c": 0, "b": 0, "e": 0})
}

CEREBROS = []
for i in range(1, 101):
    if i <= 15:
        rol = "M5 ZONA - Toca y rebota"
    elif i <= 30:
        rol = "M5 DIVISAS"
    elif i <= 45:
        rol = "M5 BITCOIN"
    elif i <= 60:
        rol = "M5 BINANCE BYBIT"
    elif i <= 70:
        rol = "M5 MT5 - PEGADO"
    elif i <= 80:
        rol = "M5 XTB COINBASE"
    elif i <= 90:
        rol = "M5 APPLE TESLA"
    elif i <= 99:
        rol = "M5 CAPITAL T212"
    else:
        rol = "JEFE RAUDY ORO M5"
    CEREBROS.append({"id": i, "rol": rol, "estado": "VIVO M5", "jefe": "RAUDY ORO", "tf": "M5"})

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

def precio_bybit():
    try:
        r = requests.get("https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT", timeout=4)
        return float(r.json()["result"]["list"][0]["lastPrice"])
    except:
        return yahoo("BTC-USD", 98000)

def todos_precios():
    oro = oro_real()
    btc_b = precio_binance()
    btc_c = precio_coinbase()
    btc_y = precio_bybit()
    d = {
        "ORO": oro, "EURUSD": yahoo("EURUSD=X", 1.1150),
        "GBPUSD": yahoo("GBPUSD=X", 1.2750), "USDJPY": yahoo("USDJPY=X", 149.5),
        "USDCHF": yahoo("USDCHF=X", 0.8850), "AUDUSD": yahoo("AUDUSD=X", 0.6550),
        "BTC": btc_b, "BTC_COINBASE": btc_c, "BTC_BINANCE": btc_b, "BTC_BYBIT": btc_y,
        "ETH": yahoo("ETH-USD", 3400), "AAPL": yahoo("AAPL", 262),
        "TSLA": yahoo("TSLA", 340), "NVDA": yahoo("NVDA", 185),
        "MSFT": yahoo("MSFT", 495), "AMZN": yahoo("AMZN", 235),
        "META": yahoo("META", 645), "GOOGL": yahoo("GOOGL", 282),
        "NFLX": yahoo("NFLX", 765), "AMD": yahoo("AMD", 125)
    }
    return d

# ===== NUEVO - CEREBRO QUE DECIDE Y OPERA SOLO =====
def robot_decide_y_opera(activo, precio, m5_dato):
    # 1. Guarda punto para el grafico
    GRAFICO["velas"].append({"hora": datetime.now().strftime("%H:%M"), "p": precio, "a": activo})
    GRAFICO["velas"] = GRAFICO["velas"][-60:]
    save("grafico.json", GRAFICO)
    # 2. Revisa operaciones abiertas - si toco TP o SL, cierra
    for op in list(OPS["abiertas"]):
        if op["activo"] != activo:
            continue
        gano = False
        perdio = False
        if op["lado"] == "COMPRA":
            if precio >= op["tp"]:
                gano = True
            elif precio <= op["sl"]:
                perdio = True
        else: # VENTA
            if precio <= op["tp"]:
                gano = True
            elif precio >= op["sl"]:
                perdio = True
        if gano or perdio:
            op["cierre"] = precio
            op["hora_cierre"] = datetime.now().strftime("%H:%M")
            op["resultado"] = "GANO +$" + str(op["ganar"]) if gano else "PERDIO -$" + str(op["perder"])
            OPS["abiertas"].remove(op)
            OPS["cerradas"].append(op)
            OPS["h"].append(op)
            if gano:
                OPS["ganado"] += op["ganar"]
            else:
                OPS["perdido"] += op["perder"]
            OPS["u"] = "Robot cerro " + op["lado"] + " " + op["activo"] + " en $" + str(precio) + " - " + op["resultado"]
    # 3. Si AUTO apagado, no abre nuevas
    if not OPS.get("auto", True):
        save("ops.json", OPS)
        return OPS["u"]
    # 4. Si ya hay una abierta de este activo, no abre otra
    for op in OPS["abiertas"]:
        if op["activo"] == activo:
            save("ops.json", OPS)
            return "Robot ya tiene abierta " + activo + " - esperando TP/SL"
    # 5. DECISION - usa tu misma regla M5 ZONA
    accion = m5_dato.get("accion", "ESPERA M5")
    if "COMPRA" in accion:
        lado = "COMPRA"
        tp = m5_dato.get("tp_m5")
        sl = m5_dato.get("sl_m5")
    elif "VENTA" in accion:
        lado = "VENTA"
        tp = m5_dato.get("tp_m5")
        sl = m5_dato.get("sl_m5")
    else:
        save("ops.json", OPS)
        return "Robot M5: ESPERA - " + activo + " $" + str(precio) + " no toco zona, no opera"
    # 6. ABRE OPERACION SOLO
    nueva = {
        "activo": activo, "lado": lado, "entrada": precio,
        "tp": tp, "sl": sl, "lote": 0.01, "ganar": 5, "perder": 2,
        "hora": datetime.now().strftime("%H:%M"), "estado": "ABIERTA",
        "motivo": m5_dato.get("mensaje", "")
    }
    OPS["abiertas"].append(nueva)
    OPS["h"].append(nueva)
    OPS["u"] = "🤖 ROBOT ABRIO SOLO: " + lado + " " + activo + " en $" + str(precio) + " TP $" + str(tp) + " SL $" + str(sl)
    save("ops.json", OPS)
    return OPS["u"]

# ===== PEGADO A M5 - ESTRATEGIA M5 ZONA =====
def m5_zona_analiza(activo, precio):
    z = ZONAS[activo]
    zc = z["c"]
    zv = z["v"]
    rango = zv - zc
    tol = rango * 0.15
    M5["v"].append({"hora": datetime.now().strftime("%H:%M"), "p": precio, "a": activo})
    M5["v"] = M5["v"][-30:]
    velas = [x["p"] for x in M5["v"][-3:] if x["a"] == activo]
    if len(velas) >= 3:
        if velas[-1] > velas[-2] > velas[-3]:
            dir_m5 = "M5 SUBIENDO ⬆️"
        elif velas[-1] < velas[-2] < velas[-3]:
            dir_m5 = "M5 BAJANDO ⬇️"
        else:
            dir_m5 = "M5 LATERAL 🟡"
    else:
        dir_m5 = "M5 ESPERANDO VELAS..."
    if abs(precio - zc) <= tol:
        msg = "🟢 M5 ZONA ABAJO TOCADA - " + NOMBRES[activo] + " $" + str(precio) + " en M5 - COMPRA YA - " + dir_m5
        accion = "COMPRA M5"
        tp = precio + rango * 0.8
        sl = precio - rango * 0.2
        M5_ZONA["senales"] += 1
    elif abs(precio - zv) <= tol:
        msg = "🔴 M5 ZONA ARRIBA TOCADA - " + NOMBRES[activo] + " $" + str(precio) + " en M5 - VENTA YA - " + dir_m5
        accion = "VENTA M5"
        tp = precio - rango * 0.8
        sl = precio + rango * 0.2
        M5_ZONA["senales"] += 1
    else:
        msg = "🟡 M5 ESPERA - " + NOMBRES[activo] + " $" + str(precio) + " - " + dir_m5 + " - Espera que toque ZONA M5"
        accion = "ESPERA M5"
        tp = zc
        sl = zv
    M5_ZONA["u"] = msg
    M5_ZONA["h"].append({"hora": datetime.now().strftime("%H:%M"), "a": activo, "p": precio, "accion": accion, "tf": "M5"})
    M5_ZONA["h"] = M5_ZONA["h"][-20:]
    save("m5_zona.json", M5_ZONA)
    save("m5.json", M5)
    return {"activo": activo, "precio": precio, "tf": "M5", "plataforma": "MT5", "mensaje": msg, "accion": accion, "direccion_m5": dir_m5, "tp_m5": round(tp, 4), "sl_m5": round(sl, 4), "velas_m5": velas}

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

def chat_robot(msg, precios, zonas, m5_dato):
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
        return "Hola jefe RAUDY ORO. 100 cerebros M5 ZONA en vivo. Dime: m5 oro o compro 0.01 en m5 para ganar 5 y perder 2"
    if "m5" in m:
        return "M5 MT5 PEGADO - " + m5_dato.get("mensaje", "") + " | TP M5 " + str(m5_dato.get("tp_m5")) + " SL M5 " + str(m5_dato.get("sl_m5")) + " | " + nombre + " $" + str(precio)
    if "zona" in m:
        return "ZONA " + nombre + ": " + z.get("mensaje", "") + " | TP ZONA " + str(z.get("tp_zona")) + " SL ZONA " + str(z.get("sl_zona"))
    if "bybit" in m:
        return "BYBIT jefe: BTC $" + str(precios["BTC_BYBIT"]) + ". " + PLATS["BYBIT"]["u"]
    if "binance" in m:
        return "BINANCE jefe: BTC $" + str(precios["BTC_BINANCE"]) + ". " + PLATS["BINANCE"]["u"]
    if "mt5" in m:
        return "MT5 M5 PEGADO jefe: ORO $" + str(precios["ORO"]) + " EUR $" + str(precios["EURUSD"]) + " - " + m5_dato.get("mensaje", "")
    if "qr" in m or "broker" in m:
        return "QR JEFE: Escanea para entrar a " + NOMBRE_BROKER_QR + " Link: " + LINK_BROKER
    if "compr" in m:
        if "ganar" in m or "gana" in m or "perder" in m:
            entrada = ZONAS[activo]["c"] if precio > ZONAS[activo]["c"] else precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "COMPRA", activo)
            r = "Jefe M5 PEGADO: COMPRA " + nombre + " " + str(lote) + " en M5 ZONA $" + str(round(entrada, 4)) + " TP " + str(round(tp, 4)) + " ganas $" + str(ganar) + " SL " + str(round(sl, 4)) + " pierdes $" + str(perder) + ". " + m5_dato.get("mensaje", "")
            return r
        return "Dime: compro 0.01 en m5 para ganar 5 y perder 2"
    if "vend" in m:
        if "ganar" in m or "perder" in m:
            entrada = ZONAS[activo]["v"] if precio < ZONAS[activo]["v"] else precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "VENTA", activo)
            r = "Jefe M5 PEGADO: VENTA " + nombre + " " + str(lote) + " en M5 ZONA $" + str(round(tp, 4)) + " ganas $" + str(ganar) + " SL " + str(round(sl, 4)) + " pierdes $" + str(perder)
            return r
        return "VENTA " + nombre + " en ZONA $" + str(ZONAS[activo]["v"])
    if "opera" in m or "robot" in m or "auto" in m:
        return "🤖 ROBOT AUTO: " + OPS["u"] + " | Abiertas: " + str(len(OPS["abiertas"])) + " | Ganado: $" + str(OPS["ganado"]) + " Perdido: $" + str(OPS["perdido"])
    return "Te entendi jefe: " + msg + ". " + nombre + " $" + str(precio) + ". " + m5_dato.get("mensaje", "")

def qr_url():
    return "https://api.qrserver.com/v1/create-qr-code/?size=280x280&data=" + urllib.parse.quote(LINK_BROKER)

H = []
H.append("<!DOCTYPE html><html lang='es'><head>")
H.append("<meta charset='UTF-8'>")
H.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
H.append("<title>RAUDY VIP M5 PEGADO</title>")
H.append("<style>body{background:#050505;color:#fff;font-family:Arial;text-align:center;margin:0}")
H.append("header{background:#FFD700;color:#000;padding:15px}")
H.append(".box{margin:10px;padding:15px;border-radius:15px;border:3px solid #FFD700}")
H.append(".zona{border-color:#00FFFF;background:#001a2a}")
H.append(".qr{border-color:#00FF88;background:#001a00}")
H.append(".m5box{border-color:#FF00FF;background:#1a001a}")
H.append(".m5{border-color:#00FF88}.chat{border-color:#FFD700}.sl{border-color:#FF4444}")
H.append(".vivo{border-color:#00FF88}.bin{border-color:#FFD700}")
H.append("input{width:100%;padding:12px;margin:4px 0;border-radius:10px;background:#111;color:#fff}")
H.append("button{width:100%;padding:14px;border-radius:15px;font-weight:bold;margin-top:5px}")
H.append(".grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px}")
H.append(".robot{background:#1a1a1a;padding:8px;border-radius:12px;font-size:12px}")
H.append(".luz{width:14px;height:14px;border-radius:50%;background:#FF00FF;margin:auto}")
H.append(".barra{width:100%;height:22px;background:#111;border-radius:10px;overflow:hidden}")
H.append(".relleno{height:100%;background:linear-gradient(90deg,#00FF88,#FFD700,#FF4444)}")
H.append("canvas{width:100%;background:#000;border-radius:10px}")
H.append("table{width:100%;font-size:12px;border-collapse:collapse}td,th{border:1px solid #333;padding:5px}")
H.append("</style></head><body>")
H.append("<header><h1>👑 RAUDY VIP M5 PEGADO ⚡</h1>")
H.append("<p>JEFE: RAUDY ORO - MT5 + M5 + ZONA + QR</p>")
H.append("<p id='vivo'>🟢 EN VIVO M5...</p></header>")
# ===== NUEVO - GRAFICO + ROBOT OPERANDO SOLO =====
H.append("<div class='box' style='border-color:#00FF88;background:#001100'><h2>📈 GRAFICO OPERACIONES - ROBOT M5</h2>")
H.append("<canvas id='graf' width='360' height='220'></canvas>")
H.append("<p id='robotEstado' style='font-weight:bold'>🤖 Robot esperando...</p>")
H.append("<p id='robotOps'></p>")
H.append("<button onclick='toggleAuto()' style='background:#00FF88'>🤖 PRENDER / APAGAR ROBOT AUTO</button>")
H.append("<p id='autoEstado'></p></div>")
H.append("<div class='box' style='border-color:#FF4444'><h2>📋 OPERACIONES DEL ROBOT</h2><div id='tablaOps' style='text-align:left'>Cargando operaciones...</div></div>")
H.append("<div class='box m5box'><h2>📊 PEGADO A M5 - MT5 - CADA 5 MINUTOS</h2>")
H.append("<p>Plataforma: MT5 | Timeframe: M5 | Simbolo: XAUUSD ORO</p>")
H.append("<p id='m5Zona' style='font-weight:bold;font-size:16px'>Cargando M5...</p>")
H.append("<p id='m5Dir'></p>")
H.append("<p id='m5TP'></p>")
H.append("<p id='m5Velas' style='font-size:12px'></p></div>")
H.append("<div class='box qr'><h2>📱 ESCANEA MI BROKER - RAUDY ORO</h2>")
H.append("<img id='qrImg' src='" + qr_url() + "' style='width:250px;height:250px;background:#fff;padding:10px;border-radius:15px'>")
H.append("<p style='font-weight:bold'>BYBIT - RAUDY ORO</p>")
H.append("<p style='font-size:12px;word-break:break-all'>" + LINK_BROKER + "</p>")
H.append("<button onclick=\"window.open('" + LINK_BROKER + "','_blank')\" style='background:#00FF88'>🔗 ABRIR MI BROKER</button></div>")
H.append("<div class='box zona'><h2>📊 ESTRATEGIA ZONA M5 - COMO LA FOTO</h2>")
H.append("<p>⬆️ Si toca ZONA ABAJO en M5 - REBOTA ARRIBA = COMPRA</p>")
H.append("<p>⬇️ Si toca ZONA ARRIBA en M5 - REBOTA ABAJO = VENTA</p>")
H.append("<p id='zonaOro' style='font-weight:bold'>Cargando ZONA...</p>")
H.append("<p>ZONA ARRIBA 🔴 VENTA</p>")
H.append("<div class='barra'><div class='relleno' id='barraZona' style='width:50%'></div></div>")
H.append("<p>ZONA ABAJO 🟢 COMPRA</p>")
H.append("<p id='zonaPos'></p><p id='zonaTP'></p></div>")
H.append("<div class='box vivo'><h2>🟢 EN VIVO M5</h2><p id='vivo2'>Conectando M5...</p></div>")
H.append("<div class='box chat'><h2>💬 CHAT M5 + LOTE 0.01</h2>")
H.append("<input id='chat' placeholder='Ej: m5 oro o compro 0.01 en m5 para ganar 5 y perder 2'>")
H.append("<button onclick='enviarChat()' style='background:#FFD700'>💬 ENVIAR</button>")
H.append("<p id='chatR' style='background:#111;padding:12px;border-radius:10px;text-align:left'>🤖 Hola jefe M5...</p>")
H.append("<button onclick=\"ej('m5 oro)')\" style='background:#FF00FF;color:#fff'>📊 M5 ORO PEGADO</button>")
H.append("<button onclick=\"ej('m5 bitcoin)')\" style='background:#FFA500'>📊 M5 BITCOIN</button>")
H.append("<button onclick=\"ej('compro 0.01 en m5 para ganar 5 y perder 2)')\" style='background:#00FF88'>✅ COMPRA M5 0.01</button>")
H.append("<button onclick=\"ej('zona oro)')\" style='background:#00FFFF'>📊 zona oro</button>")
H.append("<button onclick=\"ej('bybit)')\" style='background:#FFD700'>🟡 BYBIT</button>")
H.append("<button onclick=\"ej('qr)')\" style='background:#00FF88'>📱 MI QR BROKER</button></div>")
H.append("<div class='box'><h2>💶 DIVISAS M5 EN VIVO</h2><p id='divisas'></p></div>")
H.append("<div class='box'><h2>₿ BITCOIN M5 EN VIVO</h2><p id='crypto'></p></div>")
H.append("<div class='box'><h2>📈 ACCIONES M5 EN VIVO</h2><p id='acciones'></p></div>")
H.append("<div class='box'><h2>🏦 8 PLATAFORMAS M5 EN VIVO</h2><p id='plats'></p></div>")
H.append("<div class='box sl'><h2>🛑 CALCULADORA M5 LOTE 0.01</h2>")
H.append("<select id='selAct'><option value='ORO'>ORO M5</option><option value='BTC'>BITCOIN M5</option><option value='EURUSD'>EUR/USD M5</option><option value='AAPL'>APPLE M5</option><option value='TSLA'>TESLA M5</option></select>")
H.append("<input id='lote' type='number' value='0.01' step='0.01'>")
H.append("<input id='ganar' type='number' value='5'>")
H.append("<input id='perder' type='number' value='2'>")
H.append("<input id='entrada' type='number' value='3910'>")
H.append("<button onclick='calcLote()' style='background:#FF4444;color:#fff'>🛑 CALCULAR TP SL M5</button>")
H.append("<p id='loteR' style='background:#111;padding:12px;border-radius:10px'></p></div>")
H.append("<div class='box'><h2>👑 JEFE 100 M5 - RAUDY ORO</h2><p id='j1'></p><p id='j2'></p></div>")
H.append("<h2>🧠 LOS 100 CEREBROS M5 PEGADOS</h2>")
H.append("<div class='grid' id='grid'></div>")
H.append("<p>RAUDY VIP M5 2026 - WhatsApp 0767574050</p>")
H.append("<script>")
H.append("let g=document.getElementById('grid');")
H.append("for(let i=1;i<=100;i++){let d=document.createElement('div');")
H.append("d.className='robot';")
H.append("let rol='M5 ZONA';")
H.append("if(i>15 && i<=30) rol='M5 DIVISAS';")
H.append("if(i>30 && i<=45) rol='M5 BITCOIN';")
H.append("if(i>45 && i<=60) rol='M5 BINANCE BYBIT';")
H.append("if(i>60 && i<=70) rol='M5 MT5 PEGADO';")
H.append("if(i>70 && i<=80) rol='M5 XTB COINBASE';")
H.append("if(i>80 && i<=90) rol='M5 APPLE TESLA';")
H.append("if(i>90 && i<100) rol='M5 CAPITAL T212';")
H.append("if(i==100) rol='JEFE RAUDY ORO M5';")
H.append("d.innerHTML='<div class=luz></div><b>Cerebro '+i+' M5</b><br>'+rol+'<br><span id=m'+i+'>VIVO M5</span>';")
H.append("g.appendChild(d)}")
H.append("function hablar(t){try{let u=new SpeechSynthesisUtterance(t);u.lang='es-ES';speechSynthesis.speak(u)}catch(e){}}")
H.append("async function enviarChat(){let t=document.getElementById('chat').value;")
H.append("if(!t){document.getElementById('chatR').innerHTML='Escribe algo jefe';return}")
H.append("document.getElementById('chatR').innerHTML='🤖 Pensando M5...';")
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
# ===== NUEVO JS - DIBUJA GRAFICO + MUESTRA OPERACIONES =====
H.append("async function toggleAuto(){let r=await fetch('/api/robot_auto');let d=await r.json();document.getElementById('autoEstado').innerHTML='Robot AUTO: '+(d.auto?'🟢 PRENDIDO - opera solo':'🔴 APAGADO - solo mira');hablar('Robot '+(d.auto?'prendido':'apagado'))}")
H.append("function dibujaGrafico(velas,ops){let c=document.getElementById('graf');if(!c||!velas||velas.length<2)return;let x=c.getContext('2d');x.clearRect(0,0,360,220);let precios=velas.map(v=>v.p);let mn=Math.min(...precios)-5;let mx=Math.max(...precios)+5;")
H.append("x.strokeStyle='#FFD700';x.beginPath();velas.forEach((v,i)=>{let px=i/(velas.length-1)*340+10;let py=210-(v.p-mn)/(mx-mn)*190;if(i==0)x.moveTo(px,py);else x.lineTo(px,py)});x.stroke();")
H.append("x.fillStyle='#00FF88';x.fillText('COMPRA ZONA 3910',10,210);x.fillStyle='#FF4444';x.fillText('VENTA ZONA 3970',10,20);")
H.append("if(ops)ops.forEach(o=>{let py=210-(o.entrada-mn)/(mx-mn)*190;x.fillStyle=o.lado=='COMPRA'?'#00FF88':'#FF4444';x.beginPath();x.arc(340,py,7,0,7);x.fill();x.fillText(o.lado+' $'+o.entrada,200,py)});}")
H.append("async function up(){try{")
H.append("let r=await fetch('/api/satelite_usa?v='+Date.now());let d=await r.json();")
H.append("document.getElementById('vivo').innerHTML='🟢 EN VIVO M5 '+d.hora+' - ORO $'+d.ORO+' BTC $'+d.BTC;")
H.append("document.getElementById('vivo2').innerHTML='ORO $'+d.ORO+' BTC $'+d.BTC+' EUR $'+d.EURUSD+' M5 PEGADO';")
H.append("document.getElementById('m5Zona').innerHTML=d.m5.mensaje;")
H.append("document.getElementById('m5Dir').innerHTML=d.m5.direccion_m5+' | MT5 M5 | Señales M5: '+d.m5_senales;")
H.append("document.getElementById('m5TP').innerHTML='TP M5 $'+d.m5.tp_m5+' SL M5 $'+d.m5.sl_m5+' - Accion: '+d.m5.accion;")
H.append("document.getElementById('m5Velas').innerHTML='Velas M5: '+JSON.stringify(d.m5.velas_m5);")
H.append("if(d.robot){document.getElementById('robotEstado').innerHTML=d.robot.mensaje;document.getElementById('robotOps').innerHTML='Abiertas: '+d.robot.abiertas.length+' | Cerradas: '+d.robot.cerradas.length+' | Ganado $'+d.robot.ganado+' | Perdido $'+d.robot.perdido+' | AUTO: '+(d.robot.auto?'🟢 ON':'🔴 OFF');")
H.append("let html='<table><tr><th>Hora</th><th>Activo</th><th>Lado</th><th>Entrada</th><th>TP</th><th>SL</th><th>Resultado</th></tr>';")
H.append("d.robot.abiertas.forEach(o=>{html+='<tr><td>'+o.hora+'</td><td>'+o.activo+'</td><td>'+o.lado+'</td><td>'+o.entrada+'</td><td>'+o.tp+'</td><td>'+o.sl+'</td><td>🟢 ABIERTA</td></tr>'});")
H.append("d.robot.cerradas.slice(-5).forEach(o=>{html+='<tr><td>'+o.hora+'</td><td>'+o.activo+'</td><td>'+o.lado+'</td><td>'+o.entrada+'</td><td>'+o.tp+'</td><td>'+o.sl+'</td><td>'+(o.resultado||'')+'</td></tr>'});")
H.append("html+='</table>';document.getElementById('tablaOps').innerHTML=html;")
H.append("dibujaGrafico(d.grafico_velas,d.robot.abiertas);}")
H.append("let z=d.zonas.ORO;")
H.append("document.getElementById('zonaOro').innerHTML=z.mensaje;")
H.append("document.getElementById('barraZona').style.width=z.posicion+'%';")
H.append("document.getElementById('zonaPos').innerHTML='Posicion ZONA M5: '+z.posicion+'% - Abajo $'+z.zona_abajo+' Arriba $'+z.zona_arriba;")
H.append("document.getElementById('zonaTP').innerHTML='TP ZONA $'+z.tp_zona+' SL ZONA $'+z.sl_zona;")
H.append("document.getElementById('divisas').innerHTML='EUR $'+d.EURUSD+' '+d.zonas.EURUSD.accion+' | GBP $'+d.GBPUSD+' '+d.zonas.GBPUSD.accion+' | JPY $'+d.USDJPY+' '+d.zonas.USDJPY.accion;")
H.append("document.getElementById('crypto').innerHTML='BTC $'+d.BTC+' '+d.zonas.BTC.mensaje+' | ETH $'+d.ETH+' '+d.zonas.ETH.accion;")
H.append("document.getElementById('acciones').innerHTML='APPLE $'+d.AAPL+' '+d.zonas.AAPL.accion+' | TESLA $'+d.TSLA+' '+d.zonas.TSLA.accion+' | NVDA $'+d.NVDA+' '+d.zonas.NVDA.accion;")
H.append("document.getElementById('plats').innerHTML='MT5 M5 ORO $'+d.ORO+' | BYBIT BTC $'+d.BTC_BYBIT+' | BINANCE BTC $'+d.BTC_BINANCE+' | COINBASE BTC $'+d.BTC_COINBASE;")
H.append("document.getElementById('j1').innerHTML=d.jefe.orden;")
H.append("document.getElementById('j2').innerHTML=d.jefe.mensaje;")
H.append("for(let i=1;i<=100;i++){let el=document.getElementById('m'+i);")
H.append("if(el)el.innerHTML='M5 VIVO $'+d.ORO+' - '+d.jefe.orden}")
H.append("}catch(e){}}")
H.append("setInterval(up,5000);up();")
H.append("</script></body></html>")
HTML = "".join(H)

@app.route("/")
def home():
    return HTML

@app.route("/api/qr")
def api_qr():
    return jsonify({"link": LINK_BROKER, "nombre": NOMBRE_BROKER_QR, "qr_url": qr_url()})

@app.route("/api/m5")
def api_m5():
    precios = todos_precios()
    activo = request.args.get("activo", "ORO")
    if activo not in ZONAS:
        activo = "ORO"
    m5 = m5_zona
