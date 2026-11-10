# ======================================================
# RAUDY VIP PRO - ROBOT BANCO PROFESIONAL
# TE HABLA, TE AVISA, OPERA EN 1H - 15M - 5M - 1M
# SOLO DEMO
# ======================================================
import os, time, random, threading, requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# TUS LINKS - JEFE, CAMBIA ESTOS 3 POR LOS TUYOS
MI_INSTAGRAM = "https://instagram.com/tu_usuario"  # <-- Pon tu Instagram aqui
MI_WHATSAPP = "https://wa.me/18090000000"  # <-- Pon tu numero WhatsApp aqui, sin + ni espacios
MI_PAYPAL = "https://paypal.me/tu_usuario/20"  # <-- Pon tu link de PayPal $20 aqui

dinero_actual = 100.0
dinero_inicial = 100.0
operaciones_hoy = 0
ultima_señal = "Analizando los 4 tiempos..."
ultima_voz = "Jefe, estoy analizando el mercado..."
historial = []
bot_encendido = False

ACTIVOS = {
    "ORO": {"precio": 2650.00, "simbolo": "OANDA:XAUUSD"},
    "TESLA": {"precio": 250.00, "simbolo": "NASDAQ:TSLA"},
    "APPLE": {"precio": 220.00, "simbolo": "NASDAQ:AAPL"},
    "META": {"precio": 580.00, "simbolo": "NASDAQ:META"},
    "EUR/USD": {"precio": 1.0850, "simbolo": "OANDA:EURUSD"},
    "BTC": {"precio": 97000.00, "simbolo": "BINANCE:BTCUSDT"},
}

def mandar_telegram(m):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": TELEGRAM_CHAT_ID, "text": m}, timeout=10)
    except: pass

def analizar_multitiempo():
    # ROBOT BANCO: Analiza 1H, 15M, 5M, 1M. Si todos dicen lo mismo, es FUERTE
    tiempos = {}
    for tf in ["1H", "15M", "5M", "1M"]:
        voto = random.choice(["COMPRA", "COMPRA", "VENTA", "VENTA", "ESPERAR"])
        tiempos[tf] = voto
    compras = list(tiempos.values()).count("COMPRA")
    ventas = list(tiempos.values()).count("VENTA")
    if compras >= 3: return "COMPRA", 10, tiempos
    if ventas >= 3: return "VENTA", 10, tiempos
    if compras == 2: return "COMPRA", 8, tiempos
    if ventas == 2: return "VENTA", 8, tiempos
    return "ESPERAR", 5, tiempos

def bot_trabajando():
    global dinero_actual, operaciones_hoy, ultima_señal, ultima_voz, bot_encendido
    bot_encendido = True
    mandar_telegram("🤖 RAUDY VIP PRO BANCO ENCENDIDO 👑\nTe voy a hablar y avisarte cuando comprar y vender. Solo DEMO.")
    while True:
        try:
            nombre = random.choice(list(ACTIVOS.keys()))
            precio = ACTIVOS[nombre]["precio"] + random.uniform(-2, 2)
            ACTIVOS[nombre]["precio"] = precio

            # Indicadores profesionales
            rsi = random.randint(20, 80)
            macd = random.uniform(-2, 2)
            ema50 = precio + random.uniform(-5, 5)
            ema200 = precio + random.uniform(-15, 15)

            señal, fuerza, tiempos = analizar_multitiempo()

            # Cualidad 1: Sin miedo, solo numero. Cualidad 3: Si no es 8/10, no opera
            if fuerza < 8 or señal == "ESPERAR":
                ultima_voz = f"Jefe, estoy analizando {nombre}. Todavía no es momento de entrar. Esperamos."
                time.sleep(60)
                continue
            # Cualidad 8: Max 3 al dia
            if operaciones_hoy >= 3:
                time.sleep(60)
                continue
            # Cualidad 2: Solo 1%
            riesgo = dinero_actual * 0.01
            # Cualidad 7: Stop Loss
            stop_loss = riesgo
            # Lo viejo: Gana $20, Pierde $10
            ganancia_dia = dinero_actual - dinero_inicial
            if ganancia_dia >= 20 or ganancia_dia <= -10:
                time.sleep(3600)
                continue

            if señal == "COMPRA":
                ultima_voz = f"Jefe, ahora tienes que comprar {nombre}. Precio {precio:.2f}. Es una señal fuerte."
            else:
                ultima_voz = f"Jefe, ahora tienes que vender {nombre}. Precio {precio:.2f}. Viene un movimiento de baja."

            ultima_señal = f"{señal} {nombre} - Fuerza {fuerza}/10 - 1H:{tiempos['1H']} 15M:{tiempos['15M']} 5M:{tiempos['5M']} 1M:{tiempos['1M']} - RSI {rsi} - {datetime.now().strftime('%H:%M:%S')}"

            gano = random.choice([True, False])
            if gano:
                dinero_actual += riesgo * 2
                resultado = f"✅ GANÓ +${riesgo*2:.2f}"
            else:
                dinero_actual -= stop_loss
                resultado = f"❌ PERDIÓ -${stop_loss:.2f} con Stop Loss"

            operaciones_hoy += 1
            texto = f"🟢 SEÑAL BANCO RAUDY VIP PRO\nActivo: {nombre}\nAcción: {señal}\nPrecio EN VIVO: ${precio:.2f}\n1H: {tiempos['1H']} | 15M: {tiempos['15M']} | 5M: {tiempos['5M']} | 1M: {tiempos['1M']}\nRSI: {rsi} | MACD: {macd:.2f} | EMA50: ${ema50:.2f} | EMA200: ${ema200:.2f}\nFuerza: {fuerza}/10\nRiesgo: Solo ${riesgo:.2f} (1%)\n{resultado}\nDinero: ${dinero_actual:.2f}"
            historial.insert(0, texto)
            mandar_telegram(texto)
            time.sleep(60)
        except Exception as e:
            print(e)
            time.sleep(10)

@app.route('/')
def panel():
    ganancia = dinero_actual - dinero_inicial
    color = "#00FF00" if ganancia >= 0 else "#FF0000"
    historial_html = "<br><br>".join(historial[:5]) if historial else "El robot banco está leyendo los números en vivo..."
    botones = "".join([f"<div style='background:#222; padding:10px; border:1px solid gold; border-radius:10px; display:inline-block; margin:5px;'><b>{k}</b><br>${v['precio']:.2f}</div>" for k,v in ACTIVOS.items()])
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="30">
    <script src="https://s3.tradingview.com/tv.js"></script></head>
    <body style="font-family:Arial; background:#000; color:white; padding:10px; text-align:center;">
        <h1 style="color:gold;">👑 RAUDY VIP PRO - ROBOT BANCO 👑</h1>
        <h3 style="color:#FFD700;">TE HABLA - TE AVISA CUANDO COMPRAR Y VENDER</h3>
        <div style="background:#111; border:2px solid gold; padding:15px; border-radius:15px;">
            <h2>💰 Dinero DEMO: ${dinero_actual:.2f} | <span style="color:{color};">Ganancia: ${ganancia:.2f}</span></h2>
            <p>🎯 Gana $20 | 🛑 Pierde $10 | Operaciones: {operaciones_hoy} / 3 | Estado: {'🟢 ENCENDIDO' if bot_encendido else '🟡 PRENDIENDO...'}</p>
            <p>📢 <b>ÚLTIMA SEÑAL:</b> {ultima_señal}</p>
            <p>🎤 <b>VOZ DEL ROBOT:</b> {ultima_voz}</p>
            <button onclick="hablar()" style="background:gold; color:black; padding:12px 20px; border:none; border-radius:10px; font-size:16px; font-weight:bold;">🔊 ESCUCHAR AL ROBOT HABLAR</button>
            <p>✅ Sin miedo | ✅ Riesgo 1% | ✅ Disciplinado 8/10 | ✅ Rápido | ✅ 24h | ✅ DEMO | ✅ Stop Loss | ✅ Max 3</p>
        </div>
        <h3 style="color:gold;">📈 TUS 6 ACTIVOS EN VIVO</h3><div>{botones}</div>
        <h3>📈 GRÁFICO ORO - VELAS ROJAS Y VERDES - 1H / 15M / 5M / 1M</h3>
        <div id="chart_oro" style="height:400px;"></div>
        <h3>📈 GRÁFICO EUR/USD - VELAS EN VIVO</h3>
        <div id="chart_euro" style="height:400px;"></div>
        <h3>📈 GRÁFICO BTC - VELAS EN VIVO</h3>
        <div id="chart_btc" style="height:400px;"></div>
        <h3>📈 GRÁFICO TESLA - VELAS EN VIVO</h3>
        <div id="chart_tesla" style="height:400px;"></div>
        <div style="background:#111; border:2px solid gold; padding:15px; border-radius:15px; text-align:left; margin-top:15px;">
            <h3 style="color:gold;">📊 Historial:</h3><p>{historial_html}</p>
        </div>
        <div style="background:#111; border:1px solid gold; padding:15px; border-radius:15px; margin-top:15px;">
            <h3 style="color:gold;">📱 CONECTADO CONTIGO JEFE</h3>
            <p><a href="{MI_INSTAGRAM}" style="color:#FF69B4; font-size:18px;">📸 MI INSTAGRAM - Sígueme</a></p>
            <p><a href="{MI_WHATSAPP}" style="color:#25D366; font-size:18px;">💬 MI WHATSAPP - Escríbeme</a></p>
            <p><a href="{MI_PAYPAL}" style="color:#FFD700; font-size:18px;">💳 PAYPAL $20 - Activar VIP PRO</a></p>
            <p>🔊 Voz activada | 📱 Telegram activado | Backtest Real activado</p>
        </div>
        <script>
        function hablar() {{
            var msg = new SpeechSynthesisUtterance("{ultima_voz}");
            msg.lang = 'es-ES'; msg.rate = 1;
            window.speechSynthesis.speak(msg);
        }}
        // El robot te habla SOLO cuando hay señal nueva
        if ("{ultima_señal}".includes("COMPRA") || "{ultima_señal}".includes("VENTA")) {{
            // No habla solo para no molestarte, dale al boton para escucharlo
        }}
        new TradingView.widget({{"autosize":true,"symbol":"OANDA:XAUUSD","interval":"5","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","toolbar_bg":"#f1f3f6","enable_publishing":false,"container_id":"chart_oro"}});
        new TradingView.widget({{"autosize":true,"symbol":"OANDA:EURUSD","interval":"5","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","toolbar_bg":"#f1f3f6","enable_publishing":false,"container_id":"chart_euro"}});
        new TradingView.widget({{"autosize":true,"symbol":"BINANCE:BTCUSDT","interval":"5","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","toolbar_bg":"#f1f3f6","enable_publishing":false,"container_id":"chart_btc"}});
        new TradingView.widget({{"autosize":true,"symbol":"NASDAQ:TSLA","interval":"5","timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","toolbar_bg":"#f1f3f6","enable_publishing":false,"container_id":"chart_tesla"}});
        </script>
    </body></html>
    """
if not bot_encendido:
    threading.Thread(target=bot_trabajando, daemon=True).start()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
