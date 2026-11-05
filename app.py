from flask import Flask, session, request, redirect, jsonify
import requests
import threading
import time
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cambia-esto-en-render-por-una-larga")
CLAVE_BUENA = os.getenv("VIP_CLAVE", "RAUDY26")
FECHA_VENCE = datetime(2026, 12, 3, 23, 59, 59)
BOT_TOKEN = os.getenv("BOT_TOKEN", "AQUI_PON_TU_TOKEN_DEL_BOTFATHER")
CHAT_ID_VIP = os.getenv("CHAT_ID", "AQUI_PON_TU_ID_O_DEL_CANAL")
BOT_USERNAME = os.getenv("BOT_USERNAME", "raudy_vip_oro_bot")
COMPRAS = [3900, 3890, 3865]
VENTAS = [3980, 3990, 4020]
alertado_compra = {p: False for p in COMPRAS}
alertado_venta = {p: False for p in VENTAS}
ultimo_update_id = 0
historial_oro = []
historial_senales = []

# ===== 50 ROBOTS RAUDY - CADA UNO HACE SU TRABAJO =====
ROBOTS_RAUDY = []
NOMBRES_ROBOTS = ["Cazador Rapido","Relampago Oro","Flecha Veloz","Ojo Aguila","Tiburon Oro","Ninja Precio","Rayo Londres","Trueno NY","Guardian Scalping","Maestro Scalping","Rey Londres","Reina Londres","Guardian Londres","Cazador Londres","Jefe Londres","Rey NY","Reina NY","Guardian NY","Cazador NY","Jefe NY","Ojo Noticias","Alarma Noticias","Guardian Noticias","Cazador Noticias","Jefe Noticias","Soporte 3900","Soporte 3890","Soporte 3865","Resistencia 3980","Resistencia 4020","Robot DIOS 1","Robot DIOS 2","Robot DIOS 3","Robot DIOS 4","Robot DIOS 5","Robot DIOS 6","Robot DIOS 7","Robot DIOS 8","Robot DIOS 9","Robot DIOS 10","Guardian Capital","Guardian Fin Semana","Guardian Cuenta","Guardian Familia","Guardian Anti-Perdida","Guardian Modo Nino","Guardian Psicologia","Guardian Copia Segura","Guardian Idioma","MAESTRO SUPREMO"]
for i, nom in enumerate(NOMBRES_ROBOTS, 1):
    ROBOTS_RAUDY.append({"id": i, "nombre": nom, "trabajo": "Trabaja con el equipo", "estrellas": 0, "puntos": 0, "mensaje": "Listo para trabajar"})

def chat_robots(precio, maestro):
    if precio <= 3910:
        return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro bajo, yo digo COMPRA"}, {"robot": "Robot 18 Guardian NY", "texto": "Confirmo, yo tambien COMPRA"}, {"robot": "Robot 50 MAESTRO", "texto": "Decido: " + maestro["señal"]}]
    if precio >= 3970:
        return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro subio, yo digo VENTA"}, {"robot": "Robot 16 Rey NY", "texto": "Confirmo, yo tambien VENTA"}, {"robot": "Robot 50 MAESTRO", "texto": "Decido: " + maestro["señal"]}]
    return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro en medio, yo digo ESPERA"}, {"robot": "Robot 50 MAESTRO", "texto": "Decido: " + maestro["señal"]}]

def hora_ginebra():
    return datetime.utcnow() + timedelta(hours=1)
def dias_restantes():
    delta = FECHA_VENCE - hora_ginebra()
    return max(0, delta.days)
def codigo_vigente():
    return hora_ginebra() <= FECHA_VENCE

def filtro_noticias(precio):
    ahora = hora_ginebra()
    hora = ahora.hour
    minuto = ahora.minute
    if hora == 14 and 25 <= minuto <= 59:
        return {"texto": "🔴 NO OPERES - NOTICIAS USA 14:30 - ESPERA 30 MIN", "color": "#ff0000", "puede": False}
    if hora == 8 and 25 <= minuto <= 45:
        return {"texto": "🔴 NO OPERES - NOTICIAS 08:30 - ESPERA", "color": "#ff0000", "puede": False}
    if hora == 10 and 0 <= minuto <= 15:
        return {"texto": "🟡 CUIDADO - NOTICIAS EUROPA 10:00", "color": "#FFA500", "puede": True}
    if len(historial_oro) >= 5:
        cambio = abs(precio - historial_oro[-5])
        if cambio > 25:
            return {"texto": "🟡 CUIDADO - MERCADO LOCO SE MOVIO " + str(round(cambio,2)) + " RAPIDO - ESPERA", "color": "#FFA500", "puede": True}
    return {"texto": "🟢 FILTRO OK - PUEDES OPERAR - SIN NOTICIAS FUERTES", "color": "#00aa00", "puede": True}

def reloj_mundial():
    ahora_ginebra = hora_ginebra()
    hora_londres = ahora_ginebra - timedelta(hours=1)
    hora_ny = ahora_ginebra - timedelta(hours=6)
    hora_tokio = ahora_ginebra + timedelta(hours=8)
    dia_semana = ahora_ginebra.weekday()
    nombres_dia = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
    dia_nombre = nombres_dia[dia_semana]
    hora_g = ahora_ginebra.hour
    if dia_semana >= 5:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🔴 HOY ES " + dia_nombre + " - MERCADO CERRADO", "color": "#ff0000", "sesion": "MERCADO CERRADO", "puede": False}
    if 9 <= hora_g < 11:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🟢 HOY " + dia_nombre + " - SESION LONDRES - BUENA HORA", "color": "#00aa00", "sesion": "LONDRES", "puede": True}
    if (hora_g == 14 and ahora_ginebra.minute >= 30) or (15 <= hora_g < 17):
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🟢🟢 HOY " + dia_nombre + " - SESION NEW YORK - LA MEJOR HORA", "color": "#00aa00", "sesion": "NEW YORK MEJOR HORA", "puede": True}
    if 2 <= hora_g < 6:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🔴 HOY " + dia_nombre + " - SESION ASIA - MERCADO DORMIDO", "color": "#ff0000", "sesion": "ASIA DORMIDO", "puede": False}
    if hora_g >= 22 or hora_g < 2:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🔴 HOY " + dia_nombre + " - MERCADO DE NOCHE", "color": "#ff0000", "sesion": "NOCHE", "puede": False}
    return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": "🟡 HOY " + dia_nombre + " - ENTRE SESIONES - ESPERA 09:00 O 14:30", "color": "#FFA500", "sesion": "ENTRE SESIONES", "puede": True}

def get_price_yahoo(symbol, fallback):
    try:
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + symbol
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        j = r.json()
        price = j['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except:
        return fallback

def get_oro_precio():
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=4)
        return float(r.json().get('price', 3922))
    except:
        return get_price_yahoo('GC=F', 3922)

def analizar_ia_oro(precio):
    historial_oro.append(precio)
    if len(historial_oro) > 50:
        historial_oro.pop(0)
    if len(historial_oro) >= 10:
        max_reciente = max(historial_oro[-20:])
        min_reciente = min(historial_oro[-20:])
    else:
        max_reciente = precio + 20
        min_reciente = precio - 20
    if precio <= 3905 and precio >= 3860:
        res = {"señal": "🟢 COMPRA SWING", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA SWING", "analisis": "IA SWING: Oro hizo SWING BAJO en " + str(round(min_reciente,2)) + " en zona 3900-3865. Es zona de COMPRA.", "entrada": precio, "tp": round(precio + 35, 2), "sl": round(precio - 18, 2), "confianza": "88%"}
    elif precio >= 3980 and precio <= 4030:
        res = {"señal": "🔴 VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA SWING", "analisis": "IA SWING: Oro hizo SWING ALTO en " + str(round(max_reciente,2)) + " en zona 3980-4020. Es zona de VENTA.", "entrada": precio, "tp": round(precio - 35, 2), "sl": round(precio + 18, 2), "confianza": "88%"}
    elif precio > 4030:
        res = {"señal": "🔴 YA PASO ZONA VENTA - ESPERA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - YA PASO VENTA", "analisis": "IA: Oro alto. Ya paso venta. Espera que baje a 3980 o a 3900.", "entrada": precio, "tp": 3980, "sl": round(precio + 20, 2), "confianza": "65%"}
    elif precio > 3940:
        res = {"señal": "🔴 ESPERANDO VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - ESPERANDO VENTA", "analisis": "IA: Oro en " + str(round(precio,2)) + ". No compres aqui. Espera 3980 venta o 3900 compra.", "entrada": precio, "tp": 3900, "sl": 4040, "confianza": "65%"}
    elif precio < 3940 and precio > 3905:
        res = {"señal": "🟡 CERCA DE COMPRA SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 LUZ NARANJA - CERCA DE COMPRA", "analisis": "IA: Oro se acerca a compra. Si toca 3900 es COMPRA.", "entrada": 3900, "tp": 3935, "sl": 3882, "confianza": "70%"}
    else:
        res = {"señal": "🟡 ANALIZANDO SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 ANALIZANDO", "analisis": "IA: Analizando swing... Espera señal clara.", "entrada": precio, "tp": round(precio + 30, 2), "sl": round(precio - 15, 2), "confianza": "50%"}
    res["botin"] = res["tp"]
    res["salida_emergencia"] = res["sl"]
    res["entrada_grafico"] = res["entrada"]
    return res

def analizar_50_raudy(precio, eur_val, gbp_val):
    votos = []
    votos.append(("1 SWING", "COMPRA" if precio <= 3905 else "VENTA" if precio >= 3980 else "ESPERA"))
    if len(historial_oro) >= 2 and precio > historial_oro[-2] + 5:
        votos.append(("2 RAPIDO", "COMPRA"))
    elif len(historial_oro) >= 2 and precio < historial_oro[-2] - 5:
        votos.append(("2 RAPIDO", "VENTA"))
    else:
        votos.append(("2 RAPIDO", "ESPERA"))
    votos.append(("3 TENDENCIA", "COMPRA" if precio > 3940 else "VENTA"))
    f = filtro_noticias(precio)
    votos.append(("4 NOTICIAS", "ESPERA" if not f["puede"] else "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("5 VELAS", "VENTA" if precio >= 3970 else "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("6 ORO Y DOLAR", "COMPRA" if eur_val > 1.115 else "VENTA"))
    votos.append(("7 SOPORTE", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("8 VOLUMEN", "COMPRA" if len(historial_oro)>=5 and abs(precio-historial_oro[-5])>10 else "ESPERA"))
    votos.append(("9 ZONA PELIGROSA", "ESPERA" if abs(precio-3940) < 5 else "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("10 MAESTRO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("11 RSI", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("12 MACD", "COMPRA" if precio > 3940 else "VENTA"))
    votos.append(("13 BOLLINGER", "COMPRA" if precio <= 3900 else "VENTA" if precio >= 3990 else "ESPERA"))
    votos.append(("14 FIBONACCI", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("15 SESIONES", "COMPRA" if 9 <= hora_ginebra().hour < 17 else "ESPERA"))
    votos.append(("16 SENTIMIENTO", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("17 IA PREDICCION", "COMPRA" if precio <= 3920 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("18 DIVERGENCIA", "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("19 ROMPIMIENTO", "COMPRA" if precio > 3980 else "VENTA" if precio < 3900 else "ESPERA"))
    votos.append(("20 MAESTRO FINAL", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("21 MEDIA MOVIL", "COMPRA" if precio > 3940 else "VENTA"))
    votos.append(("22 ORO vs PLATA", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("23 PETROLEO", "COMPRA" if precio < 3940 else "ESPERA"))
    votos.append(("24 BITCOIN", "COMPRA" if precio < 3940 else "ESPERA"))
    votos.append(("25 MIEDO", "ESPERA" if abs(precio-3940)<10 else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("26 HORA NOTICIA", "ESPERA" if not f["puede"] else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("27 REBOTE", "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("28 TRAMPA", "ESPERA" if 3935 <= precio <= 3945 else "COMPRA" if precio<3935 else "VENTA"))
    votos.append(("29 GUARDIAN", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("30 MAESTRO SUPREMO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("31 HISTORIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("32 CAZADOR NOCTURNO", "ESPERA"))
    votos.append(("33 ANTI-PERDIDA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("34 DOBLE CONFIRMACION", "COMPRA" if precio <= 3905 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("35 MAESTRO FINAL 2", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("36 APERTURA LONDRES", "COMPRA" if 9 <= hora_ginebra().hour < 11 and precio <= 3920 else "ESPERA"))
    votos.append(("37 APERTURA NY", "COMPRA" if 14 <= hora_ginebra().hour < 17 and precio <= 3920 else "VENTA" if 14 <= hora_ginebra().hour < 17 and precio >= 3970 else "ESPERA"))
    votos.append(("38 GAP", "ESPERA"))
    votos.append(("39 SPREAD", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("40 SWAP", "ESPERA"))
    votos.append(("41 PATRONES", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("42 PIVOT", "COMPRA" if precio <= 3900 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("43 PSICOLOGIA", "ESPERA"))
    votos.append(("44 COPIA SEGURA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("45 ALERTA FAMILIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("46 MODO NINO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("47 PROTECTOR", "ESPERA" if precio > 4030 else "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("48 MODO OSCURO", "ESPERA"))
    votos.append(("49 IDIOMA", "ESPERA"))
    c_compra = sum(1 for _, v in votos if v == "COMPRA")
    c_venta = sum(1 for _, v in votos if v == "VENTA")
    c_espera = sum(1 for _, v in votos if v == "ESPERA")
    if c_compra >= 35:
        maestro = {"señal": "👑🔥 COMPRA DIOS - LA MEJOR DEL DIA", "color": "#00ff00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE FUERTE - COMPRA DIOS"}
    elif c_venta >= 35:
        maestro = {"señal": "👑🔥 VENTA DIOS - LA MEJOR DEL DIA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA FUERTE - VENTA DIOS"}
    elif c_compra > c_venta + 5:
        maestro = {"señal": "🟢 COMPRA FUERTE", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA"}
    elif c_venta > c_compra + 5:
        maestro = {"señal": "🔴 VENTA FUERTE", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA"}
    else:
        maestro = {"señal": "🟡 ESPERA - LOS 50 NO ESTAN DE ACUERDO", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 LUZ AMARILLA - ESPERA"}
    maestro["votos_compra"] = c_compra
    maestro["votos_venta"] = c_venta
    maestro["votos_espera"] = c_espera
    maestro["lista"] = votos
    maestro["total"] = 50
    return maestro

def send_telegram(mensaje):
    try:
        if "AQUI_PON" in BOT_TOKEN:
            return
        url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
        for chat_id in CHAT_ID_VIP.split(","):
            chat_id = chat_id.strip()
            if not chat_id or "AQUI_PON" in chat_id:
                continue
            payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=5)
    except:
        pass

def telegram_bot_loop():
    global ultimo_update_id
    while True:
        try:
            precio = get_oro_precio()
            ia = analizar_ia_oro(precio)
            for nivel in COMPRAS:
                if precio <= nivel and not alertado_compra[nivel]:
                    send_telegram("🔥 RAUDY ORO - COMPRA - Oro toco " + str(nivel))
                    alertado_compra[nivel] = True
                if precio > nivel + 40:
                    alertado_compra[nivel] = False
            for nivel in VENTAS:
                if precio >= nivel and not alertado_venta[nivel]:
                    send_telegram("🔴 RAUDY ORO - VENTA - Oro toco " + str(nivel))
                    alertado_venta[nivel] = True
                if precio < nivel - 40:
                    alertado_venta[nivel] = False
            if "AQUI_PON" not in BOT_TOKEN:
                url = "https://api.telegram.org/bot" + BOT_TOKEN + "/getUpdates"
                params = {"offset": ultimo_update_id + 1, "timeout": 5}
                resp = requests.get(url, params=params, timeout=10).json()
                if resp.get("ok"):
                    for upd in resp.get("result", []):
                        ultimo_update_id = upd["update_id"]
                        msg = upd.get("message", {})
                        texto = msg.get("text", "").lower().strip()
                        if texto in ["/start", "start", "hola", "hi"]:
                            send_telegram("🔥 RAUDY ORO PRO VIP ACTIVO - Escribe /precios")
                        elif texto in ["/precios", "precios", "oro"]:
                            send_telegram("🟡 ORO AHORA: " + str(precio))
        except:
            pass
        time.sleep(60)

threading.Thread(target=telegram_bot_loop, daemon=True).start()

def esta_logueado():
    if not codigo_vigente():
        return False
    return session.get("vip") == CLAVE_BUENA

@app.route('/login', methods=['GET','POST'])
def login():
    if not codigo_vigente():
        return '<h1>CODIGO VENCIDO</h1><a href="https://www.paypal.me/RaudyManzueta/20">PAGAR $20</a>'
    error = ""
    dias = dias_restantes()
    if request.method == 'POST':
        clave = request.form.get("clave","").strip().upper()
        if clave == CLAVE_BUENA:
            session["vip"] = CLAVE_BUENA
            return redirect("/")
        error = "CLAVE MALA"
    pagina = "<html><body style='background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:20px'><div style='border:2px solid #FFD700;border-radius:20px;padding:25px;background:#1a1a1a;max-width:400px;margin:40px auto'><h1 style='color:#FFD700;'>RAUDY ORO PRO VIP</h1><div>VENCE EN __DIAS__ DIAS</div><form method='POST'><input name='clave' placeholder='ESCRIBE TU CLAVE VIP' required style='padding:15px;width:90%'><div style='color:red'>" + error + "</div><button style='background:#FFD700;padding:15px;width:100%;font-weight:bold'>ENTRAR VIP</button></form><a href='https://www.paypal.me/RaudyManzueta/20' style='background:#FFD700;color:black;display:block;padding:15px;margin-top:10px;text-decoration:none;font-weight:bold'>PAGAR VIP $20</a><a href='https://wa.me/41767574050' style='background:#25D366;color:white;display:block;padding:15px;margin-top:10px;text-decoration:none;font-weight:bold'>WHATSAPP RAUDY</a><a href='https://t.me/__BOT__' style='background:#229ED9;color:white;display:block;padding:15px;margin-top:10px;text-decoration:none;font-weight:bold'>TELEGRAM</a></div></body></html>"
    pagina = pagina.replace("__DIAS__", str(dias)).replace("__BOT__", BOT_USERNAME)
    return pagina

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route('/api/robots')
def api_robots():
    if not esta_logueado():
        return jsonify({"error": "no autorizado"}), 401
    return jsonify({"robots": sorted(ROBOTS_RAUDY, key=lambda x: x["estrellas"], reverse=True)})

@app.route('/api/dar_estrella', methods=['POST'])
def api_dar_estrella():
    if not esta_logueado():
        return jsonify({"error": "no autorizado"}), 401
    d = request.get_json() or {}
    rid = int(d.get("id", 0))
    cant = int(d.get("estrellas", 1))
    for r in ROBOTS_RAUDY:
        if r["id"] == rid:
            r["estrellas"] += cant
            r["puntos"] += cant * 10
            r["mensaje"] = "Gracias jefe! Raudy me dio estrella"
            return jsonify({"ok": True, "mensaje": "Le diste estrella a Robot " + str(rid)})
    return jsonify({"error": "no encontrado"}), 404

@app.route('/api/precios')
def precios():
    if not esta_logueado():
        return jsonify({"error": "no autorizado"}), 401
    oro = 3951.50
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=4)
        oro = r.json().get('price', oro)
    except:
        oro = get_price_yahoo('GC=F', oro)
    oro_f = float(oro)
    gbp_v = get_price_yahoo('GBPUSD=X', 1.3412)
    eur_v = get_price_yahoo('EURUSD=X', 1.1197)
    tesla_v = get_price_yahoo('TSLA', 245.80)
    apple_v = get_price_yahoo('AAPL', 185.30)
    ia = analizar_ia_oro(oro_f)
    filtro = filtro_noticias(oro_f)
    reloj = reloj_mundial()
    maestro50 = analizar_50_raudy(oro_f, eur_v, gbp_v)
    chat = chat_robots(oro_f, maestro50)
    historial_senales.append({"hora": hora_ginebra().strftime("%H:%M"), "precio": oro_f, "señal": maestro50["señal"]})
    if len(historial_senales) > 100:
        historial_senales.pop(0)
    return {"oro": oro_f,"gbp": gbp_v,"eur": eur_v,"tesla": tesla_v,"apple": apple_v,"ia": ia, "filtro": filtro, "reloj": reloj, "maestro50": maestro50, "historial": historial_senales[-20:], "chat_robots": chat, "robots_top": sorted(ROBOTS_RAUDY, key=lambda x: x["estrellas"], reverse=True)[:5]}

@app.route('/')
def home():
    if not esta_logueado():
        return redirect("/login")
    dias = dias_restantes()
    fecha_txt = FECHA_VENCE.strftime("%d/%m/%Y")
    pagina = get_html()
    pagina = pagina.replace("__DIAS__", str(dias)).replace("__FECHA__", fecha_txt).replace("__BOT__", BOT_USERNAME)
    return pagina

def get_html():
    return """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY ORO PRO</title>
<script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
<style>
body{background:#0a0a0a;color:white;font-family:Arial;margin:0;padding:10px}
.header{text-align:center;padding:15px;border:2px solid #FFD700;border-radius:15px;background:#1a1a1a;margin-bottom:12px}
.box{border:2px solid #FFD700;border-radius:15px;padding:12px;text-align:center;margin-bottom:14px;background:#1a1a1a}
.precio{font-size:32px;color:#00ff00;font-weight:bold}
.maestro-box{border:3px solid #FFD700;border-radius:15px;padding:12px;background:#1a1a00;margin-bottom:14px;text-align:center}
.luz-grande{width:60px;height:60px;border-radius:50%;background:#333;margin:10px auto}
.robot-card{border:2px solid #FFD700;border-radius:12px;padding:10px;background:#1a1a1a;margin-bottom:8px;text-align:left}
.btn-estrella{background:#FFD700;color:black;border:none;padding:8px 12px;border-radius:10px;font-weight:bold;cursor:pointer;margin:2px}
.btn-yellow{background:#FFD700;color:black;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}
.btn-green{background:#25D366;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:12px;display:block;text-decoration:none}
.chart{width:100%;height:180px;margin-top:10px;border-radius:10px;background:#0f0f0f}
</style></head><body>
<div class="header"><h1 style="color:#FFD700;">🔥 RAUDY ORO PRO + IA SWING + 50 🔥</h1><div style="background:#FFD700;color:black;padding:6px;border-radius:8px;font-weight:bold;font-size:12px;">🇨🇭 CREADO POR RAUDY EN GINEBRA SUIZA</div><div>⏰ TU VIP VENCE EN __DIAS__ DIAS - __FECHA__</div><div><a href="/logout" style="color:#ff4444;font-size:11px;">SALIR</a></div></div>
<div class="maestro-box"><div style="font-weight:bold;color:#FFD700;font-size:18px;">👑 MAESTRO SUPREMO - 50 ANALIZADORES - CON 35 = DIOS</div><div id="luz-maestro" class="luz-grande"></div><div id="maestro-texto" style="font-size:18px;font-weight:bold;">ESPERANDO MAESTRO...</div><div id="maestro-votos" style="font-size:12px;color:#aaa;">--</div><div id="maestro-lista" style="font-size:11px;text-align:left;max-height:120px;overflow:auto;margin-top:8px;"></div></div>
<div class="maestro-box" style="border-color:#00ff00;"><div style="font-weight:bold;color:#00ff00;font-size:18px;">🤖 50 ROBOTS RAUDY - CADA UNO HACE SU TRABAJO Y HABLAN ENTRE ELLOS</div><div style="font-size:12px;color:#aaa;">Si un robot hace bien su trabajo, dale ⭐. El que tenga mas estrellas, el Maestro le hace mas caso.</div><div id="chat-robots" style="background:#0a0a0a;border-radius:10px;padding:10px;text-align:left;font-size:12px;margin-top:10px;">Esperando que los robots hablen...</div><div style="font-weight:bold;color:#FFD700;margin-top:12px;">🏆 TOP 5 ROBOTS CON MAS ESTRELLAS</div><div id="top-robots" style="font-size:12px;text-align:left;margin-top:6px;">--</div><button onclick="cargarRobots()" style="background:#FFD700;color:black;border:none;padding:12px;border-radius:10px;font-weight:bold;width:100%;margin-top:10px;cursor:pointer;">🤖 VER LOS 50 ROBOTS Y DARLES ESTRELLA ⭐</button><div id="lista-robots" style="margin-top:10px;max-height:400px;overflow:auto;"></div></div>
<div class="box"><div style="font-weight:bold;">🌍 RELOJ MUNDIAL RAUDY</div><div id="reloj-texto" style="font-size:14px;font-weight:bold;">REVISANDO...</div><div id="reloj-sesion" style="font-size:12px;color:#FFD700;">--</div><div style="display:flex;gap:6px;margin-top:8px;font-size:11px;"><div style="flex:1;background:#1a1a1a;border-radius:8px;padding:6px;">🇨🇭 GINEBRA<br><b id="h-ginebra">--:--</b></div><div style="flex:1;background:#1a1a1a;border-radius:8px;padding:6px;">🇬🇧 LONDRES<br><b id="h-londres">--:--</b></div><div style="flex:1;background:#1a1a1a;border-radius:8px;padding:6px;">🇺🇸 NEW YORK<br><b id="h-ny">--:--</b></div><div style="flex:1;background:#1a1a1a;border-radius:8px;padding:6px;">🇯🇵 TOKIO<br><b id="h-tokio">--:--</b></div></div></div>
<div class="box"><div style="font-weight:bold;">🛡️ FILTRO DE NOTICIAS RAUDY</div><div id="filtro-texto">REVISANDO FILTRO...</div></div>
<div class="box" style="border-color:#00ff00;"><div style="font-weight:bold;color:#00ff00;">🤖 IA RAUDY - ANALISIS SWING</div><div id="ia-señal" style="font-size:18px;font-weight:bold;">ANALIZANDO...</div><div id="ia-analisis" style="font-size:12px;">Esperando...</div><div>TP: <span id="ia-tp">--</span> | SL: <span id="ia-sl">--</span> | Confianza: <span id="ia-conf">--</span> | Entrada: <span id="ia-entrada">--</span></div><div>Botin: <span id="ghost-botin">--</span> | Entrada: <span id="ghost-entrada">--</span> | Salida: <span id="ghost-salida">--</span></div></div>
<div class="box"><div style="font-weight:bold;">💰 MI OPERACION - TP Y SL</div><input id="mi-entrada" type="number" placeholder="Donde compraste Ej 3880" style="padding:12px;width:90%"><br><br><input id="mi-ganar" type="number" value="50" style="padding:12px;width:90%"><br><br><input id="mi-perder" type="number" value="20" style="padding:12px;width:90%"><br><br><button onclick="calcularMiOp('COMPRA')" style="background:#00aa00;color:white;padding:12px;border:none;border-radius:10px;font-weight:bold;">COMPRE AQUI</button> <button onclick="calcularMiOp('VENTA')" style="background:#ff0000;color:white;padding:12px;border:none;border-radius:10px;font-weight:bold;">VENDI AQUI</button><div id="mi-resultado" style="display:none;margin-top:10px;"><div id="mi-titulo"></div><div id="mi-texto"></div><div>TP: <span id="mi-tp">--</span> | SL: <span id="mi-sl">--</span></div></div></div>
<div class="box"><div style="font-weight:bold;">🟡 ORO (XAUUSD) - EN VIVO</div><div class="precio" id="oro">$3951.70</div><div style="font-size:11px;">COMPRA: 3900 - 3890 - 3865 | VENTA: 3980 - 3990 - 4020</div><div id="estado-oro">ESPERANDO</div><div id="texto-luz">ESPERANDO</div><div class="chart" id="chart-oro"></div></div>
<div class="box"><div style="font-weight:bold;">📜 HISTORIAL</div><div id="historial-lista" style="font-size:12px;text-align:left;">--</div></div>
<div class="box"><div style="font-weight:bold;">💷 GBPUSD</div><div class="precio" id="gbp">1.3412</div><div class="chart" id="chart-gbp"></div></div>
<div class="box"><div style="font-weight:bold;">💶 EURUSD</div><div class="precio" id="eur">1.1197</div><div class="chart" id="chart-eur"></div></div>
<div class="box"><div style="font-weight:bold;">🚗 TESLA</div><div class="precio" id="tesla">$245.80</div><div class="chart" id="chart-tesla"></div></div>
<div class="box"><div style="font-weight:bold;">🍎 APPLE</div><div class="precio" id="apple">$185.30</div><div class="chart" id="chart-apple"></div></div>
<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20</a>
<a href="https://wa.me/41767574050" class="btn-green">📱 WHATSAPP RAUDY</a>
<div style="text-align:center;font-size:10px;color:#666;padding:10px;">© 2026 Raudy Manzueta - Ginebra Suiza - Solo Educativo - Vence __FECHA__</div>
<script>
async function cargarRobots(){
  try{
    let r = await fetch('/api/robots');
    let d = await r.json();
    let html = '';
    d.robots.forEach(function(robot){
      html += '<div class="robot-card"><b>Robot '+robot.id+' - '+robot.nombre+'</b><br><span style="font-size:11px;color:#aaa;">'+robot.trabajo+'</span><br><span style="color:#FFD700;">Estrellas: '+robot.estrellas+' | Puntos: '+robot.puntos+'</span><br><span style="font-size:11px;">'+robot.mensaje+'</span><br><button class="btn-estrella" onclick="darEstrella('+robot.id+',1)">⭐ +1</button><button class="btn-estrella" onclick="darEstrella('+robot.id+',2)">⭐⭐ +2</button><button class="btn-estrella" onclick="darEstrella('+robot.id+',3)">⭐⭐⭐ +3 DIOS</button></div>';
    });
    document.getElementById('lista-robots').innerHTML = html;
  }catch(e){}
}
async function darEstrella(id, cantidad){
  try{
    let r = await fetch('/api/dar_estrella', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({id:id, estrellas:cantidad})});
    let d = await r.json();
    alert(d.mensaje || 'Estrella dada');
    cargarRobots();
  }catch(e){ alert('Error'); }
}
function sonidoPrueba(){ try{ let a=new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg'); a.play(); }catch(e){} }
function calcularMiOp(tipo){
  let entrada = parseFloat(document.getElementById('mi-entrada').value);
  let ganar = parseFloat(document.getElementById('mi-ganar').value);
  let perder = parseFloat(document.getElementById('mi-perder').value);
  if(!entrada || !ganar || !perder){ alert('Pon los 3 numeros'); return; }
  let tp, sl;
  if(tipo === 'COMPRA'){ tp = entrada + ganar; sl = entrada - perder; } else { tp = entrada - ganar; sl = entrada + perder; }
  document.getElementById('mi-resultado').style.display = 'block';
  document.getElementById('mi-titulo').innerText = tipo + ' EN $' + entrada.toFixed(2);
  document.getElementById('mi-texto').innerText = 'Pon esto en tu broker';
  document.getElementById('mi-tp').innerText = '$' + tp.toFixed(2);
  document.getElementById('mi-sl').innerText = '$' + sl.toFixed(2);
  document.getElementById('ghost-entrada').innerText = '$' + entrada.toFixed(2);
  document.getElementById('ghost-botin').innerText = '$' + tp.toFixed(2);
  document.getElementById('ghost-salida').innerText = '$' + sl.toFixed(2);
}
function makeCandleChart(elemId){ const chart = LightweightCharts.createChart(document.getElementById(elemId), {layout:{background:{color:'#0f0f0f'}, textColor:'#888'}, grid:{vertLines:{color:'#222'}, horzLines:{color:'#222'}}, width: document.getElementById(elemId).clientWidth, height: 180}); const series = chart.addCandlestickSeries({upColor:'#00ff00', downColor:'#ff4444', borderVisible:false, wickUpColor:'#00ff00', wickDownColor:'#ff4444'}); return {chart:chart, series:series, data:[]}; }
let charts = {oro: makeCandleChart('chart-oro'), gbp: makeCandleChart('chart-gbp'), eur: makeCandleChart('chart-eur'), tesla: makeCandleChart('chart-tesla'), apple: makeCandleChart('
