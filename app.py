from flask import Flask
from flask import jsonify, request
import requests, json, os, re, urllib.parse, time, hmac, hashlib
from datetime import datetime
app = Flask(__name__)

LINK_BROKER = "https://www.bybit.com/invite?ref=RAUDYORO"
NOMBRE_BROKER_QR = "BYBIT - RAUDY ORO"
M5_CONFIG = {"plataforma": "MT5", "timeframe": "M5", "simbolo": "XAUUSD", "activa": True, "jefe": "RAUDY ORO"}

# ===== BYBIT - CONEXION ROBOT =====
BYBIT_KEY = os.environ.get("BYBIT_API_KEY", "")
BYBIT_SECRET = os.environ.get("BYBIT_API_SECRET", "")
BYBIT_TESTNET = os.environ.get("BYBIT_TESTNET", "false") == "true"
BYBIT_BASE = "https://api-testnet.bybit.com" if BYBIT_TESTNET else "https://api.bytick.com"
# ORO en Bybit = PAXGUSDT, EUR/USD no hay en Spot, usamos EURUSDT, BTC = BTCUSDT
MAP_BYBIT = {"ORO": "PAXGUSDT", "BTC": "BTCUSDT", "EURUSD": "EURUSDT"}

def bybit_firma(ts, body_str):
    msg = ts + BYBIT_KEY + "5000" + body_str
    return hmac.new(BYBIT_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()

def bybit_orden_real(simbolo, lado, cantidad):
    # lado: Buy / Sell
    if not BYBIT_KEY or not BYBIT_SECRET:
        return {"ok": False, "msg": "Sin llave Bybit - sigue en SIMULACION"}
    try:
        ts = str(int(time.time()*1000))
        body = {"category": "spot", "symbol": simbolo, "side": lado, "orderType": "Market", "qty": str(cantidad)}
        body_str = json.dumps(body)
        headers = {"X-BAPI-API-KEY": BYBIT_KEY, "X-BAPI-TIMESTAMP": ts, "X-BAPI-RECV-WINDOW": "5000", "X-BAPI-SIGN": bybit_firma(ts, body_str), "Content-Type": "application/json"}
        r = requests.post(BYBIT_BASE + "/v5/order/create", json=body, headers=headers, timeout=10)
        j = r.json()
        if j.get("retCode") == 0:
            return {"ok": True, "msg": "Orden Bybit OK " + simbolo + " " + lado, "data": j}
        else:
            return {"ok": False, "msg": "Bybit error: " + str(j.get("retMsg")), "data": j}
    except Exception as e:
        return {"ok": False, "msg": "Error Bybit: " + str(e)}

def bybit_balance():
    if not BYBIT_KEY or not BYBIT_SECRET:
        return {"ok": False, "msg": "Sin llave - pon BYBIT_API_KEY en Render Environment"}
    try:
        ts = str(int(time.time()*1000))
        params = "accountType=UNIFIED"
        firma = hmac.new(BYBIT_SECRET.encode(), (ts + BYBIT_KEY + "5000" + params).encode(), hashlib.sha256).hexdigest()
        headers = {"X-BAPI-API-KEY": BYBIT_KEY, "X-BAPI-TIMESTAMP": ts, "X-BAPI-RECV-WINDOW": "5000", "X-BAPI-SIGN": firma}
        r = requests.get(BYBIT_BASE + "/v5/account/wallet-balance?" + params, headers=headers, timeout=10)
        return {"ok": True, "data": r.json(), "modo": "TESTNET" if BYBIT_TESTNET else "REAL"}
    except Exception as e:
        return {"ok": False, "msg": str(e)}

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
        r = requests.get("https://api.bytick.com/v5/market/tickers?category=spot&symbol=BTCUSDT", timeout=3)
        return float(r.json()["result"]["list"][0]["lastPrice"])
    except:
        return yahoo("BTC-USD", 98000)

def todos_precios():
    global _CACHE
    ahora = time.time()
    if _CACHE["datos"] is not None and (ahora - _CACHE["tiempo"] < 30):
        return _CACHE["datos"]
    try:
        oro = oro_real(); btc_b = precio_binance(); btc_c = precio_coinbase(); btc_y = precio_bybit()
        d = {"ORO": oro, "EURUSD": yahoo("EURUSD=X", 1.1150),"GBPUSD": yahoo("GBPUSD=X", 1.2750), "USDJPY": yahoo("USDJPY=X", 149.5),"USDCHF": yahoo("USDCHF=X", 0.8850), "AUDUSD": yahoo("AUDUSD=X", 0.6550),"BTC": btc_b, "BTC_COINBASE": btc_c, "BTC_BINANCE": btc_b, "BTC_BYBIT": btc_y,"ETH": yahoo("ETH-USD", 3400), "AAPL": yahoo("AAPL", 262),"TSLA": yahoo("TSLA", 340), "NVDA": yahoo("NVDA", 185),"MSFT": yahoo("MSFT", 495), "AMZN": yahoo("AMZN", 235),"META": yahoo("META", 645), "GOOGL": yahoo("GOOGL", 282),"NFLX": yahoo("NFLX", 765), "AMD": yahoo("AMD", 125)}
    except:
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
                # Si gano/perdio, cierra tambien en Bybit con orden contraria
                if op.get("bybit_id"):
                    lado_cierre = "Sell" if op["lado"] == "COMPRA" else "Buy"
                    bybit_orden_real(MAP_BYBIT.get(activo, "PAXGUSDT"), lado_cierre, op.get("bybit_qty", "0.002"))
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
        # ===== CONECTA A BYBIT - SOLO SI HAY LLAVE =====
        bybit_msg = "SIMULACION"
        bybit_qty = "0.002"
        if activo == "BTC": bybit_qty = "0.0001"
        if activo == "EURUSD": bybit_qty = "5"
        bybit_id = ""
        if BYBIT_KEY:
            simbolo = MAP_BYBIT.get(activo, "PAXGUSDT")
            lado_bybit = "Buy" if lado == "COMPRA" else "Sell"
            res = bybit_orden_real(simbolo, lado_bybit, bybit_qty)
            bybit_msg = res.get("msg", "")
            if res.get("ok"):
                try: bybit_id = res["data"]["result"].get("orderId", "")
                except: bybit_id = "OK"
        nueva = {"activo": activo, "lado": lado, "entrada": precio, "tp": tp, "sl": sl, "lote": 0.01, "ganar": 5, "perder": 2, "hora": datetime.now().strftime("%H:%M"), "estado": "ABIERTA", "motivo": m5_dato.get("mensaje", ""), "bybit": bybit_msg, "bybit_id": bybit_id, "bybit_qty": bybit_qty}
        OPS["abiertas"].append(nueva); OPS["h"].append(nueva)
        OPS["u"] = "🤖 ROBOT ABRIO SOLO: " + lado + " " + activo + " en $" + str(precio) + " TP $" + str(tp) + " SL $" + str(sl) + " | BYBIT: " + bybit_msg
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
    if "bybit" in m: return "BYBIT jefe: BTC $" + str(precios["BTC_BYBIT"]) + ". " + PLATS["BYBIT"]["u"] + " | Llave: " + ("SI CONECTADA " + ("TESTNET" if BYBIT_TESTNET else "REAL") if BYBIT_KEY else "NO - pon llave en Render")
    if "binance" in m: return "BINANCE jefe: BTC $" + str(precios["BTC_BINANCE"]) + ". " + PLATS["BINANCE"]["u"]
    if "mt5" in m: return "MT5 M5 PEGADO jefe: ORO $" + str(precios["ORO"]) + " EUR $" + str(precios["EURUSD"]) + " - " + m5_dato.get("mensaje", "")
    if "qr" in m or "broker" in m: return "QR JEFE: Escanea para entrar a " + NOMBRE_BROKER_QR + " Link: " + LINK_BROKER
    if "compr" in m:
        if "ganar" in m or "gana" in m or "perder" in m:
            entrada = ZONAS[activo]["c"] if precio > ZONAS[activo]["c"] else precio; tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "COMPRA", activo); return "Jefe M5 PEGADO: COMPRA " + nombre + " " + str(lote) + " en M5 ZONA $" + str(round(entrada, 4)) + " TP " + str(round(tp, 4)) + " ganas $" + str(ganar) + " SL " + str(round(sl, 4)) + " pierdes $" + str(perder) + ". " + m5_dato.get("mensaje", "")
        return "Dime: compro 0.01 en m5 para
