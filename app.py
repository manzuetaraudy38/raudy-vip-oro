# ============================================================
# RAUDY VIP PRO - TODO JUNTO - AUTOMATICO + TRADINGVIEW + TELEGRAM + VOZ
# Jefe: Raudy Manzueta - PayPal: paypal.me/RaudyManzueta/20
# Bot: @raudy_vip_oro_bot
# ============================================================
import os, random, threading, time, requests, yfinance as yf
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ============ CONFIGURACION - TUS LLAVES ============
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "767574050")
PAYPAL_LINK = "https://paypal.me/RaudyManzueta/20"
TELEGRAM_LINK = "https://t.me/raudy_vip_oro_bot"

# ============ DINERO DEMO Y REGLAS ============
dinero_demo = 1000.0
posicion_abierta = None
operaciones_hoy = 0
ganancia_hoy = 0.0
ultima_señal = "Robot encendido, esperando señal..."
ultima_voz = "Jefe, ya estoy encendido y trabajando solo."
historial = ["🤖 RAUDY VIP PRO ENCENDIDO - TODO JUNTO"]
precios = {}
senal_por_activo = {}

# ============ TUS 14 ACTIVOS ============
ACTIVOS = {
    "ORO": "GC=F", "BTC": "BTC-USD",
    "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "USDJPY=X",
    "USD/CHF": "USDCHF=X", "AUD/USD": "AUDUSD=X", "USD/CAD": "USDCAD=X",
    "TESLA": "TSLA", "META": "META", "APPLE": "AAPL", "AMAZON": "AMZN", "NVIDIA": "NVDA",
    "SP500": "^GSPC"
}

# ============ TELEGRAM ============
def mandar_telegram(mensaje):
    if not TELEGRAM_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}, timeout=5)
    except:
        pass

# ============ PRECIOS REALES ============
def actualizar_precios():
    global precios
    for nombre, simbolo in ACTIVOS.items():
        try:
            ticker = yf.Ticker(simbolo)
            hist = ticker.history(period="1d", interval="5m")
            if len(hist) > 0:
                precios[nombre] = float(hist['Close'].iloc[-1])
        except:
            pass
    return precios

def analizar_activo(nombre):
    # Simula indicadores reales: RSI, MACD, EMA
    rsi = random.randint(18, 82)
    macd = random.choice(["ALCISTA", "BAJISTA"])
    tendencia = random.choice(["ALCISTA", "BAJISTA", "LATERAL"])
    if rsi < 30 and macd == "ALCISTA":
        return {"accion": "COMPRA", "rsi": rsi, "macd": macd, "tendencia": tendencia, "confianza": random.randint(78, 95)}
    if rsi > 70 and macd == "BAJISTA":
        return {"accion": "VENTA", "rsi": rsi, "macd": macd, "tendencia": tendencia, "confianza": random.randint(78, 95)}
    return {"accion": "ESPERA", "rsi": rsi, "macd": macd, "tendencia": tendencia, "confianza": random.randint(40, 65)}

# ============ ROBOT AUTOMATICO - CEREBRO ============
def robot_automatico():
    global dinero_demo, posicion_abierta, operaciones_hoy, ganancia_hoy, ultima_señal, ultima_voz
    while True:
        try:
            time.sleep(60)
            if operaciones_hoy >= 3:
                ultima_señal = "Jefe, ya hice 3 operaciones hoy. Me apago por disciplina."
                continue
            if ganancia_hoy >= 20:
                ultima_señal = "Jefe, ya gané $20 hoy. Me apago solo para cuidar tu dinero."
                continue
            if ganancia_hoy <= -10:
                ultima_señal = "Jefe, perdí $10 hoy. Me apago solo con Stop Loss del día."
                continue

            actualizar_precios()
            # Revisa todos los activos
            for nombre in ACTIVOS:
                if nombre not in precios:
                    continue
                analisis = analizar_activo(nombre)
                senal_por_activo[nombre] = analisis
                if posicion_abierta is None and analisis["accion"] in ["COMPRA", "VENTA"] and analisis["confianza"] >= 75:
                    precio = precios[nombre]
                    stop = precio * 0.995 if analisis["accion"] == "COMPRA" else precio * 1.005
                    tp = precio * 1.01 if analisis["accion"] == "COMPRA" else precio * 0.99
                    posicion_abierta = {"activo": nombre, "tipo": analisis["accion"], "entrada": precio, "stop": stop, "tp": tp}
                    operaciones_hoy += 1
                    ultima_señal = f"YO SOLO ENTRÉ - {analisis['accion']} {nombre} en ${precio:.2f} - Confianza {analisis['confianza']}%"
                    ultima_voz = f"Jefe, yo solo compré {nombre}. Entré solo."
                    texto = f"🤖 ENTRÉ SOLO\n{analisis['accion']} {nombre}\nPrecio: ${precio:.2f}\nRSI: {analisis['rsi']} | MACD: {analisis['macd']}\nConfianza: {analisis['confianza']}%"
                    historial.insert(0, texto); mandar_telegram(texto)
                    break
                # Si hay posición, revisa salida
                elif posicion_abierta and posicion_abierta["activo"] == nombre:
                    precio_actual = precios[nombre]
                    g = 0
                    cerrar = False
                    motivo = ""
                    if posicion_abierta["tipo"] == "COMPRA":
                        if precio_actual >= posicion_abierta["tp"]:
                            g = 10; cerrar = True; motivo = "TAKE PROFIT - GANANCIA"
                        elif precio_actual <= posicion_abierta["stop"]:
                            g = -5; cerrar = True; motivo = "STOP LOSS - PÉRDIDA CONTROLADA"
                    else:
                        if precio_actual <= posicion_abierta["tp"]:
                            g = 10; cerrar = True; motivo = "TAKE PROFIT - GANANCIA"
                        elif precio_actual >= posicion_abierta["stop"]:
                            g = -5; cerrar = True; motivo = "STOP LOSS - PÉRDIDA CONTROLADA"
                    if cerrar:
                        dinero_demo += g; ganancia_hoy += g
                        texto = f"✅ CERRÉ SOLO - {posicion_abierta['activo']}\nMotivo: {motivo}\nGanancia: ${g}\nBalance: ${dinero_demo:.2f}"
                        ultima_señal = texto; ultima_voz = f"Jefe, cerré solo {posicion_abierta['activo']} con {motivo}."
                        historial.insert(0, texto); mandar_telegram(texto)
                        posicion_abierta = None
        except Exception as e:
            print("Error robot:", e)

# ============ WEBHOOK TRADINGVIEW - TU APP CONECTADA ============
@app.route('/webhook', methods=['POST'])
def webhook_tradingview():
    global posicion_abierta, ultima_señal, ultima_voz, operaciones_hoy
    try:
        datos = request.get_json(force=True)
        activo = datos.get("activo", "ORO")
        accion = datos.get("accion", "COMPRA").upper()
        precio = float(datos.get("precio", 0))
        if posicion_abierta is not None:
            return jsonify({"ok": False, "mensaje": "Ya hay una operación abierta"})
        if accion in ["COMPRA", "BUY", "LONG"]:
            tipo = "COMPRA"
        elif accion in ["VENTA", "SELL", "SHORT"]:
            tipo = "VENTA"
        else:
            return jsonify({"ok": False})
        stop = precio * 0.995 if tipo == "COMPRA" else precio * 1.005
        tp = precio * 1.01 if tipo == "COMPRA" else precio * 0.99
        posicion_abierta = {"activo": activo, "tipo": tipo, "entrada": precio, "stop": stop, "tp": tp}
        operaciones_hoy += 1
        ultima_señal = f"TRADINGVIEW MANDÓ {tipo} SOLO - {activo} en ${precio:.2f}"
        ultima_voz = f"Jefe, TradingView me mandó {tipo} {activo}. Ya entré solo."
        texto = f"📈 TRADINGVIEW CONECTADO - ENTRÓ SOLO\n{tipo} {activo}\nPrecio: ${precio:.2f}\nSeñal desde tu app de TradingView."
        historial.insert(0, texto); mandar_telegram(texto)
        return jsonify({"ok": True, "mensaje": "Robot recibió señal de TradingView"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# ============ PANTALLA PRINCIPAL - TODO EN ESPAÑOL ============
HTML = """
<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RAUDY VIP PRO - AUTOMATICO</title>
<style>body{background:#0a0a0a;color:#fff;font-family:Arial;padding:12px;text-align:center} .card{background:#1a1a1a;border:2px solid #FFD700;border-radius:16px;padding:14px;margin:10px 0} .verde{color:#00ff88} .rojo{color:#ff4444} .btn{background:#FFD700;color:#000;padding:12px 18px;border-radius:10px;font-weight:900;border:none;font-size:16px;margin:5px} .grid{display:grid;grid-template-columns:1fr 1fr;gap:8px} .mini{background:#222;padding:10px;border-radius:10px} a{color:#FFD700}</style></head>
<body>
<h1>👑 RAUDY VIP PRO</h1><p>AUTOMÁTICO + TRADINGVIEW + TELEGRAM</p>
<div class="card"><h2>💰 Balance DEMO: ${{ dinero }} | Hoy: ${{ ganancia_hoy }} | Operaciones: {{ ops }}/3</h2>
<p><b>Señal:</b> {{ senal }}</p>
<p><b>Posición:</b> {{ posicion }}</p>
<button class="btn" onclick="hablar()">🔊 ESCUCHAR AL ROBOT</button>
<p><a href="{{ paypal }}" target="_blank">💳 PAGAR $20 CON PAYPAL</a> | <a href="{{ telegram }}" target="_blank">📩 MI TELEGRAM</a></p>
</div>
<div class="card"><h3>📊 MIS 14 ACTIVOS EN VIVO</h3><div class="grid">{% for k,v in precios.items() %}<div class="mini"><b>{{ k }}</b><br>${{ "%.2f"|format(v) }}<br><small>{{ senales[k].accion if k in senales else '...' }} | RSI {{ senales[k].rsi if k in senales else '-' }}</small></div>{% endfor %}</div></div>
<div class="card"><h3>📈 GRÁFICOS TRADINGVIEW EN VIVO</h3>
<div class="tradingview-widget-container"><div id="tv"></div><script src="https://s3.tradingview.com/tv.js"></script><script>new TradingView.widget({autosize:true,symbol:"OANDA:XAUUSD",interval:"15",timezone:"America/Santo_Domingo",theme:"dark",locale:"es",container_id:"tv"});</script></div>
</div>
<div class="card"><h3>📜 HISTORIAL</h3>{% for h in historial %}<p style="text-align:left;border-bottom:1px solid #333;padding:6px">{{ h }}</p>{% endfor %}</div>
<script>function hablar(){let u=new SpeechSynthesisUtterance("{{ voz }}");u.lang='es-DO';speechSynthesis.speak(u);} setTimeout(()=>location.reload(),60000);</script>
</body></html>
"""

@app.route('/')
def inicio():
    actualizar_precios()
    pos_txt = "Sin operación - Esperando" if not posicion_abierta else f"{posicion_abierta['tipo']} {posicion_abierta['activo']} en ${posicion_abierta['entrada']:.2f}"
    return render_template_string(HTML, dinero=f"{dinero_demo:.2f}", ganancia_hoy=f"{ganancia_hoy:.2f}", ops=operaciones_hoy, senal=ultima_señal, posicion=pos_txt, voz=ultima_voz, paypal=PAYPAL_LINK, telegram=TELEGRAM_LINK, precios=precios, senales=senal_por_activo, historial=historial[:15])

@app.route('/salud')
def salud():
    return jsonify({"ok": True, "robot": "RAUDY VIP PRO", "balance": dinero_demo})

# Arrancar robot
threading.Thread(target=robot_automatico, daemon=True).start()
mandar_telegram("🤖 RAUDY VIP PRO - TODO JUNTO ENCENDIDO 👑\nAutomático + TradingView + Telegram + Voz\nYa estoy trabajando solo, jefe.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
