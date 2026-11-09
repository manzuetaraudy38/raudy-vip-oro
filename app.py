from flask import Flask, jsonify, request
import requests, json, os, re, threading, time
from datetime import datetime

app = Flask(__name__)

# ===== LLAVES - SE PONEN EN RENDER, NO AQUI =====
BYBIT_API_KEY = os.environ.get("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.environ.get("BYBIT_API_SECRET", "")
# Para prueba pon True, para real pon False
USAR_TESTNET = os.environ.get("USAR_TESTNET", "True") == "True"

# Intenta importar pybit, si no esta, no rompe la pagina
try:
    from pybit.unified_trading import HTTP
    HAY_PYBIT = True
except:
    HAY_PYBIT = False
    print("No hay pybit todavia, instalando...")

def get_session():
    if not HAY_PYBIT or not BYBIT_API_KEY:
        return None
    try:
        return HTTP(testnet=USAR_TESTNET, api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)
    except Exception as e:
        print(f"Error session: {e}")
        return None

def check_bybit():
    if BYBIT_API_KEY and BYBIT_API_SECRET:
        return {"conectado": True, "mensaje": "✅ BYBIT CONECTADO - Testnet" if USAR_TESTNET else "✅ BYBIT CONECTADO - REAL"}
    return {"conectado": False, "mensaje": "❌ BYBIT NO CONECTADO - Faltan llaves en Render"}

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
        cruce = "CRUCE DORADO"; senal = "COMPRA"; texto = f"🟢 CRUCE DORADO - EMA50 ${ema50} ARRIBA de EMA200 ${ema200} + Precio ${round(precio_actual,2)} - ALCISTA"
    elif ema50 < ema200 and precio_actual < ema50:
        cruce = "CRUCE DE MUERTE"; senal = "VENTA"; texto = f"🔴 CRUCE DE MUERTE - EMA50 ${ema50} ABAJO de EMA200 ${ema200} + Precio ${round(precio_actual,2)} - BAJISTA"
    elif ema50 > ema200:
        cruce = "ALCISTA SIN CONFIRMAR"; senal = "ESPERA"; texto = f"🟡 EMA50 ${ema50} arriba de EMA200 ${ema200} pero precio no confirma. ESPERA."
    else:
        cruce = "BAJISTA SIN CONFIRMAR"; senal = "ESPERA"; texto = f"🟡 EMA50 ${ema50} abajo de EMA200 ${ema200} pero precio no confirma. ESPERA."
    return {"EMA50": ema50, "EMA200": ema200, "precio": round(precio_actual,2), "cruce": cruce, "senal_ema": senal, "texto": texto, "velas_grafico": datos["velas"], "vela_1h": vela_txt, "vela_4h": vela_txt}

def load(n, d):
    try:
        if os.path.exists(n):
            return json.load(open(n))
    except: pass
    return d
def save(n, d):
    try: json.dump(d, open(n, "w"))
    except: pass

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
    if i <= 15: rol = "ZONA - Toca y rebota"
    elif i <= 30: rol = "DIVISAS ZONA"
    elif i <= 45: rol = "BITCOIN ZONA"
    elif i <= 60: rol = "BINANCE"
    elif i <= 70: rol = "eTORO MT5"
    elif i <= 80: rol = "XTB COINBASE"
    elif i <= 90: rol = "APPLE TESLA ZONA"
    elif i <= 99: rol = "CAPITAL T212 ZONA"
    else: rol = "JEFE RAUDY ORO"
    CEREBROS.append({"id": i, "rol": rol, "estado": "VIVO", "jefe": "RAUDY ORO"})

ZONAS = {
    "ORO": {"c": 4100, "v": 4150},
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
    "ORO": "ORO 🥇", "EURUSD": "EUR/USD 💶", "GBPUSD": "GBP/USD 💷", "USDJPY": "USD/JPY 💴",
    "USDCHF": "USD/CHF 🇨🇭", "AUDUSD": "AUD/USD 🦘", "BTC": "BITCOIN ₿", "ETH": "ETHEREUM Ξ",
    "AAPL": "APPLE 🍎", "TSLA": "TESLA 🚗", "NVDA": "NVIDIA 💚", "MSFT": "MICROSOFT 🪟",
    "AMZN": "AMAZON 📦", "META": "META 👍", "GOOGL": "GOOGLE 🔍", "NFLX": "NETFLIX 🎬", "AMD": "AMD 🔴"
}
def yahoo(s, fb):
    try:
        u = "https://query1.finance.yahoo.com/v8/finance/chart/" + s
        r = requests.get(u, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        j = r.json()
        v = j["chart"]["result"][0]["meta"]
        return float(v["regularMarketPrice"])
    except: return fb
def oro_real():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=4)
        return float(r.json().get("price", 4118))
    except: return yahoo("GC=F", 4118)
def precio_binance():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=4)
        return float(r.json().get("price", 98000))
    except: return yahoo("BTC-USD", 98000)
def precio_coinbase():
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=4)
        return float(r.json()["data"]["amount"])
    except: return yahoo("BTC-USD", 98000)
def todos_precios():
    oro = oro_real(); btc_b = precio_binance(); btc_c = precio_coinbase()
    return {"ORO": oro, "EURUSD": yahoo("EURUSD=X", 1.1150), "GBPUSD": yahoo("GBPUSD=X", 1.2750), "USDJPY": yahoo("USDJPY=X", 149.5), "USDCHF": yahoo("USDCHF=X", 0.8850), "AUDUSD": yahoo("AUDUSD=X", 0.6550), "BTC": btc_b, "BTC_COINBASE": btc_c, "BTC_BINANCE": btc_b, "ETH": yahoo("ETH-USD", 3400), "AAPL": yahoo("AAPL", 262), "TSLA": yahoo("TSLA", 340), "NVDA": yahoo("NVDA", 185), "MSFT": yahoo("MSFT", 495), "AMZN": yahoo("AMZN", 235), "META": yahoo("META", 645), "GOOGL": yahoo("GOOGL", 282), "NFLX": yahoo("NFLX", 765), "AMD": yahoo("AMD", 125), "DXY": yahoo("DX-Y.NYB", 99.5), "VIX": yahoo("^VIX", 15.2)}
def zona_analiza(activo, precio, precios):
    z = ZONAS[activo]; zc = z["c"]; zv = z["v"]; rango = zv - zc; tol = rango * 0.15
    pos = (precio - zc) / rango * 100 if rango != 0 else 50
    pos = max(0, min(100, pos))
    if abs(precio - zc) <= tol:
        ZONA_H["toques_c"] += 1; msg = "🟢 ZONA ABAJO TOCADA - " + NOMBRES[activo] + " COMPRA YA"; tipo = "ZONA_COMPRA"; accion = "COMPRA"; tp = precio + rango * 0.8; sl = precio - rango * 0.2
    elif abs(precio - zv) <= tol:
        ZONA_H["toques_v"] += 1; msg = "🔴 ZONA ARRIBA TOCADA - " + NOMBRES[activo] + " VENTA YA"; tipo = "ZONA_VENTA"; accion = "VENTA"; tp = precio - rango * 0.8; sl = precio + rango * 0.2
    elif precio < zc:
        msg = "🔴 " + NOMBRES[activo] + " ABAJO DE ZONA - Espera"; tipo = "DEBAJO_ZONA"; accion = "ESPERA_BARREDOR"; tp = zc + rango * 0.8; sl = zc - rango * 0.2
    elif precio > zv:
        msg = "🔴 " + NOMBRES[activo] + " ARRIBA DE ZONA - Espera"; tipo = "ENCIMA_ZONA"; accion = "ESPERA"; tp = zv - rango * 0.8; sl = zv + rango * 0.2
    else:
        msg = "🟡 " + NOMBRES[activo] + " en MEDIO - ESPERA"; tipo = "MEDIO"; accion = "ESPERA"; tp = zc; sl = zv
    ZONA_H["u"] = msg; ZONA_H["h"].append({"hora": datetime.now().strftime("%H:%M"), "a": activo, "p": precio, "t": tipo}); ZONA_H["h"] = ZONA_H["h"][-20:]; save("zona.json", ZONA_H)
    return {"activo": activo, "precio": precio, "zona_abajo": zc, "zona_arriba": zv, "posicion": round(pos, 1), "mensaje": msg, "tipo": tipo, "accion": accion, "tp_zona": round(tp, 4), "sl_zona": round(sl, 4)}
def zona_todos(precios):
    out = {}
    for a in ZONAS:
        if a in precios: out[a] = zona_analiza(a, precios[a], precios)
    return out
def aprende(oro, orden):
    if "COMPRA" in orden or oro <= 4100: MEM["c"] += 1; dec = "COMPRA"
    elif "VENTA" in orden or oro >= 4150: MEM["v"] += 1; dec = "VENTA"
    else: MEM["e"] += 1; dec = "ESPERA"
    MEM["l"] = f"ORO en {oro}. Me acuerdo jefe."; MEM["h"].append({"hora": datetime.now().strftime("%H:%M"), "oro": oro, "d": dec}); MEM["h"] = MEM["h"][-20:]; save("mem.json", MEM)
def m5_aprende(p):
    M5["v"].append({"hora": datetime.now().strftime("%H:%M"), "p": p}); M5["v"] = M5["v"][-20:]
    if len(M5["v"]) >= 3:
        a = M5["v"][-3]["p"]; b = M5["v"][-2]["p"]; c = M5["v"][-1]["p"]
        if c > b > a: M5["s"] += 1; M5["b"] = 0; M5["u"] = f"M5 subio {a}>{b}>{c}"
        elif c < b < a: M5["b"] += 1; M5["s"] = 0; M5["u"] = f"M5 bajo {a}>{b}>{c}"
        else: M5["u"] = f"M5 en {c} mezclado. ESPERA."
    save("m5.json", M5)
def plat_aprende(key, pc, pr, nombre, archivo):
    D = PLATS[key]
    if pc > 10000:
        if pc <= 95000: D["b"] += 1; lec = nombre + " BARATO BTC $" + str(pc)
        elif pc >= 108000: D["c"] += 1; lec = nombre + " CARO BTC $" + str(pc)
        else: lec = nombre + " MEDIO BTC $" + str(pc)
    else:
        if pc >= 4150: D["c"] += 1; lec = nombre + " CARO ORO $" + str(pc)
        elif pc <= 4100: D["b"] += 1; lec = nombre + " BARATO ORO $" + str(pc)
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
def chat_robot(msg, precios, zonas):
    m = msg.lower(); nums = re.findall(r"\d+\.?\d*", msg); activo = busca_activo(m); precio = precios.get(activo, 4118); nombre = NOMBRES.get(activo, activo); z = zonas.get(activo, {}); lote = 0.01; ganar = 5.0; perder = 2.0
    if "0.02" in msg: lote = 0.02
    if "0.05" in msg: lote = 0.05
    if "0.1" in msg: lote = 0.1
    if "ganar" in m and len(nums) >= 2:
        try: ganar = float(nums[-2]); perder = float(nums[-1])
        except: pass
    if "hola" in m: return "Hola jefe RAUDY ORO. 100 cerebros ZONA en vivo. Dime: compro 0.01 bitcoin para ganar 5 y perder 2 o dime: zona oro"
    if "zona" in m: return "ZONA " + nombre + ": " + z.get("mensaje", "") + " | TP ZONA " + str(z.get("tp_zona")) + " SL ZONA " + str(z.get("sl_zona"))
    if "binance" in m: return "BINANCE jefe: BTC $" + str(precios["BTC_BINANCE"]) + ". " + PLATS["BINANCE"]["u"]
    if "compr" in m:
        if "ganar" in m or "gana" in m or "perder" in m:
            entrada = ZONAS[activo]["c"] if precio > ZONAS[activo]["c"] else precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "COMPRA", activo)
            return f"Jefe ZONA: COMPRA {nombre} {lote} en ZONA ${round(entrada,4)} TP {round(tp,4)} ganas ${ganar} SL {round(sl,4)} pierdes ${perder}. {z.get('mensaje','')}"
        return "Dime: compro 0.01 bitcoin para ganar 5 y perder 2"
    if "vend" in m:
        if "ganar" in m or "perder" in m:
            entrada = ZONAS[activo]["v"] if precio < ZONAS[activo]["v"] else precio
            tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, "VENTA", activo)
            return f"Jefe ZONA: VENTA {nombre} {lote} en ZONA ${round(entrada,4)} TP {round(tp,4)} ganas ${ganar} SL {round(sl,4)} pierdes ${perder}"
        return "VENTA " + nombre + " en ZONA $" + str(ZONAS[activo]["v"])
    return f"Te entendi jefe: {msg}. {nombre} ${precio}. {z.get('mensaje','')}"

# ===== ROBOT AUTOMATICO - CORRE SOLO EN SEGUNDO PLANO =====
ROBOT_LOG = {"ultimo": "Robot esperando...", "operaciones": 0}
def robot_auto_loop():
    print("ROBOT AUTO PRENDIDO JEFE")
    while True:
        try:
            session = get_session()
            if not session:
                ROBOT_LOG["ultimo"] = "Sin llaves Bybit - Solo modo señales"
                time.sleep(60); continue
            # Ver si ya tengo posicion abierta
            try:
                pos = session.get_positions(category="linear", symbol="XAUUSDT")
                tiene = any(float(p['size']) > 0 for p in pos['result']['list'])
            except: tiene = False
            if tiene:
                ROBOT_LOG["ultimo"] = "Ya tengo una abierta, ESPERA"
                time.sleep(3600); continue
            # Precio real Bybit
            try:
                r = session.get_tickers(category="linear", symbol="XAUUSDT")
                precio = float(r['result']['list'][0]['lastPrice'])
            except:
                precio = oro_real()
            ema = get_ema_oro()
            print(f"Robot chequeando Oro: {precio} EMA: {ema.get('senal_ema')}")
            # ZONA NUEVA 4100 / 4150
            if precio < 4100 and ema.get("senal_ema") == "COMPRA":
                print(f"COMPRA AUTO {precio}")
                session.place_order(category="linear", symbol="XAUUSDT", side="Buy", orderType="Market", qty=0.01, takeProfit=precio+5, stopLoss=precio-5)
                ROBOT_LOG["ultimo"] = f"COMPRA AUTO en {precio}"; ROBOT_LOG["operaciones"] += 1
            elif precio > 4150 and ema.get("senal_ema") == "VENTA":
                print(f"VENTA AUTO {precio}")
                session.place_order(category="linear", symbol="XAUUSDT", side="Sell", orderType="Market", qty=0.01, takeProfit=precio-5, stopLoss=precio+5)
                ROBOT_LOG["ultimo"] = f"VENTA AUTO en {precio}"; ROBOT_LOG["operaciones"] += 1
            else:
                ROBOT_LOG["ultimo"] = f"ESPERA - Oro {precio} - EMA {ema.get('cruce')}"
        except Exception as e:
            print(f"Robot error: {e}"); ROBOT_LOG["ultimo"] = f"Error: {e}"
        time.sleep(3600)

# Prender robot en hilo aparte, no rompe la pagina
threading.Thread(target=robot_auto_loop, daemon=True).start()

HTML = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY VIP ZONA + BYBIT</title><style>body{background:#050505;color:#fff;font-family:Arial;text-align:center;margin:0}header{background:#FFD700;color:#000;padding:15px}.box{margin:10px;padding:15px;border-radius:15px;border:3px solid #FFD700}input,select{width:100%;padding:12px;margin:4px 0;border-radius:10px;background:#111;color:#fff}button{width:100%;padding:14px;border-radius:15px;font-weight:bold;margin-top:5px;cursor:pointer}.btn-compra{background:#00FF88}.btn-venta{background:#FF4444;color:#fff}</style></head><body><header><h1>👑 RAUDY VIP ZONA ⚡</h1><p>JEFE: RAUDY ORO - ZONA + BYBIT AUTO</p><p id="vivo">🟢 EN VIVO...</p></header><div class="box"><h2>💰 BYBIT - JEFE RAUDY</h2><p id="bybit-estado">🔌 Verificando...</p><p id="robot-estado">🤖 Robot: Cargando...</p><a href="https://www.bybit.com" target="_blank" style="display:inline-block;padding:12px 20px;background:#F7A600;color:#000;font-weight:bold;border-radius:25px;text-decoration:none">🟡 ABRIR BYBIT</a></div><div class="box"><h2>📈 EMA + ZONA</h2><p id="ema-texto">Cargando...</p><p id="final-senal">Calculando...</p><p id="zonaOro">Cargando ZONA...</p></div><div class="box"><h2>💬 CHAT</h2><input id="chat" placeholder="Ej: zona oro o compro 0.01 para ganar 5 y perder 2"><button onclick="enviarChat()" style="background:#FFD700">💬 ENVIAR</button><p id="chatR" style="background:#111;padding:12px;border-radius:10px;text-align:left">🤖 Hola jefe...</p></div><div class="box"><h2>🟢🔴 OPERAR</h2><select id="opAct"><option value="ORO">ORO 🥇</option><option value="BTC">BITCOIN ₿</option><option value="EURUSD">EUR/USD 💶</option></select><input id="opLote" type="number" value="0.01" step="0.01"><input id="opGanar" type="number" value="5"><input id="opPerder" type="number" value="2"><button class="btn-compra" onclick="operarBtn('COMPRA')">🟢 COMPRAR</button><button class="btn-venta" onclick="operarBtn('VENTA')">🔴 VENDER</button><p id="opRes">👆 Elige y pulsa.</p></div><p>RAUDY VIP 2026 - No es consejo financiero, es educación</p><script>async function enviarChat(){let t=document.getElementById('chat').value;if(!t)return;document.getElementById('chatR').innerHTML='Pensando...';let r=await fetch('/api/chat?msg='+encodeURIComponent(t));let d=await r.json();document.getElementById('chatR').innerHTML='🤖 '+d.respuesta}async function operarBtn(lado){let act=document.getElementById('opAct').value;let lote=parseFloat(document.getElementById('opLote').value);let ganar=parseFloat(document.getElementById('opGanar').value);let perder=parseFloat(document.getElementById('opPerder').value);document.getElementById('opRes').innerHTML='Calculando...';let r=await fetch('/api/operar?activo='+act+'&lado='+lado+'&lote='+lote+'&ganar='+ganar+'&perder='+perder);let d=await r.json();document.getElementById('opRes').innerHTML=d.respuesta}async function up(){try{let r=await fetch('/api/satelite_usa?v='+Date.now());let d=await r.json();document.getElementById('vivo').innerHTML='EN VIVO '+d.hora+' - ORO $'+d.ORO;if(d.bybit)document.getElementById('bybit-estado').innerHTML=d.bybit.mensaje;if(d.robot)document.getElementById('robot-estado').innerHTML='🤖 Robot: '+d.robot.ultimo+' | Operaciones: '+d.robot.operaciones;if(d.ema)document.getElementById('ema-texto').innerHTML=d.ema.texto;if(d.senal_final)document.getElementById('final-senal').innerHTML=d.senal_final.senal_final+' - '+d.senal_final.motivo;if(d.zonas)document.getElementById('zonaOro').innerHTML=d.zonas.ORO.mensaje;}catch(e){}}setInterval(up,5000);up();</script></body></html>"""

@app.route("/")
def home(): return HTML
@app.route("/api/satelite_usa")
def sat():
    d = todos_precios(); oro = d["ORO"]; btc = d["BTC"]; zonas = zona_todos(d); ema = get_ema_oro(); zona_oro_accion = zonas["ORO"]["accion"]; ema_senal = ema.get("senal_ema"); dxy = d.get("DXY", 99.5); vix = d.get("VIX", 15.2)
    if vix >= 30: senal_final = {"senal_final": "🛑 PAUSA - VIX PANICO", "motivo": f"VIX {vix} en panico."}; jefe_orden_txt = "🛑 PAUSA"
    elif zona_oro_accion == "COMPRA" and ema_senal == "COMPRA": senal_final = {"senal_final": "🟢 COMPRA FUERTE", "motivo": f"ZONA COMPRA + {ema['cruce']} + ORO ${oro}"}; jefe_orden_txt = "🟢 PERMISO - COMPRA"
    elif zona_oro_accion == "VENTA" and ema_senal == "VENTA": senal_final = {"senal_final": "🔴 VENTA FUERTE", "motivo": f"ZONA VENTA + {ema['cruce']} + ORO ${oro}"}; jefe_orden_txt = "🔴 PERMISO - VENTA"
    else: senal_final = {"senal_final": "🟡 ESPERA - NO HAY ACUERDO", "motivo": f"ZONA: {zona_oro_accion} | EMA: {ema['cruce']} | ORO ${oro}"}; jefe_orden_txt = "🟡 ESPERA"
    if oro <= 4100: orden = "COMPRA"
    elif oro >= 4150: orden = "VENTA"
    else: orden = "ESPERA"
    aprende(oro, orden); m5_aprende(oro)
    plat_aprende("CAPITAL", oro, oro, "Capital.com", "cap.json"); plat_aprende("T212", oro, oro, "Trading 212", "t212.json"); plat_aprende("BINANCE", btc, btc, "Binance", "bin.json"); plat_aprende("ETORO", oro, oro, "eToro", "eto.json"); plat_aprende("MT5", oro, oro, "MT5", "mt5.json"); plat_aprende("XTB", oro, oro, "XTB", "xtb.json"); plat_aprende("COINBASE", d["BTC_COINBASE"], btc, "Coinbase", "coin.json")
    jefe = {"orden": jefe_orden_txt, "mensaje": "JEFE RAUDY: " + senal_final["motivo"]}
    plats_out = {}
    for k in PLATS: plats_out[k] = {"mensaje": k + " - " + str(len(PLATS[k]["h"])) + " jugadas", "leccion": PLATS[k]["u"]}
    return jsonify({**d, "hora": datetime.now().strftime("%H:%M:%S"), "zonas": zonas, "zona_oro": zonas["ORO"], "ema": ema, "senal_final": senal_final, "bybit": check_bybit(), "robot": ROBOT_LOG, "cerebro": {"mensaje": "100 cerebros ZONA", "leccion": MEM["l"]}, "cerebro_m5": {"mensaje": "M5", "leccion": M5["u"]}, "plats": plats_out, "jefe": jefe, "cerebros": CEREBROS, "total_cerebros": 100})
@app.route("/api/chat")
def api_chat():
    msg = request.args.get("msg", ""); precios = todos_precios(); zonas = zona_todos(precios); r = chat_robot(msg, precios, zonas); return jsonify({"respuesta": r})
@app.route("/api/lote")
def api_lote():
    try:
        lote = float(request.args.get("lote", 0.01)); ganar = float(request.args.get("ganar", 5)); perder = float(request.args.get("perder", 2)); ent = float(request.args.get("entrada", 4100)); act = request.args.get("activo", "ORO")
        tp, sl, dt, ds = calc_lote(lote, ganar, perder, ent, "COMPRA", act)
        return jsonify({"respuesta": f"COMPRA {act} {lote} en {ent} TP {round(tp,4)} SL {round(sl,4)}", "tp": tp, "sl": sl})
    except: return jsonify({"respuesta": "Escribe lote 0.01 ganar 5 perder 2"})
@app.route("/api/operar")
def api_operar():
    try:
        act = request.args.get("activo", "ORO"); lado = request.args.get("lado", "COMPRA"); lote = float(request.args.get("lote", 0.01)); ganar = float(request.args.get("ganar", 5)); perder = float(request.args.get("perder", 2))
        precios = todos_precios(); zonas = zona_todos(precios); precio = precios.get(act, 4100); z = zonas.get(act, {}); ema = get_ema_oro()
        entrada = ZONAS[act]["c"] if lado == "COMPRA" and precio > ZONAS[act]["c"] else (ZONAS[act]["v"] if lado == "VENTA" and precio < ZONAS[act]["v"] else precio)
        tp, sl, dt, ds = calc_lote(lote, ganar, perder, entrada, lado, act)
        r = f"ORDEN PREPARADA - {lado} {NOMBRES.get(act, act)} Lote {lote}<br>Entrada: ${round(entrada,4)} | Ahora: ${round(precio,4)}<br>TP: ${round(tp,4)} ganas ${ganar} | SL: ${round(sl,4)} pierdes ${perder}<br>ZONA: {z.get('mensaje','')}<br>EMA: {ema.get('texto','')}"
        return jsonify({"respuesta": r, "tp": tp, "sl": sl, "entrada": entrada})
    except Exception as e: return jsonify({"respuesta": "Error jefe: " + str(e)})
@app.route("/api/ema")
def api_ema(): return jsonify(get_ema_oro())
@app.route("/api/bybit_status")
def api_bybit_status(): return jsonify(check_bybit())
@app.route("/api/robot_status")
def api_robot_status(): return jsonify(ROBOT_LOG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
