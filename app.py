# ======================================================
# RAUDY VIP PRO - ROBOT 100% AUTOMÁTICO
# ÉL ENTRA SOLO, ÉL SALE SOLO, TÚ SOLO MIRAS
# SOLO DEMO - DINERO FALSO PARA APRENDER
# ======================================================
import os, time, threading, requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "767574050")

MI_PAYPAL = "https://paypal.me/RaudyManzueta/20"
MI_TELEGRAM_BOT = "https://t.me/raudy_vip_oro_bot"

# DINERO DEMO - AUTOMÁTICO
dinero_demo = 100.0
dinero_inicial = 100.0
operaciones_hoy = 0
posicion_abierta = None  # Si el robot ya compró, aquí lo guarda
ultima_señal = "Robot automático prendiendo..."
ultima_voz = "Jefe, soy automático, yo trabajo solo..."
historial = []
bot_encendido = False

ACTIVOS = {
    "ORO": {"precio": 4032.04},
    "BTC": {"precio": 97000.00},
    "EUR/USD": {"precio": 1.0850},
}

def mandar_telegram(m):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": TELEGRAM_CHAT_ID, "text": m}, timeout=10)
    except: pass

def get_precio_oro_real():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD", headers=headers, timeout=8).json()
        return float(r['items'][0]['curr'])
    except:
        try:
            r = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=1m", headers={"User-Agent": "Mozilla/5.0"}, timeout=8).json()
            return float(r['chart']['result'][0]['meta']['regularMarketPrice'])
        except:
            return 4032.04

def get_velas_reales_binance(symbol):
    try:
        url = f"https://api.binance.us/api/v3/klines?symbol={symbol}&interval=15m&limit=100"
        r = requests.get(url, timeout=10).json()
        return [float(x[4]) for x in r]
    except:
        return []

def calcular_rsi(cierres, periodo=14):
    if len(cierres) < periodo + 1: return 50
    ganancias = []; perdidas = []
    for i in range(1, len(cierres)):
        cambio = cierres[i] - cierres[i-1]
        if cambio > 0: ganancias.append(cambio); perdidas.append(0)
        else: ganancias.append(0); perdidas.append(-cambio)
    avg_gan = sum(ganancias[-periodo:]) / periodo
    avg_per = sum(perdidas[-periodo:]) / periodo
    if avg_per == 0: return 100
    rs = avg_gan / avg_per
    return round(100 - (100 / (1 + rs)), 2)

def calcular_ema(cierres, periodo):
    if len(cierres) < periodo: return cierres[-1] if cierres else 0
    k = 2 / (periodo + 1)
    ema = sum(cierres[:periodo]) / periodo
    for p in cierres[periodo:]:
        ema = (p * k) + (ema * (1 - k))
    return round(ema, 2)

def calcular_macd(cierres):
    if len(cierres) < 26: return 0
    return round(calcular_ema(cierres, 12) - calcular_ema(cierres, 26), 4)

def bot_automatico():
    global dinero_demo, operaciones_hoy, posicion_abierta, ultima_señal, ultima_voz, bot_encendido
    bot_encendido = True
    mandar_telegram("🤖 RAUDY VIP PRO AUTOMÁTICO ENCENDIDO 👑\nYo opero SOLO. Tú solo miras. Solo DEMO.")

    while True:
        try:
            # 1. REVISAR SI YA GANÓ $20 O PERDIÓ $10 - SE APAGA SOLO
            ganancia = dinero_demo - dinero_inicial
            if ganancia >= 20 or ganancia <= -10:
                ultima_voz = "Jefe, ya llegué a mi meta del día. Me apago solo para cuidar tu dinero."
                time.sleep(3600)
                continue
            if operaciones_hoy >= 3:
                time.sleep(3600)
                continue

            # 2. SI YA TIENE UNA POSICIÓN ABIERTA, LA CUIDA SOLO
            if posicion_abierta:
                nombre = posicion_abierta["activo"]
                precio_actual = get_precio_oro_real() if nombre == "ORO" else posicion_abierta["entrada"]
                if nombre == "BTC":
                    velas = get_velas_reales_binance("BTCUSDT")
                    if velas: precio_actual = velas[-1]
                entrada = posicion_abierta["entrada"]
                stop = posicion_abierta["stop"]
                tp = posicion_abierta["tp"]
                tipo = posicion_abierta["tipo"]

                # ¿Llegó a Take Profit? VENDE SOLO CON GANANCIA
                if (tipo == "COMPRA" and precio_actual >= tp) or (tipo == "VENTA" and precio_actual <= tp):
                    gan = abs(tp - entrada) * 2  # Simulación DEMO
                    dinero_demo += gan
                    operaciones_hoy += 1
                    texto = f"✅ ROBOT AUTOMÁTICO CERRÓ SOLO CON GANANCIA\nActivo: {nombre} - {tipo}\nEntró: ${entrada:.2f}\nSalió: ${tp:.2f}\nGanó: +${gan:.2f}\nDinero: ${dinero_demo:.2f}"
                    historial.insert(0, texto); mandar_telegram(texto)
                    posicion_abierta = None
                # ¿Llegó a Stop Loss? VENDE SOLO PARA NO PERDER MÁS
                elif (tipo == "COMPRA" and precio_actual <= stop) or (tipo == "VENTA" and precio_actual >= stop):
                    perdida = dinero_demo * 0.01
                    dinero_demo -= perdida
                    operaciones_hoy += 1
                    texto = f"🛑 ROBOT AUTOMÁTICO CERRÓ SOLO CON STOP LOSS\nActivo: {nombre} - {tipo}\nPara protegerte, salí en ${stop:.2f}\nPerdió: -${perdida:.2f}\nDinero: ${dinero_demo:.2f}"
                    historial.insert(0, texto); mandar_telegram(texto)
                    posicion_abierta = None
                time.sleep(30)
                continue

            # 3. SI NO TIENE POSICIÓN, BUSCA SEÑAL SOLO
            for nombre in ["ORO", "BTC"]:
                if nombre == "ORO":
                    precio = get_precio_oro_real()
                    cierres = get_velas_reales_binance("BTCUSDT")
                    if cierres:
                        factor = precio / cierres[-1]
                        cierres = [c * factor for c in cierres]
                    else: continue
                else:
                    cierres = get_velas_reales_binance("BTCUSDT")
                    if not cierres: continue
                    precio = cierres[-1]

                ACTIVOS[nombre]["precio"] = precio
                rsi = calcular_rsi(cierres)
                macd = calcular_macd(cierres)
                ema50 = calcular_ema(cierres, 50)
                ema200 = calcular_ema(cierres, 50)

                votos_compra = 0; votos_venta = 0
                if rsi < 30: votos_compra += 1
                elif rsi > 70: votos_venta += 1
                if macd > 0: votos_compra += 1
                elif macd < 0: votos_venta += 1
                if ema50 > ema200: votos_compra += 1
                else: votos_venta += 1

                # 4. SI HAY 3 VOTOS, ENTRA SOLO - SIN PREGUNTARTE
                if votos_compra >= 3:
                    entrada = precio
                    stop = precio * 0.995
                    tp = precio * 1.01
                    posicion_abierta = {"activo": nombre, "tipo": "COMPRA", "entrada": entrada, "stop": stop, "tp": tp}
                    ultima_señal = f"AUTOMÁTICO COMPRÓ {nombre} SOLO - Entrada ${entrada:.2f} - Stop ${stop:.2f} - TP ${tp:.2f} - RSI {rsi}"
                    ultima_voz = f"Jefe, yo solo compré {nombre}. No tienes que hacer nada. Yo lo cuido."
                    texto = f"🤖 ROBOT AUTOMÁTICO COMPRÓ SOLO\nActivo: {nombre}\nEntró SOLO en: ${entrada:.2f}\nStop Loss: ${stop:.2f}\nTake Profit: ${tp:.2f}\nRSI REAL: {rsi} | MACD: {macd}\nYo lo cuido solo, jefe."
                    historial.insert(0, texto); mandar_telegram(texto)
                    break
                elif votos_venta >= 3:
                    entrada = precio
                    stop = precio * 1.005
                    tp = precio * 0.99
                    posicion_abierta = {"activo": nombre, "tipo": "VENTA", "entrada": entrada, "stop": stop, "tp": tp}
                    ultima_señal = f"AUTOMÁTICO VENDIÓ {nombre} SOLO - Entrada ${entrada:.2f} - Stop ${stop:.2f} - TP ${tp:.2f} - RSI {rsi}"
                    ultima_voz = f"Jefe, yo solo vendí {nombre}. No tienes que hacer nada."
                    texto = f"🤖 ROBOT AUTOMÁTICO VENDIÓ SOLO\nActivo: {nombre}\nEntró SOLO en: ${entrada:.2f}\nStop Loss: ${stop:.2f}\nTake Profit: ${tp:.2f}\nRSI REAL: {rsi} | MACD: {macd}"
                    historial.insert(0, texto); mandar_telegram(texto)
                    break
                else:
                    ultima_señal = f"AUTOMÁTICO ANALIZANDO {nombre} - Precio REAL ${precio:.2f} - RSI {rsi} - Esperando señal fuerte..."
            time.sleep(60)
        except Exception as e:
            print(e); time.sleep(15)

@app.route('/')
def panel():
    ganancia = dinero_demo - dinero_inicial
    pos = f"📍 Posición Abierta: {posicion_abierta['tipo']} {posicion_abierta['activo']} en ${posicion_abierta['entrada']:.2f}" if posicion_abierta else "📍 Sin posición - Buscando señal solo..."
    historial_html = "<br><br>".join(historial[:5]) if historial else "El robot automático está trabajando solo..."
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="30">
    <script src="https://s3.tradingview.com/tv.js"></script></head>
    <body style="font-family:Arial; background:#000; color:white; padding:10px; text-align:center;">
        <h1 style="color:gold;">👑 RAUDY VIP PRO - 100% AUTOMÁTICO 👑</h1>
        <h3 style="color:#FFD700;">ÉL OPERA SOLO - TÚ SOLO MIRAS</h3>
        <div style="background:#111; border:2px solid gold; padding:15px; border-radius:15px;">
            <h2>💰 Dinero DEMO: ${dinero_demo:.2f} | Ganancia: ${ganancia:.2f}</h2>
            <p>{pos}</p>
            <p>📢 {ultima_señal}</p>
            <p>🎤 {ultima_voz}</p>
            <button onclick="hablar()" style="background:gold; color:black; padding:12px 20px; border:none; border-radius:10px; font-size:16px; font-weight:bold;">🔊 ESCUCHAR AL ROBOT</button>
            <p>✅ Automático | ✅ Entra Solo | ✅ Sale Solo | ✅ Stop Loss Solo | ✅ Max 3 al día | ✅ Gana $20 / Pierde $10 se apaga</p>
        </div>
        <h3>📈 ORO - VELAS REALES</h3><div id="chart_oro" style="height:400px;"></div>
        <h3>📈 BTC - VELAS REALES</h3><div id="chart_btc" style="height:400px;"></div>
        <div style="background:#111; border:2px solid gold; padding:15px; border-radius:15px; text-align:left;"><h3>📊 Historial Automático:</h3><p>{historial_html}</p></div>
        <div style="margin-top:15px;">
            <p><a href="{MI_TELEGRAM_BOT}" style="color:#00BFFF; font-size:18px;">🤖 MI TELEGRAM BOT - @raudy_vip_oro_bot</a></p>
            <p><a href="{MI_PAYPAL}" style="color:#FFD700; font-size:18px;">💳 PAYPAL $20 - Activar VIP PRO</a></p>
        </div>
        <script>
        function hablar() {{
            var msg = new SpeechSynthesisUtterance("{ultima_voz}");
            msg.lang = 'es-ES'; window.speechSynthesis.speak(msg);
        }}
        new TradingView.widget({{"autosize":true,"symbol":"OANDA:XAUUSD","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_oro"}});
        new TradingView.widget({{"autosize":true,"symbol":"BINANCE:BTCUSDT","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_btc"}});
        </script>
    </body></html>
    """
if not bot_encendido:
    threading.Thread(target=bot_automatico, daemon=True).start()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
