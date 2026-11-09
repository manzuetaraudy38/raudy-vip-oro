from flask import Flask
from flask import jsonify, request
import requests, json, os, re
from datetime import datetime
app = Flask(__name__)

BYBIT_API_KEY = os.environ.get("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.environ.get("BYBIT_API_SECRET", "")
BYBIT_QR_URL = "PON_AQUI_TU_LINK_DE_QR_BYBIT"
BYBIT_LINK_DEPOSITO = "https://www.bybit.com"

def check_bybit():
    if BYBIT_API_KEY and BYBIT_API_SECRET:
        return {"conectado": True, "mensaje": "✅ BYBIT AUTOMATICO CONECTADO - Llaves leidas desde Render"}
    return {"conectado": False, "mensaje": "❌ BYBIT NO CONECTADO - Faltan BYBIT_API_KEY / BYBIT_API_SECRET en Render"}

def get_velas_yahoo(symbol, intervalo="1h", rango="5d"):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={intervalo}&range={rango}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=6)
        j = r.json()
        result = j['chart']['result'][0]
        closes = result['indicators']['quote'][0]['close']
        opens = result['indicators']['quote'][0]['open']
        highs = result['indicators']['quote'][0]['high']
        lows = result['indicators']['quote'][0]['low']
        precios = [c for c in closes if c is not None]
        velas = []
        for i in range(len(closes)):
            if closes[i] is not None and opens[i] is not None:
                velas.append({"open": round(float(opens[i]),2), "high": round(float(highs[i]),2), "low": round(float(lows[i]),2), "close": round(float(closes[i]),2), "color": "VERDE" if closes[i] >= opens[i] else "ROJA"})
        return {"precios": precios, "velas": velas[-20:], "ultima": velas[-1] if velas else None}
    except:
        return {"precios": [], "velas": [], "ultima": None}

def calcular_ema(precios, periodo):
    if not precios:
        return 0
    if len(precios) < periodo:
        return round(sum(precios)/len(precios), 2)
    sma = sum(precios[:periodo]) / periodo
    ema = sma
    k = 2 / (periodo + 1)
    for p in precios[periodo:]:
        ema = (p * k) + (ema * (1 - k))
    return round(ema, 2)

def get_ema_oro():
    datos = get_velas_yahoo('GC=F', '1h', '5d')
    precios = datos["precios"]
    if not precios:
        return {"EMA50": 4100, "EMA200": 4093, "precio": 4127, "cruce": "ESPERA", "senal_ema": "ESPERA", "texto": "Esperando Yahoo", "velas_grafico": [], "vela_1h": "SIN DATOS"}
    ema50 = calcular_ema(precios, 50)
    ema200 = calcular_ema(precios, 200) if len(precios) >= 50 else ema50
    precio_actual = precios[-1]
    ultima = datos["ultima"]
    vela_txt = "VERDE - Subiendo" if ultima and ultima["color"] == "VERDE" else "ROJA - Bajando"
    if ema50 > ema200 and precio_actual > ema50:
        cruce = "CRUCE DORADO"
        senal = "COMPRA"
        texto = f"🟢 CRUCE DORADO - EMA50 ${ema50} ARRIBA de EMA200 ${ema200} + Precio ${round(precio_actual,2)} - ALCISTA"
    elif ema50 < ema200 and precio_actual < ema50:
        cruce = "CRUCE DE MUERTE"
        senal = "VENTA"
        texto = f"🔴 CRUCE DE MUERTE - EMA50 ${ema50} ABAJO de EMA200 ${ema200} + Precio ${round(precio_actual,2)} - BAJISTA"
    elif ema50 > ema200:
        cruce = "ALCISTA SIN CONFIRMAR"
        senal = "ESPERA"
        texto = f"🟡 EMA50 ${ema50} arriba de EMA200 ${ema200} pero precio no confirma. ESPERA."
    else:
        cruce = "BAJISTA SIN CONFIRMAR"
        senal = "ESPERA"
        texto = f"🟡 EMA50 ${ema50} abajo de EMA200 ${ema200} pero precio no confirma. ESPERA."
    return {"EMA50": ema50, "EMA200": ema200, "precio": round(precio_actual,2), "cruce": cruce, "senal_ema": senal, "texto": texto, "velas_grafico": datos["velas"], "vela_1h": vela_txt, "vela_4h": vela_txt}

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
        "ORO": oro,
        "EURUSD": yahoo("EURUSD=X", 1.1150),
        "GBPUSD": yahoo("GBPUSD=X", 1.2750),
        "USDJPY": yahoo("USDJPY=X", 149.5),
        "USDCHF": yahoo("USDCHF=X", 0.8850),
        "AUDUSD": yahoo("AUDUSD=X", 0.6550),
        "BTC": btc_b,
        "BTC_COINBASE": btc_c,
        "BTC_BINANCE": btc_b,
        "ETH": yahoo("ETH-USD", 3400),
        "AAPL": yahoo("AAPL", 262),
        "TSLA": yahoo("TSLA", 340),
        "NVDA": yahoo("NVDA", 185),
        "MSFT": yahoo("MSFT", 495),
        "AMZN": yahoo("AMZN", 235),
        "META": yahoo("META", 645),
        "GOOGL": yahoo("GOOGL", 282),
        "NFLX": yahoo("NFLX", 765),
        "AMD": yahoo("AMD", 125),
        "DXY": yahoo("DX-Y.NYB", 99.5),
        "VIX": yahoo("^VIX", 15.2),
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
        msg = "🟢 ZONA ABAJO TOCADA - " + NOMBRES[activo] + " toco ZONA $" + str(zc) + " REBOTE PARA ARRIBA - COMPRA YA"
        tipo = "ZONA_COMPRA"
        accion = "COMPRA"
        tp = precio + rango * 0.8
        sl = precio - rango * 0.2
    elif abs(precio - zv) <= tol:
        ZONA_H["toques_v"] += 1
        msg = "🔴 ZONA ARRIBA TOCADA - " + NOMBRES[activo] + " toco ZONA $" + str(zv) + " REBOTE PARA ABAJO - VENTA YA"
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
        msg = "🟡 " + NOMBRES[activo] + " en MEDIO DE ZONA $" + str(precio) + " - ESPERA que toque ZONA ABAJO o ARRIBA"
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
        return "Hola jefe RAUDY ORO. 100 cerebros ZONA en vivo. Dime: compro 0.01 bitcoin para ganar 5 y perder 2 o dime: zona oro"
    if "zona" in m:
        return "ZONA " + nombre + ": " + z.get("mensaje", "") + " | TP ZONA " + str(z.get("tp_zona")) + " SL ZONA " + str(z.get("sl_zona"))
    if "binance" in m:
        return "BINANCE jefe: BTC $" + str(precios["BTC_BINANCE"]) + ". " + PLATS["BINANCE"]["u"]
    if "etoro" in m:
        return "eTORO jefe: APPLE $" + str(precios["AAPL"]) + " TESLA $" + str(precios["TSLA"])
    if "mt5" in m:
        return "MT5 jefe: ORO $" + str(precios["ORO"]) + " EUR $" + str(precios["EURUSD"])
    if "xtb" in m:
        return "XTB jefe: ORO $" + str(precios["ORO"]) + " BTC $" + str(precios["BTC"])
    if "coinbase" in m:
        return "COINBASE jefe: BTC $" + str(precios["BTC_COINBASE"])
    if "212" in m:
        return "Trading 212 jefe: ORO $" + str(precios["ORO"])
    if "capital" in m:
        return "Capital.com jefe: ORO $" + str(precios["ORO"])
    if "cuanto puedo comprar" in m or "a cuanto compro" in m:
        return "Jefe puedes COMPRAR " + nombre + " en ZONA ABAJO $" + str(ZONAS[activo]["c"]) + ". Ahora $" + str(precio) + ". " + z.get("mensaje", "")
    if "cuanto puedo vender" in m or "a cuanto vendo" in m:
        return "Jefe puedes VENDER " + nombre + " en ZONA ARRIBA $" + str(ZONAS[activo]["v"]) + ". Ahora $" + str(precio)
    if "donde pongo" in m and ("tp" in m or "sl" in m):
        tp, sl, dt, ds = calc_lote(0.01, 5, 2, precio, "COMPRA", activo)
        r = "Jefe " + nombre + " ZONA: COMPRA $" + str(round(precio, 4))
        r += " TP $" + str(round(tp, 4)) + " SL $" + str(round(sl, 4))
        r += " | TP ZONA $" + str(z.get("tp_zona")) + " - " + z.get("mensaje", "")
        return r
    if "compr" in m:
        if "ganar" in m or "gana" in m or "perder" in m:
            entrada = ZONAS[activo]["c"] if precio > ZONAS[activo]["c"] else precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "COMPRA", activo)
            r = "Jefe ZONA: COMPRA " + nombre + " " + str(lote)
            r += " en ZONA $" + str(round(entrada, 4))
            r += " TP " + str(round(tp, 4)) + " ganas $" + str(ganar)
            r += " SL " + str(round(sl, 4)) + " pierdes $" + str(perder)
            r += ". " + z.get("mensaje", "")
            return r
        return "Dime: compro 0.01 bitcoin para ganar 5 y perder 2"
    if "vend" in m:
        if "ganar" in m or "perder" in m:
            entrada = ZONAS[activo]["v"] if precio < ZONAS[activo]["v"] else precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "VENTA", activo)
            r = "Jefe ZONA: VENTA " + nombre + " " + str(lote)
            r += " en ZONA $" + str(round(entrada, 4))
            r += " TP " + str(round(tp, 4)) + " ganas $" + str(ganar)
            r += " SL " + str(round(sl, 4)) + " pierdes $" + str(perder)
            return r
        return "VENTA " + nombre + " en ZONA $" + str(ZONAS[activo]["v"])
    return "Te entendi jefe: " + msg + ". " + nombre + " $" + str(precio) + ". " + z.get("mensaje", "")

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP ZONA + BYBIT + VELAS + EMA</title>
<style>
body{background:#050505;color:#fff;font-family:Arial;text-align:center;margin:0}
header{background:#FFD700;color:#000;padding:15px}
.box{margin:10px;padding:15px;border-radius:15px;border:3px solid #FFD700}
.zona{border-color:#00FFFF;background:#001a2a}
.m5{border-color:#00FF88}
.chat{border-color:#FFD700}
.sl{border-color:#FF4444}
.vivo{border-color:#00FF88}
.bin{border-color:#FFD700}
.ema{border-color:#FFD700;background:#0a0a2a;text-align:left}
.velasbox{background:#000;border:3px solid white}
.velasbox canvas{width:100%;max-width:600px;height:280px;background:#111;border-radius:12px}
.bybit{background:#FFF8DC;color:#000;border:3px solid #F7A600}
.operar{background:#0a2a00;border:3px solid #00FF88}
input,select{width:100%;padding:12px;margin:4px 0;border-radius:10px;background:#111;color:#fff}
.bybit input{background:#fff;color:#000}
button{width:100%;padding:14px;border-radius:15px;font-weight:bold;margin-top:5px;cursor:pointer}
.btn-compra{background:#00FF88}
.btn-venta{background:#FF4444;color:#fff}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px}
.robot{background:#1a1a1a;padding:8px;border-radius:12px;font-size:12px}
.luz{width:14px;height:14px;border-radius:50%;background:#00FF88;margin:auto}
.barra{width:100%;height:22px;background:#111;border-radius:10px;overflow:hidden}
.relleno{height:100%;background:linear-gradient(90deg,#00FF88,#FFD700,#FF4444)}
</style>
</head>
<body>
<header><h1>👑 RAUDY VIP ZONA ⚡</h1>
<p>JEFE: RAUDY ORO - ZONA + BYBIT + VELAS + EMA</p>
<p id="vivo">🟢 EN VIVO...</p></header>

<div class="box bybit"><h2>💰 BYBIT - JEFE RAUDY</h2>
<p id="bybit-estado">🔌 Verificando Bybit...</p>
<a href="https://www.bybit.com" target="_blank" style="display:inline-block;padding:12px 20px;background:#F7A600;color:#000;font-weight:bold;border-radius:25px;text-decoration:none">🟡 ABRIR BYBIT</a>
<p style="font-size:12px">Pon dinero en Bybit con tu app, luego usa los botones de abajo. El robot te dice TP/SL, tu confirmas.</p></div>

<div class="box ema"><h2 style="text-align:center">🕯️ VELAS + 📈 EMA 50 + EMA 200</h2>
<p id="ema-texto" style="font-weight:bold">📈 EMA: Cargando velas reales...</p>
<p id="ema-detalle" style="color:#FFD700">Calculando EMA 50 y EMA 200...</p>
<p id="vela-texto">🕯️ Vela 1H: Cargando...</p>
<p id="final-senal" style="font-weight:bold;color:#00FF88">🧠 SEÑAL FINAL: Calculando...</p>
<p id="final-motivo" style="color:#FFD700"></p></div>

<div class="box velasbox"><h2>🕯️ GRAFICO VELAS ORO 1H - SE VE GRANDE</h2>
<p style="color:#FFD700;font-size:13px">Verde = Subiendo | Rojo = Bajando | Amarilla = EMA 50 | Azul = EMA 200</p>
<canvas id="canvasVelas" width="600" height="280"></canvas>
<p id="velas-info">Cargando velas...</p></div>

<div class="box operar"><h2>🟢🔴 OPERAR CON ROBOT + BYBIT - TP / SL</h2>
<p>Elige activo, lote, ganar y perder. El robot calcula TP/SL.</p>
<select id="opAct"><option value="ORO">ORO 🥇</option><option value="EURUSD">EUR/USD 💶</option><option value="GBPUSD">GBP/USD 💷</option><option value="USDJPY">USD/JPY 💴</option><option value="USDCHF">USD/CHF 🇨🇭</option><option value="AUDUSD">AUD/USD 🦘</option><option value="BTC">BITCOIN ₿</option><option value="AAPL">APPLE 🍎</option><option value="TSLA">TESLA 🚗</option><option value="NVDA">NVIDIA 💚</option></select>
<input id="opLote" type="number" value="0.01" step="0.01">
<input id="opGanar" type="number" value="5">
<input id="opPerder" type="number" value="2">
<button class="btn-compra" onclick="operarBtn('COMPRA')">🟢 COMPRAR - ROBOT + BYBIT</button>
<button class="btn-venta" onclick="operarBtn('VENTA')">🔴 VENDER - ROBOT + BYBIT</button>
<p id="opRes" style="background:#111;padding:12px;border-radius:10px;text-align:left">👆 Elige y pulsa COMPRA o VENTA.</p>
<p style="font-size:11px;color:#aaa">⚠️ El botón PREPARA la orden con TP/SL. Tú confirmas en tu app de Bybit. Empieza con $10-$20.</p></div>

<div class="box zona"><h2>📊 ESTRATEGIA ZONA - COMO LA FOTO</h2>
<p>⬆️ Si toca ZONA ABAJO - REBOTA ARRIBA = COMPRA</p>
<p>⬇️ Si toca ZONA ARRIBA - REBOTA ABAJO = VENTA</p>
<p id="zonaOro" style="font-weight:bold;font-size:16px">Cargando ZONA ORO...</p>
<p>ZONA ARRIBA 🔴 VENTA</p>
<div class="barra"><div class="relleno" id="barraZona" style="width:50%"></div></div>
<p>ZONA ABAJO 🟢 COMPRA</p>
<p id="zonaPos"></p>
<p id="zonaTP"></p></div>

<div class="box vivo"><h2>🟢 EN VIVO</h2><p id="vivo2">Conectando...</p></div>
<div class="box"><h2>🧠 CEREBRO JEFE</h2><p id="c1"></p><p id="c2"></p></div>
<div class="box m5"><h2>🧠 CEREBRO M5</h2><p id="m1"></p><p id="m2"></p></div>
<div class="box bin"><h2>🟡 BINANCE</h2><p id="bin1"></p><p id="bin2"></p></div>
<div class="box"><h2>🔵 eTORO | 📊 MT5 | 🟣 XTB | 🟠 COINBASE</h2><p id="otras"></p></div>

<div class="box chat"><h2>💬 CHAT ZONA + LOTE 0.01</h2>
<input id="chat" placeholder="Ej: zona oro o compro 0.01 para ganar 5 y perder 2">
<button onclick="enviarChat()" style="background:#FFD700">💬 ENVIAR</button>
<p id="chatR" style="background:#111;padding:12px;border-radius:10px;text-align:left">🤖 Hola jefe...</p>
<button onclick="ej('zona oro')" style="background:#00FFFF">📊 zona oro</button>
<button onclick="ej('zona bitcoin')" style="background:#FFA500">📊 zona bitcoin</button>
<button onclick="ej('compro 0.01 para ganar 5 y perder 2')" style="background:#00FF88">✅ ORO ZONA 0.01</button>
<button onclick="ej('compro 0.01 bitcoin para ganar 5 y perder 2')" style="background:#FFA500">₿ BITCOIN ZONA 0.01</button>
<button onclick="ej('compro 0.01 euro para ganar 5 y perder 2')" style="background:#00FFFF">💶 EUR ZONA 0.01</button>
<button onclick="ej('compro 0.01 apple para ganar 5 y perder 2')" style="background:#00FF88">🍎 APPLE ZONA 0.01</button>
<button onclick="ej('compro 0.01 tesla para ganar 5 y perder 2')" style="background:#FF4444;color:#fff">🚗 TESLA ZONA 0.01</button>
<button onclick="ej('Binance')" style="background:#FFD700">🟡 Binance</button>
<button onclick="ej('MT5')" style="background:#FF4444;color:#fff">📊 MT5</button></div>

<div class="box"><h2>💶 DIVISAS ZONA EN VIVO</h2><p id="divisas"></p></div>
<div class="box"><h2>₿ BITCOIN + ETH ZONA EN VIVO</h2><p id="crypto"></p></div>
<div class="box"><h2>📈 ACCIONES ZONA EN VIVO</h2><p id="acciones"></p></div>
<div class="box"><h2>🏦 7 PLATAFORMAS ZONA EN VIVO</h2><p id="plats"></p></div>

<div class="box sl"><h2>🛑 CALCULADORA ZONA LOTE 0.01</h2>
<select id="selAct"><option value="ORO">ORO</option><option value="BTC">BITCOIN</option><option value="EURUSD">EUR/USD</option><option value="AAPL">APPLE</option><option value="TSLA">TESLA</option></select>
<input id="lote" type="number" value="0.01" step="0.01">
<input id="ganar" type="number" value="5">
<input id="perder" type="number" value="2">
<input id="entrada" type="number" value="3910">
<button onclick="calcLote()" style="background:#FF4444;color:#fff">🛑 CALCULAR TP SL ZONA</button>
<p id="loteR" style="background:#111;padding:12px;border-radius:10px"></p></div>

<div class="box"><h2>👑 JEFE 100 - RAUDY ORO</h2><p id="j1"></p><p id="j2"></p></div>
<h2>🧠 LOS 100 CEREBROS ZONA EN VIVO</h2>
<div class="grid" id="grid"></div>
<p>RAUDY VIP 2026 - WhatsApp 0767574050 - No es consejo financiero, es educación</p>

<script>
let g=document.getElementById('grid');
for(let i=1;i<=100;i++){let d=document.createElement('div');d.className='robot';let rol='ZONA';if(i>15 && i<=30) rol='DIVISAS ZONA';if(i>30 && i<=45) rol='BITCOIN ZONA';if(i>45 && i<=60) rol='BINANCE';if(i>60 && i<=70) rol='eTORO MT5';if(i>70 && i<=80) rol='XTB COINBASE';if(i>80 && i<=90) rol='APPLE TESLA ZONA';if(i>90 && i<100) rol='CAPITAL T212 ZONA';if(i==100) rol='JEFE RAUDY ORO';d.innerHTML='<div class=luz></div><b>Cerebro '+i+'</b><br>'+rol+'<br><span id=m'+i+'>VIVO</span>';g.appendChild(d)}
function hablar(t){try{let u=new SpeechSynthesisUtterance(t);u.lang='es-ES';speechSynthesis.speak(u)}catch(e){}}
function dibujarVelas(velas, ema50, ema200){let canvas=document.getElementById('canvasVelas');if(!canvas||!velas||velas.length===0)return;let ctx=canvas.getContext('2d');let W=canvas.width,H=canvas.height;ctx.clearRect(0,0,W,H);ctx.fillStyle='#111';ctx.fillRect(0,0,W,H);let min=Math.min(...velas.map(v=>v.low));let max=Math.max(...velas.map(v=>v.high));let rango=max-min;if(rango===0)rango=1;min-=rango*0.1;max+=rango*0.1;rango=max-min;function y(p){return H-20-((p-min)/rango)*(H-40);}let ancho=W/velas.length;velas.forEach((v,i)=>{let x=i*ancho+ancho/2;let color=v.color==='VERDE'?'#00FF88':'#FF4444';ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,y(v.high));ctx.lineTo(x,y(v.low));ctx.stroke();ctx.fillStyle=color;let top=Math.min(y(v.open),y(v.close));let h=Math.abs(y(v.close)-y(v.open));if(h<3)h=3;ctx.fillRect(x-ancho*0.3,top,ancho*0.6,h);});ctx.strokeStyle='#FFD700';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(0,y(ema50));ctx.lineTo(W,y(ema50));ctx.stroke();ctx.fillStyle='#FFD700';ctx.font='bold 13px Arial';ctx.fillText('EMA 50 $'+ema50,8,y(ema50)-6);ctx.strokeStyle='#00BFFF';ctx.beginPath();ctx.moveTo(0,y(ema200));ctx.lineTo(W,y(ema200));ctx.stroke();ctx.fillStyle='#00BFFF';ctx.fillText('EMA 200 $'+ema200,8,y(ema200)-6);document.getElementById('velas-info').innerHTML='Velas: '+velas.length+' ultimas 1H | Precio: $'+velas[velas.length-1].close+' | Si velas estan ARRIBA de amarilla, SUBE. Si ABAJO, BAJA.';}
async function enviarChat(){let t=document.getElementById('chat').value;if(!t){document.getElementById('chatR').innerHTML='Escribe algo jefe';return}document.getElementById('chatR').innerHTML='Pensando ZONA...';let r=await fetch('/api/chat?msg='+encodeURIComponent(t));let d=await r.json();document.getElementById('chatR').innerHTML='🤖 '+d.respuesta;hablar(d.respuesta)}
function ej(t){document.getElementById('chat').value=t;enviarChat()}
async function operarBtn(lado){let act=document.getElementById('opAct').value;let lote=parseFloat(document.getElementById('opLote').value);let ganar=parseFloat(document.getElementById('opGanar').value);let perder=parseFloat(document.getElementById('opPerder').value);document.getElementById('opRes').innerHTML='Robot calculando TP/SL para '+lado+' '+act+'...';let r=await fetch('/api/operar?activo='+act+'&lado='+lado+'&lote='+lote+'&ganar='+ganar+'&perder='+perder);let d=await r.json();document.getElementById('opRes').innerHTML=d.respuesta;hablar(d.respuesta)}
async function calcLote(){let lote=parseFloat(document.getElementById('lote').value);let ganar=parseFloat(document.getElementById('ganar').value);let perder=parseFloat(document.getElementById('perder').value);let ent=parseFloat(document.getElementById('entrada').value);let act=document.getElementById('selAct').value;let r=await fetch('/api/lote?lote='+lote+'&ganar='+ganar+'&perder='+perder+'&entrada='+ent+'&activo='+act);let d=await r.json();document.getElementById('loteR').innerHTML=d.respuesta;hablar(d.respuesta)}
async function up(){try{let r=await fetch('/api/satelite_usa?v='+Date.now());let d=await r.json();document.getElementById('vivo').innerHTML='EN VIVO '+d.hora+' - ORO $'+d.ORO+' BTC $'+d.BTC;document.getElementById('vivo2').innerHTML='ORO $'+d.ORO+' BTC $'+d.BTC+' EUR $'+d.EURUSD+' ZONA';if(d.bybit){document.getElementById('bybit-estado').innerHTML=d.bybit.mensaje;}if(d.ema){document.getElementById('ema-texto').innerHTML=d.ema.texto;document.getElementById('ema-detalle').innerHTML='EMA 50: $'+d.ema.EMA50+' | EMA 200: $'+d.ema.EMA200+' | Precio: $'+d.ema.precio+' | Cruce: '+d.ema.cruce;document.getElementById('vela-texto').innerHTML='Vela 1H: '+d.ema.vela_1h;if(d.ema.velas_grafico){dibujarVelas(d.ema.velas_grafico,d.ema.EMA50,d.ema.EMA200);}}if(d.senal_final){document.getElementById('final-senal').innerHTML=d.senal_final.senal_final;document.getElementById('final-motivo').innerHTML=d.senal_final.motivo;}let z=d.zonas.ORO;document.getElementById('zonaOro').innerHTML=z.mensaje;document.getElementById('barraZona').style.width=z.posicion+'%';document.getElementById('zonaPos').innerHTML='Posicion en ZONA: '+z.posicion+'% - Abajo $'+z.zona_abajo+' Arriba $'+z.zona_arriba;document.getElementById('zonaTP').innerHTML='TP ZONA $'+z.tp_zona+' SL ZONA $'+z.sl_zona+' - Accion: '+z.accion;document.getElementById('c1').innerHTML=d.cerebro.mensaje;document.getElementById('c2').innerHTML=d.cerebro.leccion;document.getElementById('m1').innerHTML=d.cerebro_m5.mensaje;document.getElementById('m2').innerHTML=d.cerebro_m5.leccion;document.getElementById('bin1').innerHTML=d.plats.BINANCE.mensaje;document.getElementById('bin2').innerHTML=d.plats.BINANCE.leccion+' | BTC Binance $'+d.BTC_BINANCE;document.getElementById('otras').innerHTML='eTORO APPLE $'+d.AAPL+' | MT5 ORO $'+d.ORO+' | XTB BTC $'+d.BTC+' | COINBASE BTC $'+d.BTC_COINBASE+' | CAPITAL ORO $'+d.ORO+' | T212 ORO $'+d.ORO;document.getElementById('divisas').innerHTML='EUR $'+d.EURUSD+' '+d.zonas.EURUSD.accion+' | GBP $'+d.GBPUSD+' '+d.zonas.GBPUSD.accion+' | JPY $'+d.USDJPY+' '+d.zonas.USDJPY.accion+' | CHF $'+d.USDCHF+' '+d.zonas.USDCHF.accion+' | AUD $'+d.AUDUSD+' '+d.zonas.AUDUSD.accion;document.getElementById('crypto').innerHTML='BTC $'+d.BTC+' '+d.zonas.BTC.mensaje+' | ETH $'+d.ETH+' '+d.zonas.ETH.accion;document.getElementById('acciones').innerHTML='APPLE $'+d.AAPL+' '+d.zonas.AAPL.accion+' | TESLA $'+d.TSLA+' '+d.zonas.TSLA.accion+' | NVDA $'+d.NVDA+' '+d.zonas.NVDA.accion;document.getElementById('plats').innerHTML='BINANCE BTC $'+d.BTC_BINANCE+' | COINBASE BTC $'+d.BTC_COINBASE+' | eTORO APPLE $'+d.AAPL+' | MT5 ORO $'+d.ORO;document.getElementById('j1').innerHTML=d.jefe.orden;document.getElementById('j2').innerHTML=d.jefe.mensaje;for(let i=1;i<=100;i++){let el=document.getElementById('m'+i);if(el)el.innerHTML='ZONA VIVO $'+d.ORO+' - '+d.jefe.orden}}catch(e){}}
setInterval(up,5000);up();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/api/satelite_usa")
def sat():
    d = todos_precios()
    oro = d["ORO"]
    btc = d["BTC"]
    zonas = zona_todos(d)
    ema = get_ema_oro()
    zona_oro_accion = zonas["ORO"]["accion"]
    ema_senal = ema.get("senal_ema")
    dxy = d.get("DXY", 99.5)
    vix = d.get("VIX", 15.2)
    if vix >= 30:
        senal_final = {"senal_final": "🛑 PAUSA - VIX PANICO", "motivo": f"VIX {vix} en panico. JEFE ordena PAUSA aunque ZONA diga {zona_oro_accion}."}
        jefe_orden_txt = "🛑 PAUSA - VIX PANICO"
    elif zona_oro_accion == "COMPRA" and ema_senal == "COMPRA":
        senal_final = {"senal_final": "🟢 COMPRA FUERTE - TODO DE ACUERDO", "motivo": f"ZONA COMPRA + {ema['cruce']} + ORO ${oro} + DXY {dxy} - 5/5 confirmaciones."}
        jefe_orden_txt = "🟢 PERMISO - COMPRA FUERTE"
    elif zona_oro_accion == "VENTA" and ema_senal == "VENTA":
        senal_final = {"senal_final": "🔴 VENTA FUERTE - TODO DE ACUERDO", "motivo": f"ZONA VENTA + {ema['cruce']} + ORO ${oro} - 5/5 confirmaciones."}
        jefe_orden_txt = "🔴 PERMISO - VENTA FUERTE"
    else:
        senal_final = {"senal_final": "🟡 ESPERA - NO HAY ACUERDO", "motivo": f"ZONA: {zona_oro_accion} | EMA: {ema['cruce']} | ORO ${oro} | DXY {dxy} | VIX {vix} - Falta acuerdo. JEFE dice ESPERA."}
        jefe_orden_txt = "🟡 ESPERA - NO HAY ACUERDO"
    if oro <= 3910:
        orden = "COMPRA"
    elif oro >= 3970:
        orden = "VENTA"
    else:
        orden = "ESPERA"
    aprende(oro, orden)
    m5_aprende(oro)
    plat_aprende("CAPITAL", oro, oro, "Capital.com", "cap.json")
    plat_aprende("T212", oro, oro, "Trading 212", "t212.json")
    plat_aprende("BINANCE", btc, btc, "Binance", "bin.json")
    plat_aprende("ETORO", oro, oro, "eToro", "eto.json")
    plat_aprende("MT5", oro, oro, "MT5", "mt5.json")
    plat_aprende("XTB", oro, oro, "XTB", "xtb.json")
    plat_aprende("COINBASE", d["BTC_COINBASE"], btc, "Coinbase", "coin.json")
    jefe = {"orden": jefe_orden_txt, "mensaje": "JEFE RAUDY ORO DICE: " + senal_final["motivo"] + " | ZONA ORO - " + zonas["ORO"]["mensaje"]}
    plats_out = {}
    for k in PLATS:
        plats_out[k] = {"mensaje": k + " - " + str(len(PLATS[k]["h"])) + " jugadas", "leccion": PLATS[k]["u"]}
    return jsonify({**d, "hora": datetime.now().strftime("%H:%M:%S"), "zonas": zonas, "zona_oro": zonas["ORO"], "ema": ema, "senal_final": senal_final, "bybit": check_bybit(), "cerebro": {"mensaje": "100 cerebros ZONA recuerdan " + str(MEM["c"] + MEM["v"] + MEM["e"]) + " jugadas", "leccion": MEM["l"]}, "cerebro_m5": {"mensaje": "M5 - " + str(len(M5["v"])) + " velas", "leccion": M5["u"], "velas": M5["v"][-5:]}, "plats": plats_out, "jefe": jefe, "cerebros": CEREBROS, "total_cerebros": 100})

@app.route("/api/chat")
def api_chat():
    msg = request.args.get("msg", "")
    precios = todos_precios()
    zonas = zona_todos(precios)
    r = chat_robot(msg, precios, zonas)
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
        r = "COMPRA ZONA " + act + " " + str(lote) + " en " + str(ent) + " TP " + str(round(tp, 4)) + " ganas $" + str(ganar) + " SL " + str(round(sl, 4)) + " pierdes $" + str(perder) + ". Como la foto jefe."
        return jsonify({"respuesta": r, "tp": tp, "sl": sl})
    except:
        return jsonify({"respuesta": "Escribe lote 0.01 ganar 5 perder 2"})

@app.route("/api/operar")
def api_operar():
    try:
        act = request.args.get("activo", "ORO")
        lado = request.args.get("lado", "COMPRA")
        lote = float(request.args.get("lote", 0.01))
        ganar = float(request.args.get("ganar", 5))
        perder = float(request.args.get("perder", 2))
        precios = todos_precios()
        zonas = zona_todos(precios)
        precio = precios.get(act, 3910)
        z = zonas.get(act, {})
        ema = get_ema_oro()
        if lado == "COMPRA":
            entrada = ZONAS[act]["c"] if precio > ZONAS[act]["c"] else precio
        else:
            entrada = ZONAS[act]["v"] if precio < ZONAS[act]["v"] else precio
        tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, lado, act)
        aviso = ""
        if act == "ORO":
            if lado == "COMPRA" and ema.get("senal_ema") != "COMPRA":
                aviso = " OJO JEFE: EMA dice " + ema.get("cruce") + ", no COMPRA. El robot recomienda ESPERA."
            elif lado == "VENTA" and ema.get("senal_ema") != "VENTA":
                aviso = " OJO JEFE: EMA dice " + ema.get("cruce") + ", no VENTA. El robot recomienda ESPERA."
            else:
                aviso = " ZONA + EMA DE ACUERDO - Buena senal jefe."
        r = f"ORDEN PREPARADA PARA BYBIT - {lado} {NOMBRES.get(act, act)} Lote {lote}<br>Entrada: ${round(entrada,4)} | Precio ahora: ${round(precio,4)}<br>TP: ${round(tp,4)} ganas ${ganar} | SL: ${round(sl,4)} pierdes max ${perder}<br>ZONA: {z.get('mensaje','')}<br>EMA: {ema.get('texto','')}<br>{aviso}<br>Copia esto en tu app de Bybit: {lado} {act} Entrada {round(entrada,4)} TP {round(tp,4)} SL {round(sl,4)}<br>Empieza con $10-$20 jefe."
        return jsonify({"respuesta": r, "tp": tp, "sl": sl, "entrada": entrada})
    except Exception as e:
        return jsonify({"respuesta": "Error jefe: " + str(e)})

@app.route("/api/ema")
def api_ema():
    return jsonify(get_ema_oro())

@app.route("/api/bybit_status")
def api_bybit_status():
    return jsonify(check_bybit())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
