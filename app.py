from flask import Flask, session, request, redirect, jsonify
import requests, threading, time, os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cambia-esto")
CLAVE_BUENA = os.getenv("VIP_CLAVE", "RAUDY26")
FECHA_VENCE = datetime(2026, 12, 3, 23, 59, 59)
BOT_TOKEN = os.getenv("BOT_TOKEN", "AQUI_PON_TU_TOKEN_DEL_BOTFATHER")
CHAT_ID_VIP = os.getenv("CHAT_ID", "AQUI_PON_TU_ID_O_DEL_CANAL")
BOT_USERNAME = os.getenv("BOT_USERNAME", "raudy_vip_oro_bot")
COMPRAS = [3900, 3890, 3865]
VENTAS = [3980, 3990, 4020]
alertado_compra = {p: False for p in COMPRAS}
alertado_venta = {p: False for p in VENTAS}
historial_oro = []
historial_senales = []
# 50 ROBOTS
NOMBRES = ["Cazador Rapido","Relampago Oro","Flecha Veloz","Ojo Aguila","Tiburon Oro","Ninja Precio","Rayo Londres","Trueno NY","Guardian Scalping","Maestro Scalping","Rey Londres","Reina Londres","Guardian Londres","Cazador Londres","Jefe Londres","Rey NY","Reina NY","Guardian NY","Cazador NY","Jefe NY","Ojo Noticias","Alarma Noticias","Guardian Noticias","Cazador Noticias","Jefe Noticias","Soporte 3900","Soporte 3890","Soporte 3865","Resistencia 3980","Resistencia 4020","Robot DIOS 1","Robot DIOS 2","Robot DIOS 3","Robot DIOS 4","Robot DIOS 5","Robot DIOS 6","Robot DIOS 7","Robot DIOS 8","Robot DIOS 9","Robot DIOS 10","Guardian Capital","Guardian Fin Semana","Guardian Cuenta","Guardian Familia","Guardian Anti-Perdida","Guardian Modo Nino","Guardian Psicologia","Guardian Copia Segura","Guardian Idioma","MAESTRO SUPREMO"]
ROBOTS_RAUDY = [{"id": i+1, "nombre": n, "trabajo": "Trabaja con el equipo", "estrellas": 0, "puntos": 0, "mensaje": "Listo"} for i, n in enumerate(NOMBRES)]
def hora_ginebra():
    return datetime.utcnow() + timedelta(hours=1)
def dias_restantes():
    return max(0, (FECHA_VENCE - hora_ginebra()).days)
def codigo_vigente():
    return hora_ginebra() <= FECHA_VENCE
def filtro_noticias(precio):
    h = hora_ginebra().hour
    m = hora_ginebra().minute
    if h == 14 and 25 <= m <= 59:
        return {"texto": "🔴 NO OPERES - NOTICIAS USA 14:30", "color": "#ff0000", "puede": False}
    if h == 8 and 25 <= m <= 45:
        return {"texto": "🔴 NO OPERES - NOTICIAS 08:30", "color": "#ff0000", "puede": False}
    if len(historial_oro) >= 5 and abs(precio - historial_oro[-5]) > 25:
        return {"texto": "🟡 CUIDADO - MERCADO LOCO", "color": "#FFA500", "puede": True}
    return {"texto": "🟢 FILTRO OK - PUEDES OPERAR", "color": "#00aa00", "puede": True}
def reloj_mundial():
    g = hora_ginebra()
    l = g - timedelta(hours=1)
    n = g - timedelta(hours=6)
    t = g + timedelta(hours=8)
    dias = ["LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","SABADO","DOMINGO"]
    dia = dias[g.weekday()]
    base = {"dia": dia, "hora_ginebra": g.strftime("%H:%M"), "hora_londres": l.strftime("%H:%M"), "hora_ny": n.strftime("%H:%M"), "hora_tokio": t.strftime("%H:%M")}
    if g.weekday() >= 5:
        base.update({"texto": "🔴 HOY " + dia + " - MERCADO CERRADO", "color": "#ff0000", "sesion": "CERRADO", "puede": False})
    elif 9 <= g.hour < 11:
        base.update({"texto": "🟢 HOY " + dia + " - SESION LONDRES", "color": "#00aa00", "sesion": "LONDRES", "puede": True})
    elif (g.hour == 14 and g.minute >= 30) or (15 <= g.hour < 17):
        base.update({"texto": "🟢🟢 HOY " + dia + " - SESION NEW YORK - MEJOR HORA", "color": "#00aa00", "sesion": "NEW YORK", "puede": True})
    elif 2 <= g.hour < 6:
        base.update({"texto": "🔴 SESION ASIA - DORMIDO", "color": "#ff0000", "sesion": "ASIA", "puede": False})
    elif g.hour >= 22 or g.hour < 2:
        base.update({"texto": "🔴 MERCADO DE NOCHE", "color": "#ff0000", "sesion": "NOCHE", "puede": False})
    else:
        base.update({"texto": "🟡 ENTRE SESIONES - ESPERA 09:00 O 14:30", "color": "#FFA500", "sesion": "ENTRE SESIONES", "puede": True})
    return base
def get_price_yahoo(s, fb):
    try:
        r = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/' + s, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        return float(r.json()['chart']['result'][0]['meta']['regularMarketPrice'])
    except:
        return fb
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
    if precio <= 3905 and precio >= 3860:
        res = {"señal": "🟢 COMPRA SWING", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA", "analisis": "IA: Oro en zona 3900-3865. Es COMPRA.", "entrada": precio, "tp": round(precio + 35, 2), "sl": round(precio - 18, 2), "confianza": "88%"}
    elif precio >= 3980 and precio <= 4030:
        res = {"señal": "🔴 VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA", "analisis": "IA: Oro en zona 3980-4020. Es VENTA.", "entrada": precio, "tp": round(precio - 35, 2), "sl": round(precio + 18, 2), "confianza": "88%"}
    elif precio > 4030:
        res = {"señal": "🔴 YA PASO VENTA - ESPERA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 YA PASO VENTA", "analisis": "IA: Ya paso venta. Espera 3980 o 3900.", "entrada": precio, "tp": 3980, "sl": round(precio + 20, 2), "confianza": "65%"}
    elif precio > 3940:
        res = {"señal": "🔴 ESPERANDO VENTA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 ESPERANDO VENTA", "analisis": "IA: Espera 3980 venta o 3900 compra.", "entrada": precio, "tp": 3900, "sl": 4040, "confianza": "65%"}
    elif precio < 3940 and precio > 3905:
        res = {"señal": "🟡 CERCA DE COMPRA", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 CERCA DE COMPRA", "analisis": "IA: Se acerca a compra. Si toca 3900 es COMPRA.", "entrada": 3900, "tp": 3935, "sl": 3882, "confianza": "70%"}
    else:
        res = {"señal": "🟡 ANALIZANDO", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 ANALIZANDO", "analisis": "IA: Analizando...", "entrada": precio, "tp": round(precio + 30, 2), "sl": round(precio - 15, 2), "confianza": "50%"}
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
    f = filtro_noticias(precio)
    for i in range(3, 50):
        if i in [4, 26]:
            votos.append((str(i) + " NOTICIAS", "ESPERA" if not f["puede"] else "COMPRA" if precio < 3940 else "VENTA"))
        elif i in [15, 32, 38, 40, 43, 48, 49]:
            votos.append((str(i) + " ANALIZADOR", "ESPERA"))
        elif i in [3, 12, 21]:
            votos.append((str(i) + " TENDENCIA", "COMPRA" if precio > 3940 else "VENTA"))
        else:
            votos.append((str(i) + " ANALIZADOR", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    c_compra = sum(1 for _, v in votos if v == "COMPRA")
    c_venta = sum(1 for _, v in votos if v == "VENTA")
    c_espera = sum(1 for _, v in votos if v == "ESPERA")
    if c_compra >= 35:
        m = {"señal": "👑🔥 COMPRA DIOS - LA MEJOR DEL DIA", "color": "#00ff00", "luz": "#00ff00", "texto_luz": "🟢 COMPRA DIOS"}
    elif c_venta >= 35:
        m = {"señal": "👑🔥 VENTA DIOS - LA MEJOR DEL DIA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 VENTA DIOS"}
    elif c_compra > c_venta + 5:
        m = {"señal": "🟢 COMPRA FUERTE", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 COMPRA"}
    elif c_venta > c_compra + 5:
        m = {"señal": "🔴 VENTA FUERTE", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 VENTA"}
    else:
        m = {"señal": "🟡 ESPERA - LOS 50 NO ESTAN DE ACUERDO", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 ESPERA"}
    m["votos_compra"] = c_compra
    m["votos_venta"] = c_venta
    m["votos_espera"] = c_espera
    m["lista"] = votos
    m["total"] = 50
    return m
def chat_robots(precio, maestro):
    if precio <= 3910:
        return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro bajo, yo digo COMPRA"}, {"robot": "Robot 18 Guardian NY", "texto": "Confirmo COMPRA"}, {"robot": "Robot 50 MAESTRO", "texto": "Decido: " + maestro["señal"]}]
    if precio >= 3970:
        return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro subio, yo digo VENTA"}, {"robot": "Robot 16 Rey NY", "texto": "Confirmo VENTA"}, {"robot": "Robot 50 MAESTRO", "texto": "Decido: " + maestro["señal"]}]
    return [{"robot": "Robot 5 Tiburon Oro", "texto": "Oro en medio, ESPERA"}, {"robot": "Robot 50 MAESTRO", "texto": "Decido: " + maestro["señal"]}]
def send_telegram(msg):
    try:
        if "AQUI_PON" in BOT_TOKEN:
            return
        url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
        for cid in CHAT_ID_VIP.split(","):
            cid = cid.strip()
            if cid and "AQUI_PON" not in cid:
                requests.post(url, json={"chat_id": cid, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except:
        pass
def bot_loop():
    while True:
        try:
            p = get_oro_precio()
            ia = analizar_ia_oro(p)
            for niv in COMPRAS:
                if p <= niv and not alertado_compra[niv]:
                    send_telegram("🔥 RAUDY ORO - COMPRA - Oro toco " + str(niv))
                    alertado_compra[niv] = True
                if p > niv + 40:
                    alertado_compra[niv] = False
            for niv in VENTAS:
                if p >= niv and not alertado_venta[niv]:
                    send_telegram("🔴 RAUDY ORO - VENTA - Oro toco " + str(niv))
                    alertado_venta[niv] = True
                if p < niv - 40:
                    alertado_venta[niv] = False
        except:
            pass
        time.sleep(60)
threading.Thread(target=bot_loop, daemon=True).start()
def esta_logueado():
    return codigo_vigente() and session.get("vip") == CLAVE_BUENA
@app.route('/login', methods=['GET','POST'])
def login():
    if not codigo_vigente():
        return '<h1>CODIGO VENCIDO</h1><a href="https://www.paypal.me/RaudyManzueta/20">PAGAR $20</a>'
    error = ""
    if request.method == 'POST':
        if request.form.get("clave","").strip().upper() == CLAVE_BUENA:
            session["vip"] = CLAVE_BUENA
            return redirect("/")
        error =
