from flask import Flask
from flask import jsonify, request
import requests, json, os, re, urllib.parse, time
from datetime import datetime
app = Flask(__name__)

LINK_BROKER = "https://www.bybit.com/invite?ref=RAUDYORO"
NOMBRE_BROKER_QR = "BYBIT - RAUDY ORO"
M5_CONFIG = {"plataforma": "MT5", "timeframe": "M5", "simbolo": "XAUUSD", "activa": True, "jefe": "RAUDY ORO"}

# ===== ARREGLO NO PRENDE - CACHE 30 SEGUNDOS =====
_CACHE = {"tiempo": 0, "datos": None}
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
    if i <= 15: rol = "M5 ZONA - Toca y rebota"
    elif i <= 30: rol = "M5 DIVISAS"
    elif i <= 45: rol = "M5 BITCOIN"
    elif i <= 60: rol = "M5 BINANCE BYBIT"
    elif i <= 70: rol = "M5 MT5 - PEGADO"
    elif i <= 80: rol = "M5 XTB COINBASE"
    elif i <= 90: rol = "M5 APPLE TESLA"
    elif i <= 99: rol = "M5 CAPITAL T212"
    else: rol = "JEFE RAUDY ORO M5"
    CEREBROS.append({"id": i, "rol": rol, "estado": "VIVO M5", "jefe": "RAUDY ORO", "tf": "M5"})
ZONAS = {"ORO": {"c": 3910, "v": 3970},"EURUSD": {"c": 1.1150, "v": 1.1250},"GBPUSD": {"c": 1.2700, "v": 1.2850},"USDJPY": {"c": 148.00, "v": 151.00},"USDCHF": {"c": 0.8800, "v": 0.8950},"AUDUSD": {"c": 0.6500, "v": 0.6650},"BTC": {"c": 95000, "v": 108000},"ETH": {"c": 3200, "v": 3800},"AAPL": {"c": 255, "v": 270},"TSLA": {"c": 330, "v": 355},"NVDA": {"c": 180, "v": 195},"MSFT": {"c": 490, "v": 505},"AMZN": {"c": 230, "v": 245},"META": {"c": 640, "v": 660},"GOOGL": {"c": 280, "v": 292},"NFLX": {"c": 750, "v": 790},"AMD": {"c": 120, "v": 135}}
NOMBRES = {"ORO": "ORO 🥇", "EURUSD": "EUR/USD 💶", "GBPUSD": "GBP/USD 💷","USDJPY": "USD/JPY 💴", "USDCHF": "USD/CHF 🇨🇭", "AUDUSD": "AUD/USD 🦘","BTC": "BITCOIN ₿", "ETH": "ETHEREUM Ξ", "AAPL": "APPLE 🍎","TSLA": "TESLA 🚗", "NVDA": "NVIDIA 💚", "MSFT": "MICROSOFT 🪟","AMZN": "AMAZON 📦", "META": "META 👍", "GOOGL": "GOOGLE 🔍","NFLX": "NETFLIX 🎬", "AMD": "AMD 🔴"}

def yahoo(s, fb):
    try:
        u = "https://query1.finance.yahoo.com/v8/finance/chart/" + s
        r = requests.get(u, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        j = r.json()
        v = j["chart"]["result"][0]["meta"]
        return float(v["regularMarketPrice"])
    except:
        return fb
def oro_real():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=3)
        return float(r.json().get("price", 4088))
    except:
        return yahoo("GC=F", 4088)
def precio_binance():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=3)
        return float(r.json().get("price", 98000))
    except:
        return yahoo("BTC-USD", 98000)
def precio_coinbase():
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=3)
        return float(r.json()["data"]["amount"])
    except:
        return yahoo("BTC-USD", 98000)
def precio_bybit():
    try:
        r = requests.get("https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT", timeout=3)
        return float(r.json()["result"]["list"][0]["lastPrice"])
    except:
        return yahoo("BTC-USD", 98000)

def todos_precios():
    global _CACHE
    ahora = time.time()
    # Si ya buscamos hace menos de 30 seg, usa lo mismo, no busques otra vez
    if _CACHE["datos"] is not None and (ahora - _CACHE["tiempo"] < 30):
        return _CACHE["datos"]
    try:
        oro = oro_real()
        btc_b = precio_binance()
        btc_c = precio_coinbase()
        btc_y = precio_bybit()
        d = {"ORO": oro, "EURUSD": yahoo("EURUSD=X", 1.1150),"GBPUSD": yahoo("GBPUSD=X", 1.2750), "USDJPY": yahoo("USDJPY=X", 149.5),"USDCHF": yahoo("USDCHF=X", 0.8850), "AUDUSD": yahoo("AUDUSD=X", 0.6550),"BTC": btc_b, "BTC_COINBASE": btc_c, "BTC_BINANCE": btc_b, "BTC_BYBIT": btc_y,"ETH": yahoo("ETH-USD", 3400), "AAPL": yahoo("AAPL", 262),"TSLA": yahoo("TSLA", 340), "NVDA": yahoo("NVDA", 185),"MSFT": yahoo("MSFT", 495), "AMZN": yahoo("AMZN", 235),"META": yahoo("META", 645), "GOOGL": yahoo("GOOGL", 282),"NFLX": yahoo("NFLX", 765), "AMD": yahoo("AMD", 125)}
    except Exception as e:
        d = {"ORO": 4070, "EURUSD": 1.1140, "GBPUSD": 1.2750, "USDJPY": 149.5, "USDCHF": 0.8850, "AUDUSD": 0.6550, "BTC": 98000, "BTC_COINBASE": 98000, "BTC_BINANCE": 98000, "BTC_BYBIT": 98000, "ETH": 3400, "AAPL": 262, "TSLA": 340, "NVDA": 185, "MSFT": 495, "AMZN": 235, "META": 645, "GOOGL": 282, "NFLX": 765, "AMD": 125}
    _CACHE = {"tiempo": ahora, "datos": d}
    return d

def robot_decide_y_opera(activo, precio, m5_dato):
    try:
        GRAFICO["velas"].append({"hora": datetime.now().strftime("%H:%M"), "p": precio, "a": activo})
        GRAFICO["velas"] = GRAFICO["velas"][-60:]
        for op in list(OPS["abiertas"]):
            if op["activo"] != activo: continue
            gano = False; perdio = False
            if op["lado"] == "COMPRA":
                if precio >= op["tp"]: gano = True
                elif precio <= op["sl"]: perdio = True
            else:
                if precio <= op["tp"]: gano = True
                elif precio >= op["sl"]: perdio = True
            if gano or perdio:
                op["cierre"] = precio; op["hora_cierre"] = datetime.now().strftime("%H:%M")
                op["resultado"] = "GANO +$" + str(op["ganar"]) if gano else "PERDIO -$" + str(op["perder"])
                OPS["abiertas"].remove(op); OPS["cerradas"].append(op); OPS["h"].append(op)
                if gano: OPS["ganado"] += op["ganar"]
                else: OPS["perdido"] += op["perder"]
                OPS["u"] = "Robot cerro " + op["lado"] + " " + op["activo"] + " en $" + str(precio) + " - " + op["resultado"]
        if not OPS.get("auto", True):
            save("ops.json", OPS); return OPS["u"]
        for op in OPS["abiertas"]:
            if op["activo"] == activo:
                save("ops.json", OPS); return "Robot ya tiene abierta " + activo + " - esperando TP/SL"
        accion = m5_dato.get("accion", "ESPERA M5")
        if "COMPRA" in accion: lado = "COMPRA"; tp = m5_dato.get("tp_m5"); sl = m5_dato.get("sl_m5")
        elif "VENTA" in accion: lado = "VENTA"; tp = m5_dato.get("tp_m5"); sl = m5_dato.get("sl_m5")
        else:
            save("ops.json", OPS); return "Robot M5: ESPERA - " + activo + " $" + str(precio) + " no toco zona, no opera"
        nueva = {"activo": activo, "lado": lado, "entrada": precio, "tp": tp, "sl": sl, "lote": 0.01, "ganar": 5, "perder": 2, "hora": datetime.now().strftime("%H:%M"), "estado": "ABIERTA", "motivo": m5_dato.get("mensaje", "")}
        OPS["abiertas"].append(nueva); OPS["h"].append(nueva)
        OPS["u"] = "🤖 ROBOT ABRIO SOLO: " + lado + " " + activo + " en $" + str(precio) + " TP $" + str(tp) + " SL $" + str(sl)
        save("ops.json", OPS); save("grafico.json", GRAFICO)
        return OPS["u"]
    except Exception as e:
        return "Robot error: " + str(e)

def m5_zona_analiza(activo, precio):
    z = ZONAS[activo]; zc = z["c"]; zv = z["v"]; rango = zv - zc; tol = rango * 0.15
    M5["v"].append({"hora": datetime.now().strftime("%H:%M"), "p": precio, "a": activo}); M5["v"] = M5["v"][-30:]
    velas = [x["p"] for x in M5["v"][-3:] if x["a"] == activo]
    if len(velas) >= 3:
        if velas[-1] > velas[-2] > velas[-3]: dir_m5 = "M5 SUBIENDO ⬆️"
        elif velas[-1] < velas[-2] < velas[-3]: dir_m5 = "M5 BAJANDO ⬇️"
        else: dir_m5 = "M5 LATERAL 🟡"
    else: dir_m5 = "M5 ESPERANDO VELAS..."
    if abs(precio - zc) <= tol:
        msg = "🟢 M5 ZONA ABAJO TOCADA - " + NOMBRES[activo] + " $" + str(precio) + " en M5 - COMPRA YA - " + dir_m5; accion = "COMPRA M5"; tp = precio + rango * 0.8; sl = precio - rango * 0.2; M5_ZONA["senales"] += 1
    elif abs(precio - zv) <= tol:
        msg = "🔴 M5 ZONA ARRIBA TOCADA - " + NOMBRES[activo] + " $" + str(precio) + " en M5 - VENTA YA - " + dir_m5; accion = "VENTA M5"; tp = precio - rango * 0.8; sl = precio + rango * 0.2; M5_ZONA["senales"] += 1
    else:
        msg = "🟡 M5 ESPERA - " + NOMBRES[activo] + " $" + str(precio) + " - " + dir_m5 + " - Espera que toque ZONA M5"; accion = "ESPERA M5"; tp = zc; sl = zv
    M5_ZONA["u"] = msg; M5_ZONA["h"].append({"hora": datetime.now().strftime("%H:%M"), "a": activo, "p": precio, "accion": accion, "tf": "M5"}); M5_ZONA["h"] = M5_ZONA["h"][-20:]
    save("m5_zona.json", M5_ZONA); save("m5.json", M5)
    return {"activo": activo, "precio": precio, "tf": "M5", "plataforma": "MT5", "mensaje": msg, "accion": accion, "direccion_m5": dir_m5, "tp_m5": round(tp, 4), "sl_m5": round(sl, 4), "velas_m5": velas}

def zona_analiza(activo, precio, precios):
    z = ZONAS[activo]; zc = z["c"]; zv = z["v"]; rango = zv - zc; tol = rango * 0.15
    pos = (precio - zc) / rango * 100 if rango != 0 else 50
    if pos < 0: pos = 0
    if pos > 100: pos = 100
    if abs(precio - zc) <= tol:
        ZONA_H["toques_c"] += 1; msg = "🟢 ZONA ABAJO TOCADA - " + NOMBRES[activo] + " toco ZONA $" + str(zc) + " REBOTE PARA ARRIBA - COMPRA YA"; tipo = "ZONA_COMPRA"; accion = "COMPRA"; tp = precio + rango * 0.8; sl = precio - rango * 0.2
    elif abs(precio - zv) <= tol:
        ZONA_H["toques_v"] += 1; msg = "🔴 ZONA ARRIBA TOCADA - " + NOMBRES[activo] + " toco ZONA $" + str(zv) + " REBOTE PARA ABAJO - VENTA YA"; tipo = "ZONA_VENTA"; accion = "VENTA"; tp = precio - rango * 0.8; sl = precio + rango * 0.2
    elif precio < zc:
        msg = "🔴 " + NOMBRES[activo] + " ABAJO DE ZONA $" + str(precio) + " - Espera que vuelva a ZONA para COMPRAR"; tipo = "DEBAJO_ZONA"; accion = "ESPERA_BARREDOR"; tp = zc + rango * 0.8; sl = zc - rango * 0.2
    elif precio > zv:
        msg = "🔴 " + NOMBRES[activo] + " ARRIBA DE ZONA $" + str(precio) + " - Espera que vuelva a ZONA para VENDER"; tipo = "ENCIMA_ZONA"; accion = "ESPERA"; tp = zv - rango * 0.8; sl = zv + rango * 0.2
    else:
        msg = "🟡 " + NOMBRES[activo] + " en MEDIO DE ZONA $" + str(precio) + " - ESPERA que toque ZONA"; tipo = "MEDIO"; accion = "ESPERA"; tp = zc; sl = zv
    ZONA_H["u"] = msg; ZONA_H["h"].append({"hora": datetime.now().strftime("%H:%M"), "a": activo, "p": precio, "t": tipo}); ZONA_H["h"] = ZONA_H["h"][-20:]; save("zona.json", ZONA_H)
    return {"activo": activo, "precio": precio, "zona_abajo": zc, "zona_arriba": zv, "posicion": round(pos, 1), "mensaje": msg, "tipo": tipo, "accion": accion, "tp_zona": round(tp, 4), "sl_zona": round(sl, 4)}
def zona_todos(precios):
    out = {}
    for a in ZONAS:
        if a in precios: out[a] = zona_analiza(a, precios[a], precios)
    return out
def aprende(oro, orden):
    if "COMPRA" in orden or oro <= 3910: MEM["c"] += 1; dec = "COMPRA"
    elif "VENTA" in orden or oro >= 3970: MEM["v"] += 1; dec = "VENTA"
    else: MEM["e"] += 1; dec = "ESPERA"
    if oro <= 3910: MEM["l"] = "ORO bajo a " + str(oro) + ". Despues SUBIO."
    elif oro >= 3970: MEM["l"] = "ORO subio a " + str(oro) + ". Despues BAJO."
    else: MEM["l"] = "ORO en " + str(oro) + ". Me acuerdo jefe."
    MEM["h"].append({"hora": datetime.now().strftime("%H:%M"), "oro": oro, "d": dec}); MEM["h"] = MEM["h"][-20:]; save("mem.json", MEM)
def m5_aprende(p):
    M5["v"].append({"hora": datetime.now().strftime("%H:%M"), "p": p}); M5["v"] = M5["v"][-20:]
    if len(M5["v"]) >= 3:
        a = M5["v"][-3]["p"]; b = M5["v"][-2]["p"]; c = M5["v"][-1]["p"]
        if c > b > a: M5["s"] += 1; M5["b"] = 0; M5["u"] = "M5 subio 3 velas " + str(a) + ">" + str(b) + ">" + str(c)
        elif c < b < a: M5["b"] += 1; M5["s"] = 0; M5["u"] = "M5 bajo 3 velas " + str(a) + ">" + str(b) + ">" + str(c)
        else: M5["u"] = "M5 en " + str(c) + " mezclado. ESPERA."
    save("m5.json", M5)
def plat_aprende(key, pc, pr, nombre, archivo):
    D = PLATS[key]
    if pc > 10000:
        if pc <= 95000: D["b"] += 1; lec = nombre + " BARATO BTC $" + str(pc)
        elif pc >= 108000: D["c"] += 1; lec = nombre + " CARO BTC $" + str(pc)
        else: lec = nombre + " MEDIO BTC $" + str(pc)
    else:
        if pc >= 3970: D["c"] += 1; lec = nombre + " CARO ORO $" + str(pc)
        elif pc <= 3910: D["b"] += 1; lec = nombre + " BARATO ORO $" + str(pc)
        else: lec = nombre + " MEDIO ORO $" + str(pc)
    D["u"] = lec; D["h"].append({"hora": datetime.now().strftime("%H:%M"), "p": pc}); D["h"] = D["h"][-20:]; save(archivo, D); return lec
def calc_lote(lote, ganar, perder, precio, lado, activo):
    div = lote * 100
    if activo in ["EURUSD", "GBPUSD", "AUDUSD"]: d_tp = ganar * 0.001; d_sl = perder * 0.001
    elif activo in ["USDJPY", "USDCHF"]: d_tp = ganar * 0.01; d_sl = perder * 0.01
    else:
        if div == 0: div = 1
        d_tp = ganar / div; d_sl = perder / div
    if lado == "COMPRA": tp = precio + d_tp; sl = precio - d_sl
    else: tp = precio - d_tp; sl = precio + d_sl
    return tp, sl, d_tp, d_sl
def busca_activo(m):
    if "bitcoin" in m or "btc" in m: return "BTC"
    if "ethereum" in m or "eth" in m: return "ETH"
    if "euro" in m or "eur" in m: return "EURUSD"
    if "libra" in m or "gbp" in m: return "GBPUSD"
    if "yen" in m or "jpy" in m: return "USDJPY"
    if "franco" in m or "chf" in m: return "USDCHF"
    if "aud" in m or "austral" in m: return "AUDUSD"
    if "apple" in m or "aapl" in m: return "AAPL"
    if "tesla" in m or "tsla" in m: return "TSLA"
    if "nvidia" in m or "nvda" in m: return "NVDA"
    if "microsoft" in m or "msft" in m: return "MSFT"
    if "amazon" in m or "amzn" in m: return "AMZN"
    if "meta" in m: return "META"
    if "google" in m or "googl" in m: return "GOOGL"
    if "netflix" in m or "nflx" in m: return "NFLX"
    if "amd" in m: return "AMD"
    return "ORO"
def chat_robot(msg, precios, zonas, m5_dato):
    m = msg.lower(); nums = re.findall(r"\d+\.?\d*", msg); activo = busca_activo(m); precio = precios.get(activo, 4088); nombre = NOMBRES.get(activo, activo); z = zonas.get(activo, {})
    lote = 0.01; ganar = 5.0; perder = 2.0
    if "0.02" in msg: lote = 0.02
    if "0.05" in msg: lote = 0.05
    if "0.1" in msg: lote = 0.1
    if "ganar" in m and len(nums) >= 2:
        try: ganar = float(nums[-2]); perder = float(nums[-1])
        except: pass
    if "hola" in m: return "Hola jefe RAUDY ORO. 100 cerebros M5 ZONA en vivo. Dime: m5 oro o compro 0.01 en m5 para ganar 5 y perder 2"
    if "m5" in m: return "M5 MT5 PEGADO - " + m5_dato.get("mensaje", "") + " | TP M5 " + str(m5_dato.get("tp_m5")) + " SL M5 " + str(m5_dato.get("sl_m5")) + " | " + nombre + " $" + str(precio)
    if "zona" in m: return "ZONA " + nombre + ": " + z.get("mensaje", "") + " | TP ZONA " + str(z.get("tp_zona")) + " SL ZONA " + str(z.get("sl_zona"))
    if "bybit" in m: return "BYBIT jefe: BTC $" + str(precios["BTC_BYBIT"]) + ". " + PLATS["BYBIT"]["u"]
    if "binance" in m: return "BINANCE jefe: BTC $" + str(precios["BTC_BINANCE"]) + ". " + PLATS["BINANCE"]["u"]
    if "mt5" in m: return "MT5 M5 PEGADO jefe: ORO $" + str(precios["ORO"]) + " EUR $" + str(precios["EURUSD"]) + " - " + m5_dato.get("mensaje", "")
    if "qr" in m or "broker" in m: return "QR JEFE: Escanea para entrar a " + NOMBRE_BROKER_QR + " Link: " + LINK_BROKER
    if "compr" in m:
        if "ganar" in m or "gana" in m or "perder" in m:
            entrada = ZONAS[activo]["c"] if precio > ZONAS[activo]["c"] else precio; tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "COMPRA", activo); return "Jefe M5 PEGADO: COMPRA " + nombre + " " + str(lote) + " en M5 ZONA $" + str(round(entrada, 4)) + " TP " + str(round(tp, 4)) + " ganas $" + str(ganar) + " SL " + str(round(sl, 4)) + " pierdes $" + str(perder) + ". " + m5_dato.get("mensaje", "")
        return "Dime: compro 0.01 en m5 para ganar 5 y perder 2"
    if "vend" in m:
        if "ganar" in m or "perder" in m:
            entrada = ZONAS[activo]["v"] if precio < ZONAS[activo]["v"] else precio; tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "VENTA", activo); return "Jefe M5 PEGADO: VENTA " + nombre + " " + str(lote) + " en M5 ZONA $" + str(round(tp, 4)) + " ganas $" + str(ganar) + " SL " + str(round(sl, 4)) + " pierdes $" + str(perder)
        return "VENTA " + nombre + " en ZONA $" + str(ZONAS[activo]["v"])
    if "opera" in m or "robot" in m or "auto" in m: return "🤖 ROBOT AUTO: " + OPS["u"] + " | Abiertas: " + str(len(OPS["abiertas"])) + " | Ganado: $" + str(OPS["ganado"]) + " Perdido: $" + str(OPS["perdido"])
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
H.append("<div class='box' style='border-color:#00FF88;background:#001100'><h2>📈 GRAFICO OPERACIONES - ROBOT M5</h2>")
H.append("<canvas id='graf' width='360' height='220'></canvas>")
H.append("<p id='robotEstado' style='font-weight:bold'>🤖 Robot esperando...</p>")
H.append("<p id='robotOps'></p>")
H.append("<button onclick='toggleAuto()' style='background:#00FF88'>🤖 PRENDER / APAGAR ROBOT AUTO</button>")
H.append("<p id='autoEstado'></p></div>")
H.append("<div class='box' style='border-color:#FF4444'><h2>📋 OPERACIONES DEL ROBOT - ORO + EUR + BTC</h2><div id='tablaOps' style='text-align:left'>Cargando operaciones...</div></div>")
H.append("<div class='box m5box'><h2>📊 PEGADO A M5 - MT5 - CADA 5 MINUTOS</h2>")
H.append("<p>Plataforma: MT5 | Timeframe: M5 | Simbolo: XAUUSD ORO</p>")
H.append("<p id='m5Zona' style='font-weight:bold;font-size:16px'>Cargando M5...</p>")
H.append("<p id='m5Dir'></p><p id='m5TP'></p><p id='m5Velas' style='font-size:12px'></p></div>")
H.append("<div class='box qr'><h2>📱 ESCANEA MI BROKER - RAUDY ORO</h2>")
H.append("<img id='qrImg' src='" + qr_url() + "' style='width:250px;height:250px;background:#fff;padding:10px;border-radius:15px'>")
H.append("<p style='font-weight:bold'>BYBIT - RAUDY ORO</p>")
H.append("<p style='font-size:12px;word-break:break-all'>" + LINK_BROKER + "</p>")
H.append("<button onclick=\"window.open('" + LINK_BROKER + "','_blank')\" style='background:#00FF88'>🔗 ABRIR MI BROKER</button></div>")
H.append("<div class='box zona'><h2>📊 ESTRATEGIA ZONA M5 - COMO LA FOTO</h2>")
H.append("<p>⬆️ Si toca ZONA ABAJO en M5 - REBOTA ARRIBA = COMPRA</p>")
H.append("<p>⬇️ Si toca ZONA ARRIBA en M5 - REBOTA ABAJO = VENTA</p>")
H.append("<p id='zonaOro' style='font-weight:bold'>Cargando ZONA...</p>")
H.append("<p>ZONA ARRIBA 🔴 VENTA</p><div class='barra'><div class='relleno' id='barraZona' style='width:50%'></div></div><p>ZONA ABAJO 🟢 COMPRA</p><p id='zonaPos'></p><p id='zonaTP'></p></div>")
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
H.append("<input id='lote' type='number' value='0.01' step='0.01'><input id='ganar' type='number' value='5'><input id='perder' type='number' value='2'><input id='entrada' type='number' value='3910'>")
H.append("<button onclick='calcLote()' style='background:#FF4444;color:#fff'>🛑 CALCULAR TP SL M5</button><p id='loteR' style='background:#111;padding:12px;border-radius:10px'></p></div>")
H.append("<div class='box'><h2>👑 JEFE 100 M5 - RAUDY ORO</h2><p id='j1'></p><p id='j2'></p></div>")
H.append("<h2>🧠 LOS 100 CEREBROS M5 PEGADOS</h2><div class='grid' id='grid'></div><p>RAUDY VIP M5 2026 - WhatsApp 0767574050</p>")
H.append("<script>")
H.append("let g=document.getElementById('grid');")
H.append("for(let i=1;i<=100;i++){let d=document.createElement('div');d.className='robot';let rol='M5 ZONA';if(i>15 && i<=30) rol='M5 DIVISAS';if(i>30 && i<=45) rol='M5 BITCOIN';if(i>45 && i<=60) rol='M5 BINANCE BYBIT';if(i>60 && i<=70) rol='M5 MT5 PEGADO';if(i>70 && i<=80) rol='M5 XTB COINBASE';if(i>80 && i<=90) rol='M5 APPLE TESLA';if(i>90 && i<100) rol='M5 CAPITAL T212';if(i==100) rol='JEFE RAUDY ORO M5';d.innerHTML='<div class=luz></div><b>Cerebro '+i+' M5</b><br>'+rol+'<br><span id=m'+i+'>VIVO M5</span>';g.appendChild(d)}")
H.append("function hablar(t){try{let u=new SpeechSynthesisUtterance(t);u.lang='es-ES';speechSynthesis.speak(u)}catch(e){}}")
H.append("async function enviarChat(){let t=document.getElementById('chat').value;if(!t){document.getElementById('chatR').innerHTML='Escribe algo jefe';return}document.getElementById('chatR').innerHTML='🤖 Pensando M5...';let r=await fetch('/api/chat?msg='+encodeURIComponent(t));let d=await r.json();document.getElementById('chatR').innerHTML='🤖 '+d.respuesta;hablar(d.respuesta)}")
H.append("function ej(t){document.getElementById('chat').value=t;enviarChat()}")
H.append("async function calcLote(){let lote=parseFloat(document.getElementById('lote').value);let ganar=parseFloat(document.getElementById('ganar').value);let perder=parseFloat(document.getElementById('perder').value);let ent=parseFloat(document.getElementById('entrada').value);let act=document.getElementById('selAct').value;let r=await fetch('/api/lote?lote='+lote+'&ganar='+ganar+'&perder='+perder+'&entrada='+ent+'&activo='+act);let d=await r.json();document.getElementById('loteR').innerHTML=d.respuesta;hablar(d.respuesta)}")
H.append("async function toggleAuto(){try{let r=await fetch('/api/robot_auto');let d=await r.json();document.getElementById('autoEstado').innerHTML='Robot AUTO: '+(d.auto?'🟢 PRENDIDO - opera solo':'🔴 APAGADO - solo mira');hablar('Robot '+(d.auto?'prendido':'apagado'))}catch(e){document.getElementById('autoEstado').innerHTML='Error, espera 10 seg y dale otra vez'}}")
H.append("function dibujaGrafico(velas,ops){let c=document.getElementById('graf');if(!c||!velas||velas.length<2)return;let x=c.getContext('2d');x.clearRect(0,0,360,220);let solo=velas.filter(v=>v.a=='ORO');if(solo.length<2)solo=velas;let precios=solo.map(v=>v.p);let mn=Math.min(...precios)-5;let mx=Math.max(...precios)+5;if(mx==mn)mx=mn+1;x.strokeStyle='#FFD700';x.beginPath();solo.forEach((v,i)=>{let px=i/(solo.length-1)*340+10;let py=210-(v.p-mn)/(mx-mn)*190;if(i==0)x.moveTo(px,py);else x.lineTo(px,py)});x.stroke();x.fillStyle='#00FF88';x.fillText('COMPRA ZONA 3910',10,210);x.fillStyle='#FF4444';x.fillText('VENTA ZONA 3970',10,20);if(ops)ops.forEach(o=>{if(o.activo!='ORO')return;let py=210-(o.entrada-mn)/(mx-mn)*190;x.fillStyle=o.lado=='COMPRA'?'#00FF88':'#FF4444';x.beginPath();x.arc(340,py,7,0,7);x.fill();x.fillText(o.lado+' $'+o.entrada,200,py)});}")
H.append("async function up(){try{let r=await fetch('/api/satelite_usa?v='+Date.now());let d=await r.json();document.getElementById('vivo').innerHTML='🟢 EN VIVO M5 '+d.hora+' - ORO $'+d.ORO+' BTC $'+d.BTC;document.getElementById('vivo2').innerHTML='ORO $'+d.ORO+' BTC $'+d.BTC+' EUR $'+d.EURUSD+' M5 PEGADO';document.getElementById('m5Zona').innerHTML=d.m5.mensaje;document.getElementById('m5Dir').innerHTML=d.m5.direccion_m5+' | MT5 M5 | Señales M5: '+d.m5_senales;document.getElementById('m5TP').innerHTML='TP M5 $'+d.m5.tp_m5+' SL M5 $'+d.m5.sl_m5+' - Accion: '+d.m5.accion;document.getElementById('m5Velas').innerHTML='Velas M5: '+JSON.stringify(d.m5.velas_m5);if(d.robot){document.getElementById('robotEstado').innerHTML=d.robot.mensaje;document.getElementById('robotOps').innerHTML='Abiertas: '+d.robot.abiertas.length+' | Cerradas: '+d.robot.cerradas.length+' | Ganado $'+d.robot.ganado+' | Perdido $'+d.robot.perdido+' | AUTO: '+(d.robot.auto?'🟢 ON':'🔴 OFF');let html='<table><tr><th>Hora</th><th>Activo</th><th>Lado</th><th>Entrada</th><th>TP</th><th>SL</th><th>Resultado</th></tr>';d.robot.abiertas.forEach(o=>{html+='<tr><td>'+o.hora+'</td><td>'+o.activo+'</td><td>'+o.lado+'</td><td>'+o.entrada+'</td><td>'+o.tp+'</td><td>'+o.sl+'</td><td>🟢 ABIERTA</td></tr>'});d.robot.cerradas.slice(-5).forEach(o=>{html+='<tr><td>'+o.hora+'</td><td>'+o.activo+'</td><td>'+o.lado+'</td><td>'+o.entrada+'</td><td>'+o.tp+'</td><td>'+o.sl+'</td><td>'+(o.resultado||'')+'</td></tr>'});html+='</table>';document.getElementById('tablaOps').innerHTML=html;dibujaGrafico(d.grafico_velas,d.robot.abiertas);}let z=d.zonas.ORO;document.getElementById('zonaOro').innerHTML=z.mensaje;document.getElementById('barraZona').style.width=z.posicion+'%';document.getElementById('zonaPos').innerHTML='Posicion ZONA M5: '+z.posicion+'% - Abajo $'+z.zona_abajo+' Arriba $'+z.zona_arriba;document.getElementById('zonaTP').innerHTML='TP ZONA $'+z.tp_zona+' SL ZONA $'+z.sl_zona;document.getElementById('divisas').innerHTML='EUR $'+d.EURUSD+' '+d.zonas.EURUSD.accion+' | GBP $'+d.GBPUSD+' '+d.zonas.GBPUSD.accion+' | JPY $'+d.USDJPY+' '+d.zonas.USDJPY.accion;document.getElementById('crypto').innerHTML='BTC $'+d.BTC+' '+d.zonas.BTC.mensaje+' | ETH $'+d.ETH+' '+d.zonas.ETH.accion;document.getElementById('acciones').innerHTML='APPLE $'+d.AAPL+' '+d.zonas.AAPL.accion+' | TESLA $'+d.TSLA+' '+d.zonas.TSLA.accion+' | NVDA $'+d.NVDA+' '+d.zonas.NVDA.accion;document.getElementById('plats').innerHTML='MT5 M5 ORO $'+d.ORO+' | BYBIT BTC $'+d.BTC_BYBIT+' | BINANCE BTC $'+d.BTC_BINANCE+' | COINBASE BTC $'+d.BTC_COINBASE;document.getElementById('j1').innerHTML=d.jefe.orden;document.getElementById('j2').innerHTML=d.jefe.mensaje;for(let i=1;i<=100;i++){let el=document.getElementById('m'+i);if(el)el.innerHTML='M5 VIVO $'+d.ORO+' - '+d.jefe.orden}}catch(e){console.log('esperando server...')}}")
H.append("setInterval(up,10000);up();")
H.append("</script></body></html>")
HTML = "".join(H)

@app.route("/")
def home():
    return HTML
@app.route("/api/ping")
def ping():
    return jsonify({"ok": True, "hora": datetime.now().strftime("%H:%M:%S"), "auto": OPS.get("auto", True)})
@app.route("/api/qr")
def api_qr():
    return jsonify({"link": LINK_BROKER, "nombre": NOMBRE_BROKER_QR, "qr_url": qr_url()})
@app.route("/api/m5")
def api_m5():
    precios = todos_precios(); activo = request.args.get("activo", "ORO")
    if activo not in ZONAS: activo = "ORO"
    m5 = m5_zona_analiza(activo, precios.get(activo, 4088))
    return jsonify({"m5": m5, "config": M5_CONFIG})
@app.route("/api/operaciones")
def api_ops():
    return jsonify({"robot": OPS, "grafico": GRAFICO["velas"]})
@app.route("/api/robot_auto")
def api_auto():
    OPS["auto"] = not OPS.get("auto", True); save("ops.json", OPS)
    return jsonify({"auto": OPS["auto"], "mensaje": OPS["u"]})
@app.route("/api/satelite_usa")
def sat():
    try:
        d = todos_precios(); oro = d["ORO"]; btc = d["BTC"]; zonas = zona_todos(d); m5_dato = m5_zona_analiza("ORO", oro)
        robot_msgs = []
        for act_robot in ["ORO", "EURUSD", "BTC"]:
            precio_robot = d.get(act_robot, oro); m5_robot = m5_zona_analiza(act_robot, precio_robot); msg_robot = robot_decide_y_opera(act_robot, precio_robot, m5_robot); robot_msgs.append(act_robot + ": " + msg_robot)
        robot_msg = " | ".join(robot_msgs)
        if oro <= 3910: orden = "COMPRA"
        elif oro >= 3970: orden = "VENTA"
        else: orden = "ESPERA"
        aprende(oro, orden); m5_aprende(oro)
        plat_aprende("CAPITAL", oro, oro, "Capital.com", "cap.json"); plat_aprende("T212", oro, oro, "Trading 212", "t212.json"); plat_aprende("BINANCE", btc, btc, "Binance", "bin.json"); plat_aprende("ETORO", oro, oro, "eToro", "eto.json"); plat_aprende("MT5", oro, oro, "MT5 M5", "mt5.json"); plat_aprende("XTB", oro, oro, "XTB", "xtb.json"); plat_aprende("COINBASE", d["BTC_COINBASE"], btc, "Coinbase", "coin.json"); plat_aprende("BYBIT", d["BTC_BYBIT"], btc, "Bybit", "bybit.json")
        jefe = {"orden": "🟢 PERMISO M5" if orden != "ESPERA" else "🟡 ESPERA M5", "mensaje": "JEFE RAUDY ORO DICE M5: " + m5_dato["mensaje"]}
        plats_out = {}
        for k in PLATS: plats_out[k] = {"mensaje": k + " - " + str(len(PLATS[k]["h"])) + " jugadas", "leccion": PLATS[k]["u"]}
        return jsonify({**d, "hora": datetime.now().strftime("%H:%M:%S"), "zonas": zonas, "zona_oro": zonas["ORO"], "m5": m5_dato, "m5_senales": M5_ZONA["senales"], "m5_config": M5_CONFIG, "qr": {"link": LINK_BROKER, "nombre": NOMBRE_BROKER_QR, "qr_url": qr_url()}, "cerebro": {"mensaje": "100 cerebros M5 recuerdan " + str(MEM["c"] + MEM["v"] + MEM["e"]) + " jugadas", "leccion": MEM["l"]}, "cerebro_m5": {"mensaje": "M5 - " + str(len(M5["v"])) + " velas", "leccion": M5["u"], "velas": M5["v"][-5:]}, "plats": plats_out, "jefe": jefe, "cerebros": CEREBROS, "total_cerebros": 100, "robot": {"mensaje": robot_msg, "abiertas": OPS["abiertas"], "cerradas": OPS["cerradas"], "ganado": OPS["ganado"], "perdido": OPS["perdido"], "auto": OPS.get("auto", True)}, "grafico_velas": GRAFICO["velas"]})
    except Exception as e:
        return jsonify({"ORO": 4070, "BTC": 98000, "EURUSD": 1.1140, "GBPUSD": 1.2750, "USDJPY": 149.5, "USDCHF": 0.8850, "AUDUSD": 0.6550, "ETH": 3400, "AAPL": 262, "TSLA": 340, "NVDA": 185, "MSFT": 495, "AMZN": 235, "META": 645, "GOOGL": 282, "NFLX": 765, "AMD": 125, "BTC_COINBASE": 98000, "BTC_BINANCE": 98000, "BTC_BYBIT": 98000, "hora": datetime.now().strftime("%H:%M:%S"), "error": str(e), "zonas": {"ORO": {"mensaje": "Error, reintentando", "posicion": 50, "zona_abajo": 3910, "zona_arriba": 3970, "tp_zona": 3910, "sl_zona": 3970, "accion": "ESPERA"}, "EURUSD": {"accion": "ESPERA"}, "GBPUSD": {"accion": "ESPERA"}, "USDJPY": {"accion": "ESPERA"}, "BTC": {"mensaje": "BTC", "accion": "ESPERA"}, "ETH": {"accion": "ESPERA"}, "AAPL": {"accion": "ESPERA"}, "TSLA": {"accion": "ESPERA"}, "NVDA": {"accion": "ESPERA"}}, "m5": {"mensaje": "Reintentando...", "direccion_m5": "ESPERA", "tp_m5": 3910, "sl_m5": 3970, "accion": "ESPERA", "velas_m5": []}, "m5_senales": 0, "robot": {"mensaje": "Robot esperando server...", "abiertas": OPS["abiertas"], "cerradas": OPS["cerradas"], "ganado": OPS["ganado"], "perdido": OPS["perdido"], "auto": OPS.get("auto", True)}, "grafico_velas": GRAFICO["velas"], "jefe": {"orden": "ESPERA", "mensaje": "Reintentando"}, "cerebros": CEREBROS})
@app.route("/api/chat")
def api_chat():
    msg = request.args.get("msg", ""); precios = todos_precios(); zonas = zona_todos(precios); activo = busca_activo(msg.lower()); m5_dato = m5_zona_analiza(activo, precios.get(activo, 4088)); r = chat_robot(msg, precios, zonas, m5_dato); return jsonify({"respuesta": r})
@app.route("/api/lote")
def api_lote():
    try:
        lote = float(request.args.get("lote", 0.01)); ganar = float(request.args.get("ganar", 5)); perder = float(request.args.get("perder", 2)); entrada = float(request.args.get("entrada", 3910)); activo = request.args.get("activo", "ORO"); precios = todos_precios(); precio = precios.get(activo, entrada); z = ZONAS.get(activo, {"c": entrada, "v": entrada})
        if precio <= z["c"] + (z["v"] - z["c"]) * 0.15: lado = "COMPRA"
        elif precio >= z["v"] - (z["v"] - z["c"]) * 0.15: lado = "VENTA"
        else: lado = "COMPRA"
        tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, lado, activo); r = "Lote " + str(lote) + " " + activo + " " + lado + " Entrada $" + str(entrada) + " TP $" + str(round(tp, 4)) + " ganas $" + str(ganar) + " SL $" + str(round(sl, 4)) + " pierdes $" + str(perder); return jsonify({"respuesta": r, "tp": tp, "sl": sl, "lado": lado})
    except Exception as e:
        return jsonify({"respuesta": "Error lote: " + str(e)})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
