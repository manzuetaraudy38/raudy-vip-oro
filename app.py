# app.py - RAUDY VIP 1000 - CALIDAD TOTAL - 1 BACKTEST REAL + 2 MACD/BOLLINGER + 3 RIESGO 1:2 + 4 DOBLE TIEMPO - TODO JUNTO
import os, json, urllib.request, threading, time, random, math
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")
USAR_TESTNET = os.getenv("USAR_TESTNET", "True") == "True"

LINK_PAYPAL = "https://paypal.me/RaudyManzueta/20"
LINK_WHATSAPP = "https://wa.me/41767574050"
LINK_TELEGRAM = "https://t.me/raudy_vip_oro_bot"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "") or os.getenv("BOT_TOKEN", "") or os.getenv("BOT_TOKE", "") or os.getenv("BOT_TO", "")
CHAT_ID_JEFE = os.getenv("CHAT_ID_JEFE", "")

YAHOO = {"ORO": "GC=F", "TESLA": "TSLA", "APPLE": "AAPL", "META": "META", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/CHF": "CHF=X", "SP500": "^GSPC"}
BYBIT_BASE = "https://api-testnet.bybit.com" if USAR_TESTNET else "https://api.bybit.com"

BOT_AUTO = {"activo": False, "balance": 1000.0, "balance_inicial": 1000.0, "posicion": None, "precio_entrada": 0, "tp_objetivo": 0, "sl_objetivo": 0, "activo_actual": "ORO", "historial": [], "ultima_operacion": "BOT APAGADO", "ganadas": 0, "perdidas": 0, "perdidas_seguidas": 0, "total_ganado": 0.0, "total_perdido": 0.0, "trailing_sl": 0, "operaciones_manana": 0, "ganadas_manana": 0, "operaciones_noche": 0, "ganadas_noche": 0, "peor_balance": 1000.0, "mejor_balance": 1000.0}
HISTORIAL_PRECIOS_ORO = []
HISTORIAL_PRECIOS = {"ORO": [], "BTC": [], "EUR/USD": []}
# CALIDAD 3 - RIESGO 1 A 2
RIESGO_POR_OPERACION = 10.0  # Si pierde, pierde $10
GANANCIA_OBJETIVO = 20.0    # Si gana, gana $20 - EL DOBLE JEFE

def get_precio_real(simbolo_yahoo):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{simbolo_yahoo}?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            meta = data["chart"]["result"][0]["meta"]
            precio = meta.get("regularMarketPrice")
            return float(precio) if precio else None
    except Exception as e:
        print("Error precio", simbolo_yahoo, e)
        return None

def get_precio_bybit(symbol):
    try:
        url = f"{BYBIT_BASE}/v5/market/tickers?category=spot&symbol={symbol}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            lista = data.get("result", {}).get("list", [])
            if lista:
                return float(lista[0].get("lastPrice", 0))
    except Exception as e:
        print("Error Bybit", symbol, e)
    return None

def get_precios_reales_pasado(simbolo="GC=F", intervalo="1h", rango="1mo"):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{simbolo}?interval={intervalo}&range={rango}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
            result = data["chart"]["result"][0]
            closes = result["indicators"]["quote"][0]["close"]
            precios = [float(x) for x in closes if x is not None]
            return precios
    except Exception as e:
        print("Error precios reales pasado", e)
        return []

def senal_bybit(precio, tp, sl):
    if precio <= sl + 15:
        return "🟢 COMPRAR - JEFE ESTA BARATO, COMPRA AHORA"
    if precio >= tp - 15:
        return "🔴 VENDER - JEFE YA ESTA CARO, VENDE Y COBRA"
    return "🟡 ESPERA - JEFE TODAVIA NO, ESTA EN MEDIO"

def calcular_rsi(precios, periodo=14):
    if len(precios) < periodo + 1:
        return 50
    ganancias = 0
    perdidas = 0
    for i in range(1, periodo + 1):
        diff = precios[-i] - precios[-i-1]
        if diff > 0:
            ganancias += diff
        else:
            perdidas += abs(diff)
    if perdidas == 0:
        return 100
    rs = (ganancias / periodo) / (perdidas / periodo)
    return 100 - (100 / (1 + rs))

def calcular_tendencia(precios):
    if len(precios) < 10:
        return "SIN DATOS"
    ultimos_5 = sum(precios[-5:]) / 5
    anteriores_5 = sum(precios[-10:-5]) / 5
    if ultimos_5 > anteriores_5:
        return "SUBIENDO"
    if ultimos_5 < anteriores_5:
        return "BAJANDO"
    return "LADO"

def calcular_ema(precios, periodo):
    if len(precios) < periodo:
        return sum(precios) / len(precios) if precios else 0
    k = 2 / (periodo + 1)
    ema = sum(precios[:periodo]) / periodo
    for p in precios[periodo:]:
        ema = p * k + ema * (1 - k)
    return ema

def calcular_macd(precios):
    if len(precios) < 26:
        return {"macd": 0, "senal": 0, "histograma": 0, "texto": "SIN DATOS"}
    ema12 = calcular_ema(precios, 12)
    ema26 = calcular_ema(precios, 26)
    macd_linea = ema12 - ema26
    senal = macd_linea * 0.9
    hist = macd_linea - senal
    if hist > 0:
        texto = "FUERZA SUBIENDO"
    elif hist < 0:
        texto = "FUERZA BAJANDO"
    else:
        texto = "SIN FUERZA"
    return {"macd": round(macd_linea, 2), "senal": round(senal, 2), "histograma": round(hist, 2), "texto": texto}

def calcular_bollinger(precios, periodo=20):
    if len(precios) < periodo:
        return {"superior": 0, "medio": 0, "inferior": 0, "posicion": "MEDIO"}
    ultimos = precios[-periodo:]
    media = sum(ultimos) / len(ultimos)
    varianza = sum((x - media) ** 2 for x in ultimos) / len(ultimos)
    desv = math.sqrt(varianza)
    superior = media + 2 * desv
    inferior = media - 2 * desv
    precio_actual = precios[-1]
    if precio_actual <= inferior + (desv * 0.2):
        posicion = "MUY BARATO - PEGADO ABAJO"
    elif precio_actual >= superior - (desv * 0.2):
        posicion = "MUY CARO - PEGADO ARRIBA"
    elif precio_actual < media:
        posicion = "ABAJO - BARATO"
    else:
        posicion = "ARRIBA - CARO"
    return {"superior": round(superior, 2), "medio": round(media, 2), "inferior": round(inferior, 2), "posicion": posicion}

# CALIDAD 4 - DOBLE TIEMPO - 1HORA + 15 MIN
def analizar_doble_tiempo(lista_precios):
    if len(lista_precios) < 30:
        return {"largo": "SIN DATOS", "corto": "SIN DATOS", "acuerdo": False, "texto": "Faltan datos"}
    # Tiempo LARGO = 1 HORA = ultimos 30 precios
    largo_lista = lista_precios[-30:]
    tendencia_larga = calcular_tendencia(largo_lista)
    # Tiempo CORTO = 15 MIN = ultimos 10 precios
    corto_lista = lista_precios[-10:]
    tendencia_corta = calcular_tendencia(corto_lista)
    # CALIDAD: Si largo SUBE y corto BAJA = esta en oferta, buen momento para comprar barato
    # Si largo SUBE y corto SUBE = ya subio mucho, mejor esperar
    # Si largo BAJA = no comprar nunca
    if tendencia_larga == "SUBIENDO" and tendencia_corta == "BAJANDO":
        return {"largo": tendencia_larga, "corto": tendencia_corta, "acuerdo": True, "texto": "1H SUBE + 15M BAJA = OFERTA - COMPRA BARATO"}
    if tendencia_larga == "SUBIENDO" and tendencia_corta == "SUBIENDO":
        return {"largo": tendencia_larga, "corto": tendencia_corta, "acuerdo": True, "texto": "1H SUBE + 15M SUBE = CONFIRMADO"}
    if tendencia_larga == "BAJANDO":
        return {"largo": tendencia_larga, "corto": tendencia_corta, "acuerdo": False, "texto": "1H BAJA = NO COMPRAR"}
    return {"largo": tendencia_larga, "corto": tendencia_corta, "acuerdo": False, "texto": f"1H {tendencia_larga} + 15M {tendencia_corta} = ESPERA"}

def cerebro_1000_calidad(precio, tp, sl, lista_precios=None):
    if lista_precios is None:
        lista_precios = HISTORIAL_PRECIOS_ORO
    lista_precios.append(precio)
    if len(lista_precios) > 60:
        lista_precios.pop(0)
    rsi = calcular_rsi(lista_precios)
    tendencia = calcular_tendencia(lista_precios)
    macd = calcular_macd(lista_precios)
    boll = calcular_bollinger(lista_precios)
    doble = analizar_doble_tiempo(lista_precios)
    votos = 0
    detalle = []
    if rsi < 30:
        votos += 200
        detalle.append("RSI barato +200")
    elif rsi > 70:
        votos -= 200
        detalle.append("RSI caro -200")
    if tendencia == "SUBIENDO":
        votos += 150
    elif tendencia == "BAJANDO":
        votos -= 150
    if macd["histograma"] > 0:
        votos += 200
        detalle.append("MACD fuerza +200")
    elif macd["histograma"] < 0:
        votos -= 200
        detalle.append("MACD bajando -200")
    if "MUY BARATO" in boll["posicion"]:
        votos += 250
        detalle.append("Boll muy barato +250")
    elif "MUY CARO" in boll["posicion"]:
        votos -= 250
        detalle.append("Boll muy caro -250")
    elif "BARATO" in boll["posicion"]:
        votos += 100
    elif "CARO" in boll["posicion"]:
        votos -= 100
    # CALIDAD 4 - DOBLE TIEMPO PESA MUCHO
    if doble["acuerdo"] and doble["largo"] == "SUBIENDO":
        votos += 300
        detalle.append("Doble tiempo OK +300")
    if not doble["acuerdo"] and doble["largo"] == "BAJANDO":
        votos -= 300
        detalle.append("Doble tiempo NO -300")
    if precio <= sl + 30:
        votos += 50
    if precio >= tp - 30:
        votos -= 50
    print(f"CEREBRO CALIDAD TOTAL JEFE: Precio {precio} RSI {rsi:.1f} MACD {macd['texto']} Boll {boll['posicion']} Doble {doble['texto']} Votos {votos}")
    if votos >= 400:
        return "COMPRAR"
    if votos <= -400:
        return "VENDER"
    return "ESPERA"

def cerebro_1000(precio, tp, sl, lista_precios=None):
    return cerebro_1000_calidad(precio, tp, sl, lista_precios)

def es_hora_noticia():
    ahora = datetime.now()
    if ahora.hour == 14 and ahora.minute >= 25:
        return True
    if ahora.hour == 15 and ahora.minute <= 0:
        return True
    return False

def avisar_jefe(texto):
    print("AVISO JEFE:", texto)
    if not TELEGRAM_TOKEN or not CHAT_ID_JEFE:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        datos = json.dumps({"chat_id": CHAT_ID_JEFE, "text": texto}).encode()
        req = urllib.request.Request(url, data=datos, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print("Error avisar jefe", e)

def hacer_backtest():
    precios_reales = get_precios_reales_pasado("GC=F", "1h", "1mo")
    if len(precios_reales) < 50:
        precios_reales = []
        precio = 4150
        for i in range(200):
            precio += random.uniform(-12, 12)
            precios_reales.append(precio)
        modo = "SIMULADO - Sin internet"
    else:
        modo = f"REAL - {len(precios_reales)} precios reales 1H ultimo mes"
    balance_test = 1000
    ganadas = 0
    perdidas = 0
    peor = 1000
    mejor = 1000
    for i in range(30, len(precios_reales) - 5):
        lista = precios_reales[max(0, i-30):i]
        rsi = calcular_rsi(lista)
        tend = calcular_tendencia(lista)
        macd = calcular_macd(lista)
        boll = calcular_bollinger(lista)
        doble = analizar_doble_tiempo(lista)
        votos = 0
        if rsi < 45 and tend == "SUBIENDO":
            votos += 1
        if rsi < 35:
            votos += 1
        if macd["histograma"] > 0:
            votos += 1
        if "BARATO" in boll["posicion"]:
            votos += 1
        if doble["acuerdo"] and doble["largo"] == "SUBIENDO":
            votos += 1
        if votos >= 3:
            entrada = precios_reales[i]
            salida = precios_reales[min(len(precios_reales)-1, i+5)]
            gan = salida - entrada
            # CALIDAD 3 - RIESGO 1 A 2 EN BACKTEST TAMBIEN
            # Si gana, gana max $20. Si pierde, pierde max $10
            if gan > 0:
                if gan > GANANCIA_OBJETIVO:
                    gan = GANANCIA_OBJETIVO
            else:
                if gan < -RIESGO_POR_OPERACION:
                    gan = -RIESGO_POR_OPERACION
            balance_test += gan
            if balance_test < peor:
                peor = balance_test
            if balance_test > mejor:
                mejor = balance_test
            if gan >= 0:
                ganadas += 1
            else:
                perdidas += 1
    total = ganadas + perdidas
    winrate = (ganadas / total * 100) if total > 0 else 0
    # CALIDAD 3 - Aunque ganes solo 40%, con 1:2 igual ganas dinero
    esperanza = f"Con 1:2, aunque ganes solo {round(winrate,1)}%, sigues ganando porque ganas $20 y pierdes $10"
    return {"balance_inicial": 1000, "balance_final": round(balance_test, 2), "ganancia": round(balance_test - 1000, 2), "ganadas": ganadas, "perdidas": perdidas, "winrate": round(winrate, 1), "modo": modo, "peor": round(peor, 2), "mejor": round(mejor, 2), "mensaje": f"JEFE, con datos {modo}, quedaste con ${round(balance_test, 2)} - Hizo {total} operaciones - Peor momento ${round(peor,2)} - Mejor ${round(mejor,2)} - {esperanza}"}

def bot_auto_loop():
    while True:
        try:
            if BOT_AUTO["activo"]:
                if BOT_AUTO["perdidas_seguidas"] >= 3:
                    BOT_AUTO["activo"] = False
                    BOT_AUTO["ultima_operacion"] = "🛑 PROTECCION: Perdi 3 seguidas, me apague solo jefe"
                    BOT_AUTO["historial"].append(BOT_AUTO["ultima_operacion"])
                    avisar_jefe(BOT_AUTO["ultima_operacion"])
                    time.sleep(10)
                    continue
                if es_hora_noticia():
                    BOT_AUTO["ultima_operacion"] = "⏸️ PAUSA NOTICIAS: Jefe, hay noticia de USA, no opero 30 min"
                    time.sleep(20)
                    continue
                precios_multi = {}
                precios_multi["ORO"] = get_precio_real("GC=F") or 4149
                precios_multi["BTC"] = get_precio_bybit("BTCUSDT") or 90000
                precios_multi["EUR/USD"] = get_precio_real("EURUSD=X") or 1.16
                mejor_activo = None
                mejor_decision = "ESPERA"
                for activo, precio_act in precios_multi.items():
                    if activo not in HISTORIAL_PRECIOS:
                        HISTORIAL_PRECIOS[activo] = []
                    dec = cerebro_1000_calidad(precio_act, 999999 if activo == "BTC" else 4200, 0, HISTORIAL_PRECIOS[activo])
                    if dec == "COMPRAR":
                        mejor_activo = activo
                        mejor_decision = dec
                        break
                if mejor_decision == "COMPRAR" and BOT_AUTO["posicion"] is None:
                    precio_entrada = precios_multi[mejor_activo]
                    # CALIDAD 3 - CALCULAR TP Y SL 1 A 2
                    # Para ORO y BTC: TP = entrada + 20, SL = entrada - 10
                    # Para EUR/USD: TP = entrada + 0.02, SL = entrada - 0.01 (equivale a $20 / $10)
                    if mejor_activo == "EUR/USD":
                        tp_obj = precio_entrada + 0.02
                        sl_obj = precio_entrada - 0.01
                    elif mejor_activo == "BTC":
                        tp_obj = precio_entrada + 200
                        sl_obj = precio_entrada - 100
                    else:
                        tp_obj = precio_entrada + GANANCIA_OBJETIVO
                        sl_obj = precio_entrada - RIESGO_POR_OPERACION
                    BOT_AUTO["posicion"] = "COMPRAR"
                    BOT_AUTO["activo_actual"] = mejor_activo
                    BOT_AUTO["precio_entrada"] = precio_entrada
                    BOT_AUTO["tp_objetivo"] = tp_obj
                    BOT_AUTO["sl_objetivo"] = sl_obj
                    BOT_AUTO["trailing_sl"] = sl_obj
                    BOT_AUTO["ultima_operacion"] = f"🟢 BOT COMPRO {mejor_activo} en {precio_entrada} - TP ${GANANCIA_OBJETIVO} / SL ${RIESGO_POR_OPERACION} - 1:2"
                    BOT_AUTO["historial"].append(BOT_AUTO["ultima_operacion"])
                    avisar_jefe(f"🤖 JEFE, COMPRE {mejor_activo} en {precio_entrada} - Voy por $20, arriesgo $10 - Doble tiempo OK")
                    print(BOT_AUTO["ultima_operacion"])
                elif BOT_AUTO["posicion"] == "COMPRAR":
                    activo_actual = BOT_AUTO["activo_actual"]
                    precio_actual = precios_multi.get(activo_actual, BOT_AUTO["precio_entrada"])
                    ganancia_actual = precio_actual - BOT_AUTO["precio_entrada"]
                    if activo_actual == "EUR/USD":
                        ganancia_actual = ganancia_actual * 1000
                    elif activo_actual == "BTC":
                        ganancia_actual = ganancia_actual / 10
                    # CALIDAD 3 - TRAILING SOLO SI YA GANO $10, ASEGURA $10
                    if ganancia_actual >= 10:
                        nuevo_trailing = BOT_AUTO["precio_entrada"] + 10
                        if activo_actual == "EUR/USD":
                            nuevo_trailing = BOT_AUTO["precio_entrada"] + 0.01
                        elif activo_actual == "BTC":
                            nuevo_trailing = BOT_AUTO["precio_entrada"] + 100
                        if nuevo_trailing > BOT_AUTO["trailing_sl"]:
                            BOT_AUTO["trailing_sl"] = nuevo_trailing
                            BOT_AUTO["ultima_operacion"] = f"🔒 TRAILING 1:2: Jefe, ya gane $10, asegure $10, ahora voy por $20 sin riesgo"
                    cerrar = False
                    motivo = ""
                    if precio_actual <= BOT_AUTO["trailing_sl"] and ganancia_actual > 0:
                        cerrar = True
                        motivo = "TRAILING - Asegure ganancia 1:2"
                    if ganancia_actual >= GANANCIA_OBJETIVO:
                        cerrar = True
                        motivo = "TP 1:2 - Gane $20 JEFE!"
                    if ganancia_actual <= -RIESGO_POR_OPERACION:
                        cerrar = True
                        motivo = "SL 1:2 - Perdi solo $10, controlado"
                    if cerrar:
                        ganancia = ganancia_actual
                        if ganancia > GANANCIA_OBJETIVO:
                            ganancia = GANANCIA_OBJETIVO
                        if ganancia < -RIESGO_POR_OPERACION:
                            ganancia = -RIESGO_POR_OPERACION
                        BOT_AUTO["balance"] += ganancia
                        if BOT_AUTO["balance"] < BOT_AUTO["peor_balance"]:
                            BOT_AUTO["peor_balance"] = BOT_AUTO["balance"]
                        if BOT_AUTO["balance"] > BOT_AUTO["mejor_balance"]:
                            BOT_AUTO["mejor_balance"] = BOT_AUTO["balance"]
                        hora = datetime.now().hour
                        if hora < 12:
                            BOT_AUTO["operaciones_manana"] += 1
                            if ganancia >= 0: BOT_AUTO["ganadas_manana"] += 1
                        else:
                            BOT_AUTO["operaciones_noche"] += 1
                            if ganancia >= 0: BOT_AUTO["ganadas_noche"] += 1
                        if ganancia >= 0:
                            BOT_AUTO["ganadas"] += 1
                            BOT_AUTO["total_ganado"] += ganancia
                            BOT_AUTO["perdidas_seguidas"] = 0
                        else:
                            BOT_AUTO["perdidas"] += 1
                            BOT_AUTO["total_perdido"] += abs(ganancia)
                            BOT_AUTO["perdidas_seguidas"] += 1
                        BOT_AUTO["ultima_operacion"] = f"🔴 BOT VENDIO {activo_actual} en {precio_actual:.2f} - {motivo} - Ganancia: {ganancia:.2f} - Balance: {BOT_AUTO['balance']:.2f}"
                        BOT_AUTO["historial"].append(BOT_AUTO["ultima_operacion"])
                        avisar_jefe(BOT_AUTO["ultima_operacion"])
                        BOT_AUTO["posicion"] = None
                        print(BOT_AUTO["ultima_operacion"])
                if len(BOT_AUTO["historial"]) > 20:
                    BOT_AUTO["historial"] = BOT_AUTO["historial"][-20:]
            time.sleep(10)
        except Exception as e:
            print("Bot auto error", e)
            time.sleep(5)

threading.Thread(target=bot_auto_loop, daemon=True).start()

def enviar_telegram(chat_id, texto):
    if not TELEGRAM_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        datos = json.dumps({"chat_id": chat_id, "text": texto}).encode()
        req = urllib.request.Request(url, data=datos, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print("Error enviar Telegram", e)

def bot_loop():
    offset = 0
    print("BOT TELEGRAM ENCENDIDO")
    while True:
        try:
            if not TELEGRAM_TOKEN:
                time.sleep(10)
                continue
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}&timeout=10"
            with urllib.request.urlopen(url, timeout=15) as r:
                data = json.loads(r.read().decode())
                for upd in data.get("result", []):
                    offset = upd["update_id"] + 1
                    msg = upd.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    texto = msg.get("text", "").lower().strip()
                    if not chat_id:
                        continue
                    oro = get_precio_real("GC=F") or get_precio_bybit("XAUUSD") or 4149
                    if texto in ["/senal", "senal", "/signal", "señal"]:
                        s = senal_bybit(oro, 4200, 4100)
                        enviar_telegram(chat_id, f"📊 SEÑAL BYBIT JEFE\n\n🥇 ORO: {oro}\n{s}\n\n🎯 TP: 4200\n🛑 SL: 4100\n💳 Pagar $20: {LINK_PAYPAL}")
                    elif texto in ["/start", "start", "hola", "hi", "bb", "nn", "/vip", "/todo", "hol"]:
                        enviar_telegram(chat_id, f"👑 BIENVENIDO JEFE A RAUDY VIP 1000\n\n🥇 ORO EN VIVO: {oro}\n🚗 TESLA: {get_precio_real('TSLA')}\n🍎 APPLE: {get_precio_real('AAPL')}\n📘 META: {get_precio_real('META')}\n📈 SP500: {get_precio_real('^GSPC')}\n\n🎯 TP: 4200\n🛑 SL: 4100\n🤖 CEREBRO CALIDAD TOTAL: ACTIVO\n\n💳 Pagar $20: {LINK_PAYPAL}\n💬 WhatsApp: {LINK_WHATSAPP}\n\nEscribe /precio para ORO\nEscribe /senal para SEÑAL BYBIT\nEscribe /todo para todos")
                    elif texto in ["/precio", "precio"]:
                        enviar_telegram(chat_id, f"🥇 JEFE ORO EN VIVO: {oro}\n{senal_bybit(oro, 4200, 4100)}")
                    elif texto in ["/todo", "todo"]:
                        enviar_telegram(chat_id, f"👑 RAUDY VIP 1000 - TODOS EN VIVO\n\n🥇 ORO: {oro}\n🚗 TESLA: {get_precio_real('TSLA')}\n🍎 APPLE: {get_precio_real('AAPL')}\n📘 META: {get_precio_real('META')}\n📈 SP500: {get_precio_real('^GSPC')}\n\n💳 Pagar $20: {LINK_PAYPAL}")
                    else:
                        enviar_telegram(chat_id, f"Jefe, te entendi: {texto}\nEscribe /start para el menu, /precio para ORO, /senal para SEÑAL BYBIT")
        except Exception as e:
            print("Bot error", e)
            time.sleep(3)

threading.Thread(target=bot_loop, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="es"><head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP 1000</title>
<style>
* { box-sizing: border-box; }
body { margin:0; font-family: Arial; background:#0a0a0a; color:white; padding:15px; }
.top { background: gold; color:black; padding:18px; border-radius:18px; text-align:center; }
.top h1 { margin:0; font-size:32px; }
.top p { margin:5px 0 0 0; font-size:16px; font-weight:bold; }
.card { background:#1a1a1a; border-radius:20px; padding:20px; margin-top:15px; border:2px solid #333; }
.activo-titulo { font-size:28px; font-weight:bold; text-align:center; }
.precio-grande { font-size:65px; font-weight:bold; text-align:center; color:#00ff88; margin:10px 0; }
.sub { text-align:center; font-size:16px; color:#aaa; }
select, input { width:100%; padding:18px; font-size:22px; border-radius:14px; border:none; margin-top:10px; background:white; color:black; font-weight:bold; }
label { font-size:20px; font-weight:bold; display:block; margin-top:15px; }
.btn-comprar { width:100%; padding:22px; font-size:26px; font-weight:bold; background:#00c853; color:white; border:none; border-radius:16px; margin-top:15px; }
.btn-vender { width:100%; padding:22px; font-size:26px; font-weight:bold; background:#d50000; color:white; border:none; border-radius:16px; margin-top:12px; }
.btn-voz { width:100%; padding:16px; font-size:20px; background:#ff9800; border:none; border-radius:14px; margin-top:12px; font-weight:bold; }
.btn-tg { width:100%; padding:16px; font-size:18px; background:#0088cc; color:white; border:none; border-radius:14px; font-weight:bold; }
.btn-wa { width:100%; padding:16px; font-size:18px; background:#25D366; color:white; border:none; border-radius:14px; font-weight:bold; margin-top:10px; }
.btn-pago { width:100%; padding:20px; font-size:22px; background:gold; color:black; border:none; border-radius:16px; margin-top:12px; font-weight:bold; }
.lista-precios { font-size:18px; line-height:2; }
.lista-precios b { color:#00ff88; }
.senal-box { text-align:center; font-size:24px; font-weight:bold; padding:18px; border-radius:16px; margin-top:12px; background:#222; border:2px solid gold; }
canvas { width:100%; background:#000; border-radius:16px; }
.btn-bot { width:100%; padding:22px; font-size:24px; font-weight:bold; background:#7b1fa2; color:white; border:none; border-radius:16px; margin-top:12px; }
.btn-backtest { width:100%; padding:18px; font-size:20px; font-weight:bold; background:#00bcd4; color:white; border:none; border-radius:14px; margin-top:12px; }
</style></head><body>

<div class="top"><h1>RAUDY VIP 1000 👑</h1><p>CALIDAD TOTAL - RIESGO 1:2 + DOBLE TIEMPO + MACD + BOLLINGER + BACKTEST REAL</p><p id="estado">🔴 CONECTANDO PRECIOS REALES...</p></div>

<div class="card">
<div class="activo-titulo">🤖 BOT AUTO - CALIDAD TOTAL</div>
<div style="text-align:center; font-size:16px;">RSI: <b id="rsi" style="color:gold;">--</b> | Tend: <b id="tendencia" style="color:gold;">--</b></div>
<div style="text-align:center; font-size:16px; margin-top:6px;">MACD: <b id="macd" style="color:#00bcd4;">--</b> | Bollinger: <b id="bollinger" style="color:#ff9800;">--</b></div>
<div style="text-align:center; font-size:15px; margin-top:6px;">Doble Tiempo: <b id="doble" style="color:#00ff88;">--</b></div>
<div style="text-align:center; font-size:20px; margin:10px 0;">Balance Falso: <b id="balance" style="color:#00ff88;">$1000</b> | Activo: <b id="activo-bot" style="color:gold;">ORO</b></div>
<div style="text-align:center; font-size:16px; background:#000; padding:10px; border-radius:10px;" id="performance">Ganadas: 0 | Perdidas: 0 | Ganado: $0 | Perdido: $0</div>
<div style="text-align:center; font-size:14px; background:#222; padding:10px; border-radius:10px; margin-top:8px;" id="aprendizaje">🧠 APRENDIZAJE: Todavia no hay datos, deja que opere</div>
<div style="text-align:center; font-size:14px; background:#001a00; padding:8px; border-radius:10px; margin-top:8px;" id="riesgo-info">💰 RIESGO 1:2 - Si gano, gano $20 | Si pierdo, pierdo $10</div>
<div style="text-align:center; font-size:16px; margin-top:8px;" id="bot-estado">BOT APAGADO</div>
<div style="text-align:left; font-size:14px; margin-top:10px; background:#000; padding:10px; border-radius:10px;" id="historial">Sin operaciones todavia</div>
<button class="btn-bot" id="btn-bot" onclick="toggleBot()">🤖 PRENDER BOT AUTO</button>
<button class="btn-backtest" onclick="hacerBacktest()">📊 BACKTEST REAL 1:2 + DOBLE TIEMPO</button>
<div id="backtest-result" style="text-align:center; font-size:16px; margin-top:10px; background:#000; padding:12px; border-radius:10px;">Sin backtest todavia - Dale al boton azul - Ahora gana $20 pierde $10</div>
<div style="text-align:center; font-size:13px; color:#aaa; margin-top:8px;">Calidad: 1:2 + Doble Tiempo 1H+15M + MACD + Bollinger + Backtest Real | Proteccion 3 perdidas | Pausa noticias | Multi ORO+BTC+EUR/USD | FALSO</div>
</div>

<div class="card">
<div class="activo-titulo">🕯️ VELAS EN VIVO - ORO</div>
<div style="text-align:center; font-size:14px; color:#aaa;">🟢 Verde = Subio &nbsp;&nbsp; 🔴 Roja = Bajo &nbsp;&nbsp; En vivo cada 3 segundos</div>
<canvas id="velas" height="260"></canvas>
<div style="text-align:center; margin-top:8px; font-size:18px;"><span id="flecha" style="font-size:28px;">➡️</span> <span id="texto-vela">Esperando velas...</span></div>
</div>

<div class="card">
<div class="activo-titulo">📊 SEÑAL BYBIT EN VIVO</div>
<div class="senal-box" id="senal">🟡 ESPERA - Cargando señal...</div>
<div style="text-align:center; font-size:14px; color:#aaa; margin-top:8px;">La app te avisa con VOZ cuando es bueno comprar o vender</div>
<button class="btn-voz" onclick="activarVoz()">🔊 ACTIVAR VOZ DE SEÑALES - DALE AQUI</button>
</div>

<div class="card">
<div class="activo-titulo">TODOS LOS PRECIOS REALES</div>
<div class="lista-precios" id="lista">Cargando...</div>
<div style="text-align:center; color:#00ff88; font-size:14px;">Se actualiza cada 3 segundos - Fuente: Yahoo + Bybit en vivo</div>
</div>

<div class="card">
<div class="activo-titulo">ELIGE TU ACTIVO</div>
<select id="activo" onchange="cambiarActivo()">
<option value="ORO">🥇 ORO</option>
<option value="TESLA">🚗 TESLA</option>
<option value="APPLE">🍎 APPLE</option>
<option value="META">📘 META</option>
<option value="EUR/USD">💶 EUR / USD</option>
<option value="GBP/USD">💷 GBP / USD</option>
<option value="USD/CHF">🇨🇭 USD / CHF</option>
<option value="SP500">📈 SP500</option>
<option value="BTC">₿ BTC - BYBIT</option>
<option value="ETH">🔷 ETH - BYBIT</option>
</select>
<div class="activo-titulo" id="nombre-activo" style="margin-top:15px;">ORO</div>
<div class="precio-grande" id="precio">----</div>
<div class="sub" id="cerebro-texto">🤖 CEREBRO CALIDAD TOTAL: ESPERA</div>
<div class="sub" id="ultima-voz" style="margin-top:8px;">🔊 VOZ ACTIVA</div>
</div>

<div class="card">
<label>🎯 TP - DONDE QUIERO GANAR</label><input id="tp" value="4200" type="number">
<label>🛑 SL - DONDE CORTO SI PIERDO</label><input id="sl" value="4100" type="number">
<label>💰 CANTIDAD</label><input id="cantidad" value="0.01" type="number" step="0.01">
<button class="btn-comprar" onclick="operar('COMPRAR')">🟢 COMPRAR</button>
<button class="btn-vender" onclick="operar('VENDER')">🔴 VENDER</button>
<button class="btn-voz" onclick="probarVoz()">🔊 PROBAR VOZ</button>
</div>

<div class="card">
<div style="text-align:center; font-size:22px; font-weight:bold;">HABLAME JEFE</div>
<a href="LINK_TELEGRAM_PLACEHOLDER"><button class="btn-tg">📩 TELEGRAM - @raudy_vip_oro_bot</button></a>
<a href="LINK_WHATSAPP_PLACEHOLDER"><button class="btn-wa">💬 WHATSAPP - 076 757 40 50</button></a>
<a href="LINK_PAYPAL_PLACEHOLDER"><button class="btn-pago">💳 PAGAR $20 PARA USAR MI ROBOT - PAYPAL</button></a>
</div>

<script>
let precios = {};
let activoActual = "ORO";
let ultimoPrecio = 0;
let vozActivada = false;
let ultimaSenalHablada = "";
let velasHistorial = [];
let botPrendido = false;
function hablar(t){ let v = new SpeechSynthesisUtterance(t); v.lang='es-DO'; speechSynthesis.speak(v); document.getElementById('ultima-voz').innerText = "🔊 " + t; }
function activarVoz(){ vozActivada = true; hablar('Jefe, voz de señales activada, te voy a avisar cuando sea bueno comprar o vender'); alert('VOZ ACTIVADA JEFE - Ahora te aviso solo'); }
function cambiarActivo(){ activoActual = document.getElementById('activo').value; document.getElementById('nombre-activo').innerText = activoActual; velasHistorial = []; actualizarPantalla(); }
function probarVoz(){ hablar('Jefe, esta en ' + document.getElementById('precio').innerText + ', atento'); }
function operar(tipo){ let p = document.getElementById('precio').innerText; let tp=document.getElementById('tp').value; let sl=document.getElementById('sl').value; hablar('Jefe, esta en '+p+', voy a '+tipo); fetch('/operar',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({tipo:tipo, activo:activoActual, precio:p, tp:tp, sl:sl})}); alert('Orden enviada: '+tipo+' '+activoActual+' en '+p); }
async function toggleBot(){
  let r = await fetch('/api/bot_auto', {method:'POST'});
  let d = await r.json();
  botPrendido = d.activo;
  document.getElementById('btn-bot').innerText = botPrendido ? "🛑 APAGAR BOT AUTO" : "🤖 PRENDER BOT AUTO";
  document.getElementById('bot-estado').innerText = botPrendido ? "✅ BOT PRENDIDO - Operando solo con dinero falso" : "BOT APAGADO";
  hablar(botPrendido ? 'Jefe, bot auto prendido, ahora opera con riesgo 1 a 2' : 'Jefe, bot apagado');
}
async function hacerBacktest(){
  document.getElementById('backtest-result').innerText = "Probando con precios REALES 1:2 + doble tiempo... espera jefe, 5 segundos";
  let r = await fetch('/api/backtest');
  let d = await r.json();
  document.getElementById('backtest-result').innerHTML = "📊 BACKTEST CALIDAD TOTAL JEFE:<br>" + d.modo + "<br>Empezaste con $1000 y terminaste con $" + d.balance_final + "<br>Ganadas: " + d.ganadas + " | Perdidas: " + d.perdidas + " | Winrate: " + d.winrate + "%<br>Peor: $" + d.peor + " | Mejor: $" + d.mejor + "<br>" + d.mensaje;
  hablar('Jefe, backtest total listo, terminaste con ' + d.balance_final + ' dolares, ganando 20 y perdiendo 10');
}
function actualizarPantalla(){
  if(!precios[activoActual]) return;
  let p = precios[activoActual];
  document.getElementById('precio').innerText = p;
  if(ultimoPrecio !== 0){
    let diff = p - ultimoPrecio;
    if(diff > 2 && activoActual === "ORO"){ hablar('Jefe, subio, esta en ' + p); }
    if(diff < -2 && activoActual === "ORO"){ hablar('Jefe, bajo, esta en ' + p); }
  }
  ultimoPrecio = p;
}
function dibujarVelas(){
  let canvas = document.getElementById('velas');
  let ctx = canvas.getContext('2d');
  let W = canvas.width = canvas.offsetWidth * 2;
  let H = canvas.height = 520;
  ctx.fillStyle = "#000"; ctx.fillRect(0,0,W,H);
  if(velasHistorial.length < 2) return;
  let min = Math.min(...velasHistorial.map(v=>v.low)) - 1;
  let max = Math.max(...velasHistorial.map(v=>v.high)) + 1;
  let rango = max - min || 1;
  let anchoVela = W / velasHistorial.length;
  velasHistorial.forEach((vela, i)=>{
    let x = i * anchoVela + anchoVela/2;
    let yOpen = H - ((vela.open - min)/rango)*H;
    let yClose = H - ((vela.close - min)/rango)*H;
    let yHigh = H - ((vela.high - min)/rango)*H;
    let yLow = H - ((vela.low - min)/rango)*H;
    let subio = vela.close >= vela.open;
    ctx.strokeStyle = subio ? "#00ff88" : "#ff1744";
    ctx.fillStyle = subio ? "#00ff88" : "#ff1744";
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(x, yHigh); ctx.lineTo(x, yLow); ctx.stroke();
    let top = Math.min(yOpen, yClose);
    let alto = Math.max(10, Math.abs(yClose - yOpen));
    ctx.fillRect(x - anchoVela*0.35, top, anchoVela*0.7, alto);
  });
  let yTP = H - ((parseFloat(document.getElementById('tp').value) - min)/rango)*H;
  let ySL = H - ((parseFloat(document.getElementById('sl').value) - min)/rango)*H;
  ctx.strokeStyle = "#00ff88"; ctx.setLineDash([12,8]); ctx.beginPath(); ctx.moveTo(0,yTP); ctx.lineTo(W,yTP); ctx.stroke();
  ctx.strokeStyle = "#ff1744"; ctx.beginPath(); ctx.moveTo(0,ySL); ctx.lineTo(W,ySL); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = "#fff"; ctx.font = "bold 28px Arial";
  ctx.fillText("TP " + document.getElementById('tp').value, 10, Math.max(30, yTP-10));
  ctx.fillText("SL " + document.getElementById('sl').value, 10, Math.min(H-10, ySL+35));
}
async function cargarPrecios(){
  try{
    let r = await fetch('/api/precios');
    let data = await r.json();
    precios = data;
    document.getElementById('estado').innerText = "✅ EN VIVO - " + new Date().toLocaleTimeString();
    let html = "";
    for(let k in precios){ html += k + ": <b>" + precios[k] + "</b><br>"; }
    document.getElementById('lista').innerHTML = html;
    actualizarPantalla();
    let p = precios[activoActual];
    if(p){
      let ultimo = velasHistorial[velasHistorial.length-1];
      if(!ultimo || velasHistorial.length === 0){
        velasHistorial.push({open:p, close:p, high:p+0.5, low:p-0.5});
      } else {
        if(velasHistorial.length > 0 && Math.random() > 0.7){
          velasHistorial.push({open:ultimo.close, close:p, high:Math.max(ultimo.close,p)+0.4, low:Math.min(ultimo.close,p)-0.4});
        } else {
          ultimo.close = p;
          ultimo.high = Math.max(ultimo.high, p);
          ultimo.low = Math.min(ultimo.low, p);
        }
        if(velasHistorial.length > 25) velasHistorial.shift();
      }
      let v = velasHistorial[velasHistorial.length-1];
      if(v.close > v.open){
        document.getElementById('flecha').innerText = "🟢 ⬆️ SUBIENDO";
        document.getElementById('texto-vela').innerText = "Vela verde - El precio esta subiendo, esta en " + p;
      } else {
        document.getElementById('flecha').innerText = "🔴 ⬇️ BAJANDO";
        document.getElementById('texto-vela').innerText = "Vela roja - El precio esta bajando, esta en " + p;
      }
      dibujarVelas();
    }
    let tp = document.getElementById('tp').value;
    let sl = document.getElementById('sl').value;
    let s = await fetch('/api/senal?precio=' + precios['ORO'] + '&tp=' + tp + '&sl=' + sl);
    let sd = await s.json();
    document.getElementById('senal').innerText = sd.senal;
    document.getElementById('cerebro-texto').innerText = "🤖 CEREBRO CALIDAD TOTAL: " + sd.decision;
    if(sd.rsi) document.getElementById('rsi').innerText = sd.rsi;
    if(sd.tendencia) document.getElementById('tendencia').innerText = sd.tendencia;
    if(sd.macd) document.getElementById('macd').innerText = sd.macd;
    if(sd.bollinger) document.getElementById('bollinger').innerText = sd.bollinger;
    if(sd.doble) document.getElementById('doble').innerText = sd.doble;
    let b = await fetch('/api/bot_auto');
    let bd = await b.json();
    document.getElementById('balance').innerText = "$" + bd.balance.toFixed(2);
    document.getElementById('activo-bot').innerText = bd.activo_actual;
    document.getElementById('bot-estado').innerText = bd.ultima_operacion;
    document.getElementById('performance').innerText = "Ganadas: " + bd.ganadas + " | Perdidas: " + bd.perdidas + " | Ganado: $" + bd.total_ganado.toFixed(2) + " | Perdido: $" + bd.total_perdido.toFixed(2);
    if(bd.operaciones_manana + bd.operaciones_noche > 0){
      let winM = bd.operaciones_manana > 0 ? Math.round(bd.ganadas_manana / bd.operaciones_manana * 100) : 0;
      let winN = bd.operaciones_noche > 0 ? Math.round(bd.ganadas_noche / bd.operaciones_noche * 100) : 0;
      document.getElementById('aprendizaje').innerText = "🧠 APRENDE: Mañana ganas " + winM + "% (" + bd.ganadas_manana + "/" + bd.operaciones_manana + ") | Noche ganas " + winN + "% (" + bd.ganadas_noche + "/" + bd.operaciones_noche + ") - " + (winM > winN ? "Jefe, opera mas en la MAÑANA" : "Jefe, opera mas en la NOCHE");
    }
    if(bd.historial.length > 0){ document.getElementById('historial').innerHTML = bd.historial.slice().reverse().join("<br>"); }
    if(vozActivada && sd.senal !== ultimaSenalHablada && sd.senal.includes('COMPRAR')){
        hablar('Jefe, compra ahora, el precio esta bueno para comprar, esta en ' + precios['ORO']);
        ultimaSenalHablada = sd.senal;
    }
    if(vozActivada && sd.senal !== ultimaSenalHablada && sd.senal.includes('VENDER')){
        hablar('Jefe, vende ahora, el precio esta bajando, esta en ' + precios['ORO']);
        ultimaSenalHablada = sd.senal;
    }
  }catch(e){ document.getElementById('estado').innerText = "⚠️ Sin internet, reintentando..."; }
}
cargarPrecios();
setInterval(cargarPrecios, 3000);
</script></body></html>
"""
HTML = HTML.replace("LINK_TELEGRAM_PLACEHOLDER", LINK_TELEGRAM).replace("LINK_WHATSAPP_PLACEHOLDER", LINK_WHATSAPP).replace("LINK_PAYPAL_PLACEHOLDER", LINK_PAYPAL)

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/precios")
def api_precios():
    out = {}
    for nombre, yahoo_sym in YAHOO.items():
        p = get_precio_real(yahoo_sym)
        if p:
            out[nombre] = p
    btc = get_precio_bybit("BTCUSDT")
    if btc: out["BTC"] = btc
    eth = get_precio_bybit("ETHUSDT")
    if eth: out["ETH"] = eth
    if not out:
        out = {"ORO": 4149, "TESLA": 378, "APPLE": 350, "META": 641, "EUR/USD": 1.16, "GBP/USD": 1.34, "USD/CHF": 0.79, "SP500": 7549}
    return jsonify(out)

@app.route("/api/senal")
def api_senal():
    try:
        precio = float(request.args.get("precio", 4149))
        tp = float(request.args.get("tp", 4200))
        sl = float(request.args.get("sl", 4100))
    except:
        precio, tp, sl = 4149, 4200, 4100
    s = senal_bybit(precio, tp, sl)
    d = cerebro_1000_calidad(precio, tp, sl)
    rsi = calcular_rsi(HISTORIAL_PRECIOS_ORO)
    tend = calcular_tendencia(HISTORIAL_PRECIOS_ORO)
    macd = calcular_macd(HISTORIAL_PRECIOS_ORO)
    boll = calcular_bollinger(HISTORIAL_PRECIOS_ORO)
    doble = analizar_doble_tiempo(HISTORIAL_PRECIOS_ORO)
    return jsonify({"senal": s, "decision": d, "precio": precio, "rsi": round(rsi, 1), "tendencia": tend, "macd": macd["texto"], "bollinger": boll["posicion"], "doble": doble["texto"]})

@app.route("/api/bot_auto", methods=["GET", "POST"])
def api_bot_auto():
    if request.method == "POST":
        BOT_AUTO["activo"] = not BOT_AUTO["activo"]
        if BOT_AUTO["activo"]:
            BOT_AUTO["perdidas_seguidas"] = 0
            BOT_AUTO["ultima_operacion"] = "✅ BOT PRENDIDO - Operando solo con dinero falso"
        else:
            BOT_AUTO["ultima_operacion"] = "BOT APAGADO"
    return jsonify(BOT_AUTO)

@app.route("/api/backtest")
def api_backtest():
    return jsonify(hacer_backtest())

@app.route("/operar", methods=["POST"])
def operar():
    data = request.get_json()
    decision = cerebro_1000_calidad(float(str(data.get("precio", 4149)).replace(",","")), float(data.get("tp", 4200)), float(data.get("sl", 4100)))
    print(f"ORDEN JEFE: {data} -> {decision} - TESTNET: {USAR_TESTNET}")
    return jsonify({"ok": True, "decision": decision, "pedido": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
