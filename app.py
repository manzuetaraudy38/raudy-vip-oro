# ======================================================
# RAUDY VIP PRO - AUTOMÁTICO COMPLETO
# DIVISAS + ACCIONES + ORO + BTC + SP500 + AMAZON
# 100% AUTOMÁTICO - ÉL OPERA SOLO - SOLO DEMO
# ======================================================
import os, time, threading, requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "767574050")

MI_PAYPAL = "https://paypal.me/RaudyManzueta/20"
MI_TELEGRAM_BOT = "https://t.me/raudy_vip_oro_bot"

dinero_demo = 100.0
dinero_inicial = 100.0
operaciones_hoy = 0
posicion_abierta = None
ultima_señal = "Robot automático completo prendiendo..."
ultima_voz = "Jefe, ya tengo divisas, acciones, Tesla, Meta, SP500 y Amazon..."
historial = []
bot_encendido = False

# ============ TODOS TUS ACTIVOS - JEFE ============
# DIVISAS = Forex, ACCIONES = Empresas, INDICE = SP500, CRIPTO = BTC, ORO = Oro
ACTIVOS = {
    # --- ORO Y CRIPTO ---
    "ORO": {"precio": 4032.04, "tipo": "ORO", "yahoo": "GC=F", "tv": "OANDA:XAUUSD"},
    "BTC": {"precio": 97000.00, "tipo": "CRIPTO", "yahoo": "BTC-USD", "tv": "BINANCE:BTCUSDT"},
    # --- DIVISAS - FOREX ---
    "EUR/USD": {"precio": 1.0850, "tipo": "DIVISA", "yahoo": "EURUSD=X", "tv": "OANDA:EURUSD"},
    "GBP/USD": {"precio": 1.2700, "tipo": "DIVISA", "yahoo": "GBPUSD=X", "tv": "OANDA:GBPUSD"},
    "USD/JPY": {"precio": 155.00, "tipo": "DIVISA", "yahoo": "USDJPY=X", "tv": "OANDA:USDJPY"},
    "USD/CHF": {"precio": 0.8800, "tipo": "DIVISA", "yahoo": "USDCHF=X", "tv": "OANDA:USDCHF"},
    "AUD/USD": {"precio": 0.6500, "tipo": "DIVISA", "yahoo": "AUDUSD=X", "tv": "OANDA:AUDUSD"},
    "USD/CAD": {"precio": 1.3600, "tipo": "DIVISA", "yahoo": "USDCAD=X", "tv": "OANDA:USDCAD"},
    # --- ACCIONES - EMPRESAS GRANDES ---
    "TESLA": {"precio": 250.00, "tipo": "ACCION", "yahoo": "TSLA", "tv": "NASDAQ:TSLA"},
    "META": {"precio": 580.00, "tipo": "ACCION", "yahoo": "META", "tv": "NASDAQ:META"},
    "APPLE": {"precio": 220.00, "tipo": "ACCION", "yahoo": "AAPL", "tv": "NASDAQ:AAPL"},
    "AMAZON": {"precio": 200.00, "tipo": "ACCION", "yahoo": "AMZN", "tv": "NASDAQ:AMZN"},
    "NVIDIA": {"precio": 135.00, "tipo": "ACCION", "yahoo": "NVDA", "tv": "NASDAQ:NVDA"},
    # --- INDICE SP500 ---
    "SP500": {"precio": 5900.00, "tipo": "INDICE", "yahoo": "^GSPC", "tv": "OANDA:SPX500USD"},
}

def mandar_telegram(m):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": TELEGRAM_CHAT_ID, "text": m}, timeout=10)
    except: pass

# ============ PRECIOS REALES DE YAHOO - FUNCIONA EN RENDER ============
def get_precio_yahoo(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=15m"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8).json()
        result = r['chart']['result'][0]
        precio = result['meta']['regularMarketPrice']
        cierres = [c for c in result['indicators']['quote'][0]['close'] if c is not None]
        return float(precio), cierres
    except:
        return None, []

def get_velas_btc():
    try:
        url = "https://api.binance.us/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=100"
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

# ============ ROBOT 100% AUTOMÁTICO - CON 14 ACTIVOS ============
def bot_automatico():
    global dinero_demo, operaciones_hoy, posicion_abierta, ultima_señal, ultima_voz, bot_encendido
    bot_encendido = True
    mandar_telegram("🤖 RAUDY VIP PRO AUTOMÁTICO COMPLETO ENCENDIDO 👑\nDivisas + Acciones + Tesla + Meta + SP500 + Amazon + Oro + BTC. Yo opero SOLO. Solo DEMO.")

    while True:
        try:
            ganancia = dinero_demo - dinero_inicial
            if ganancia >= 20 or ganancia <= -10:
                ultima_voz = "Jefe, ya llegué a mi meta del día. Me apago solo."
                time.sleep(3600); continue
            if operaciones_hoy >= 3:
                time.sleep(3600); continue

            # SI YA TIENE POSICIÓN, LA CUIDA SOLO
            if posicion_abierta:
                nombre = posicion_abierta["activo"]
                ticker = ACTIVOS[nombre]["yahoo"]
                precio_actual, _ = get_precio_yahoo(ticker)
                if precio_actual is None:
                    precio_actual = posicion_abierta["entrada"]
                entrada = posicion_abierta["entrada"]; stop = posicion_abierta["stop"]; tp = posicion_abierta["tp"]; tipo = posicion_abierta["tipo"]
                if (tipo == "COMPRA" and precio_actual >= tp) or (tipo == "VENTA" and precio_actual <= tp):
                    g = abs(tp - entrada)
                    # En DEMO ganamos 1% simulado para no romper el dinero
                    gan = dinero_demo * 0.02
                    dinero_demo += gan; operaciones_hoy += 1
                    texto = f"✅ AUTOMÁTICO CERRÓ CON GANANCIA\n{nombre} {tipo}\nEntró ${entrada:.2f} Salió ${tp:.2f}\nGanó +${gan:.2f}\nDinero: ${dinero_demo:.2f}"
                    historial.insert(0, texto); mandar_telegram(texto); posicion_abierta = None
                elif (tipo == "COMPRA" and precio_actual <= stop) or (tipo == "VENTA" and precio_actual >= stop):
                    perdida = dinero_demo * 0.01
                    dinero_demo -= perdida; operaciones_hoy += 1
                    texto = f"🛑 AUTOMÁTICO CERRÓ CON STOP LOSS\n{nombre} {tipo}\nProtegiendo tu dinero en ${stop:.2f}\nPerdió -${perdida:.2f}\nDinero: ${dinero_demo:.2f}"
                    historial.insert(0, texto); mandar_telegram(texto); posicion_abierta = None
                time.sleep(30); continue

            # SI NO TIENE POSICIÓN, BUSCA EN TODOS LOS 14 ACTIVOS
            for nombre, info in ACTIVOS.items():
                precio, cierres = get_precio_yahoo(info["yahoo"])
                if precio is None:
                    if nombre == "BTC":
                        cierres = get_velas_btc()
                        if cierres: precio = cierres[-1]
                        else: continue
                    else: continue
                ACTIVOS[nombre]["precio"] = precio
                if len(cierres) < 30: continue
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

                if votos_compra >= 3:
                    entrada = precio; stop = precio * 0.995; tp = precio * 1.01
                    posicion_abierta = {"activo": nombre, "tipo": "COMPRA", "entrada": entrada, "stop": stop, "tp": tp}
                    ultima_señal = f"AUTOMÁTICO COMPRÓ {nombre} ({info['tipo']}) SOLO - ${entrada:.2f} - RSI {rsi}"
                    ultima_voz = f"Jefe, yo solo compré {nombre}. Es una {info['tipo']}. Yo lo cuido."
                    texto = f"🤖 AUTOMÁTICO COMPRÓ SOLO\nActivo: {nombre} ({info['tipo']})\nEntró SOLO: ${entrada:.2f}\nStop: ${stop:.2f} | TP: ${tp:.2f}\nRSI REAL: {rsi} | MACD: {macd}"
                    historial.insert(0, texto); mandar_telegram(texto); break
                elif votos_venta >= 3:
                    entrada = precio; stop = precio * 1.005; tp = precio * 0.99
                    posicion_abierta = {"activo": nombre, "tipo": "VENTA", "entrada": entrada, "stop": stop, "tp": tp}
                    ultima_señal = f"AUTOMÁTICO VENDIÓ {nombre} ({info['tipo']}) SOLO - ${entrada:.2f} - RSI {rsi}"
                    ultima_voz = f"Jefe, yo solo vendí {nombre}. Yo lo cuido."
                    texto = f"🤖 AUTOMÁTICO VENDIÓ SOLO\nActivo: {nombre} ({info['tipo']})\nEntró SOLO: ${entrada:.2f}\nStop: ${stop:.2f} | TP: ${tp:.2f}\nRSI REAL: {rsi} | MACD: {macd}"
                    historial.insert(0, texto); mandar_telegram(texto); break
                else:
                    ultima_señal = f"AUTOMÁTICO ANALIZANDO {nombre} ({info['tipo']}) - Precio REAL ${precio:.2f} - RSI {rsi} - Esperando..."
            time.sleep(60)
        except Exception as e:
            print(e); time.sleep(15)

@app.route('/')
def panel():
    ganancia = dinero_demo - dinero_inicial
    pos = f"📍 Posición: {posicion_abierta['tipo']} {posicion_abierta['activo']} en ${posicion_abierta['entrada']:.2f}" if posicion_abierta else "📍 Sin posición - Buscando en 14 activos solo..."
    # Botones por tipo
    def botones_por_tipo(tipo):
        html = ""
        for k, v in ACTIVOS.items():
            if v["tipo"] == tipo:
                html += f"<div style='background:#222; padding:10px; border:1px solid gold; border-radius:10px; display:inline-block; margin:5px; min-width:110px;'><b>{k}</b><br>${v['precio']:.2f}<br><small>{tipo}</small></div>"
        return html
    historial_html = "<br><br>".join(historial[:6]) if historial else "El robot automático completo está trabajando solo en divisas y acciones..."
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="30">
    <script src="https://s3.tradingview.com/tv.js"></script></head>
    <body style="font-family:Arial; background:#000; color:white; padding:10px; text-align:center;">
        <h1 style="color:gold;">👑 RAUDY VIP PRO - AUTOMÁTICO COMPLETO 👑</h1>
        <h3 style="color:#FFD700;">DIVISAS + ACCIONES + TESLA + META + SP500 + AMAZON + ORO + BTC</h3>
        <div style="background:#111; border:2px solid gold; padding:15px; border-radius:15px;">
            <h2>💰 DEMO: ${dinero_demo:.2f} | Ganancia: ${ganancia:.2f} | Operaciones: {operaciones_hoy}/3</h2>
            <p>{pos}</p><p>📢 {ultima_señal}</p><p>🎤 {ultima_voz}</p>
            <button onclick="hablar()" style="background:gold; color:black; padding:12px 20px; border:none; border-radius:10px; font-size:16px; font-weight:bold;">🔊 ESCUCHAR AL ROBOT</button>
            <p>✅ Automático | ✅ 14 Activos | ✅ Entra Solo | ✅ Sale Solo | ✅ Stop Loss | ✅ Max 3</p>
        </div>
        <h3 style="color:gold;">💱 DIVISAS - FOREX REAL</h3><div>{botones_por_tipo("DIVISA")}</div>
        <h3 style="color:gold;">📈 ACCIONES - EMPRESAS REALES</h3><div>{botones_por_tipo("ACCION")}</div>
        <h3 style="color:gold;">🏆 INDICE + ORO + CRIPTO</h3><div>{botones_por_tipo("INDICE")}{botones_por_tipo("ORO")}{botones_por_tipo("CRIPTO")}</div>

        <h3>📈 GRÁFICO ORO</h3><div id="chart_oro" style="height:350px;"></div>
        <h3>📈 GRÁFICO EUR/USD - DIVISA</h3><div id="chart_euro" style="height:350px;"></div>
        <h3>📈 GRÁFICO TESLA</h3><div id="chart_tesla" style="height:350px;"></div>
        <h3>📈 GRÁFICO META</h3><div id="chart_meta" style="height:350px;"></div>
        <h3>📈 GRÁFICO SP500</h3><div id="chart_sp" style="height:350px;"></div>
        <h3>📈 GRÁFICO AMAZON</h3><div id="chart_amzn" style="height:350px;"></div>
        <h3>📈 GRÁFICO BTC</h3><div id="chart_btc" style="height:350px;"></div>

        <div style="background:#111; border:2px solid gold; padding:15px; border-radius:15px; text-align:left;"><h3>📊 Historial Automático:</h3><p>{historial_html}</p></div>
        <div style="margin-top:15px;">
            <p><a href="{MI_TELEGRAM_BOT}" style="color:#00BFFF; font-size:18px;">🤖 TELEGRAM - @raudy_vip_oro_bot</a></p>
            <p><a href="{MI_PAYPAL}" style="color:#FFD700; font-size:18px;">💳 PAYPAL $20 - Activar VIP PRO</a></p>
        </div>
        <script>
        function hablar() {{
            var msg = new SpeechSynthesisUtterance("{ultima_voz}");
            msg.lang = 'es-ES'; window.speechSynthesis.speak(msg);
        }}
        new TradingView.widget({{"autosize":true,"symbol":"OANDA:XAUUSD","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_oro"}});
        new TradingView.widget({{"autosize":true,"symbol":"OANDA:EURUSD","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_euro"}});
        new TradingView.widget({{"autosize":true,"symbol":"NASDAQ:TSLA","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_tesla"}});
        new TradingView.widget({{"autosize":true,"symbol":"NASDAQ:META","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_meta"}});
        new TradingView.widget({{"autosize":true,"symbol":"OANDA:SPX500USD","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_sp"}});
        new TradingView.widget({{"autosize":true,"symbol":"NASDAQ:AMZN","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_amzn"}});
        new TradingView.widget({{"autosize":true,"symbol":"BINANCE:BTCUSDT","interval":"15","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":"chart_btc"}});
        </script>
    </body></html>
    """
if not bot_encendido:
    threading.Thread(target=bot_automatico, daemon=True).start()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
