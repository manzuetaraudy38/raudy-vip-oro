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
            return {"texto": f"🟡 CUIDADO - MERCADO LOCO SE MOVIO ${cambio:.2f} RAPIDO - ESPERA QUE SE CALME", "color": "#FFA500", "puede": True}
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
    minuto = ahora_ginebra.minute
    if dia_semana >= 5:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🔴 HOY ES {dia_nombre} - MERCADO CERRADO - NO SE COMPRA ORO - DESCANSA", "color": "#ff0000", "sesion": "MERCADO CERRADO", "puede": False}
    if 9 <= hora_g < 11:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🟢 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - SESION LONDRES - BUENA HORA PARA COMPRAR ORO", "color": "#00aa00", "sesion": "LONDRES 🟢", "puede": True}
    if (hora_g == 14 and minuto >= 30) or (15 <= hora_g < 17):
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🟢🟢 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - SESION NEW YORK - LA MEJOR HORA PARA COMPRAR / VENDER ORO", "color": "#00aa00", "sesion": "NEW YORK 🟢🟢 MEJOR HORA", "puede": True}
    if 2 <= hora_g < 6:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🔴 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - SESION ASIA - MERCADO DORMIDO - NO COMPRES ORO AHORA", "color": "#ff0000", "sesion": "ASIA 🔴 DORMIDO", "puede": False}
    if hora_g >= 22 or hora_g < 2:
        return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🔴 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - MERCADO DE NOCHE - NO HAY GENTE - NO COMPRES", "color": "#ff0000", "sesion": "NOCHE 🔴", "puede": False}
    return {"dia": dia_nombre, "hora_ginebra": ahora_ginebra.strftime("%H:%M"), "hora_londres": hora_londres.strftime("%H:%M"), "hora_ny": hora_ny.strftime("%H:%M"), "hora_tokio": hora_tokio.strftime("%H:%M"), "texto": f"🟡 HOY {dia_nombre} {ahora_ginebra.strftime('%H:%M')} - ENTRE SESIONES - ESPERA A LAS 09:00 O 14:30 PARA COMPRAR", "color": "#FFA500", "sesion": "ENTRE SESIONES 🟡", "puede": True}

def get_price_yahoo(symbol, fallback):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
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
        res = {"señal": "🟢 COMPRA SWING", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA SWING", "analisis": f"IA SWING: Oro hizo SWING BAJO en {min_reciente:.2f} en zona 3900-3865. Bajó y ahora rebota para subir. Es zona de COMPRA.", "entrada": precio, "tp": round(precio + 35, 2), "sl": round(precio - 18, 2), "confianza": "88%"}
    elif precio >= 3980 and precio <= 4030:
        res = {"señal": "🔴 VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA SWING", "analisis": f"IA SWING: Oro hizo SWING ALTO en {max_reciente:.2f} en zona 3980-4020. Subió mucho y ahora va a bajar. Es zona de VENTA.", "entrada": precio, "tp": round(precio - 35, 2), "sl": round(precio + 18, 2), "confianza": "88%"}
    elif precio > 4030:
        res = {"señal": "🔴 YA PASO ZONA VENTA - ESPERA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - YA PASO VENTA", "analisis": f"IA SWING: Oro alto en ${precio:.2f}. YA PASO la zona de venta 3980-4020. NO persigas la venta aquí. Espera que baje a 3980 para venta o a 3900 para compra. Swing Alto {max_reciente:.2f} / Bajo {min_reciente:.2f}", "entrada": precio, "tp": 3980, "sl": round(precio + 20, 2), "confianza": "65%"}
    elif precio > 3940:
        res = {"señal": "🔴 ESPERANDO VENTA SWING", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - ESPERANDO VENTA", "analisis": f"IA SWING: Oro en ${precio:.2f}. No compres aquí. Swing Alto {max_reciente:.2f} / Bajo {min_reciente:.2f}. Espera que suba a 3980 para venta o baje a 3900 para compra.", "entrada": precio, "tp": 3900, "sl": 4040, "confianza": "65%"}
    elif precio < 3940 and precio > 3905:
        res = {"señal": "🟡 CERCA DE COMPRA SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 LUZ NARANJA - CERCA DE COMPRA", "analisis": f"IA SWING: Oro en ${precio:.2f} se acerca a compra. Si toca 3900 es SWING BAJO = COMPRA. Bajo reciente {min_reciente:.2f}", "entrada": 3900, "tp": 3935, "sl": 3882, "confianza": "70%"}
    else:
        res = {"señal": "🟡 ANALIZANDO SWING", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 ANALIZANDO", "analisis": f"IA: Analizando swing... Precio ${precio:.2f}. Alto {max_reciente:.2f} Bajo {min_reciente:.2f}. Espera señal clara.", "entrada": precio, "tp": round(precio + 30, 2), "sl": round(precio - 15, 2), "confianza": "50%"}
    res["botin"] = res["tp"]
    res["salida_emergencia"] = res["sl"]
    res["entrada_grafico"] = res["entrada"]
    return res

# ===== RAUDY - 50 ANALIZADORES - CON 28 = DIOS =====
def analizar_50_raudy(precio, eur_val, gbp_val):
    votos = []
    if precio <= 3905:
        votos.append(("1 SWING", "COMPRA"))
    elif precio >= 3980:
        votos.append(("1 SWING", "VENTA"))
    else:
        votos.append(("1 SWING", "ESPERA"))
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
    votos.append(("7 SOPORTE Y RESISTENCIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
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
    votos.append(("25 MIEDO DEL MERCADO", "ESPERA" if abs(precio-3940)<10 else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("26 HORA DE NOTICIA", "ESPERA" if not f["puede"] else "COMPRA" if precio<3940 else "VENTA"))
    votos.append(("27 REBOTE", "COMPRA" if precio <= 3910 else "ESPERA"))
    votos.append(("28 TRAMPA", "ESPERA" if 3935 <= precio <= 3945 else "COMPRA" if precio<3935 else "VENTA"))
    votos.append(("29 GUARDIAN DE CUENTA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("30 MAESTRO SUPREMO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("31 HISTORIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("32 CAZADOR NOCTURNO", "ESPERA"))
    votos.append(("33 ANTI-PERDIDA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("34 DOBLE CONFIRMACION", "COMPRA" if precio <= 3905 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("35 MAESTRO SUPREMO FINAL", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("36 APERTURA LONDRES", "COMPRA" if 9 <= hora_ginebra().hour < 11 and precio <= 3920 else "ESPERA"))
    votos.append(("37 APERTURA NEW YORK", "COMPRA" if 14 <= hora_ginebra().hour < 17 and precio <= 3920 else "VENTA" if 14 <= hora_ginebra().hour < 17 and precio >= 3970 else "ESPERA"))
    votos.append(("38 GAP", "ESPERA"))
    votos.append(("39 SPREAD", "COMPRA" if precio < 3940 else "VENTA"))
    votos.append(("40 SWAP", "ESPERA"))
    votos.append(("41 PATRONES", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("42 PIVOT", "COMPRA" if precio <= 3900 else "VENTA" if precio >= 3980 else "ESPERA"))
    votos.append(("43 PSICOLOGIA", "ESPERA"))
    votos.append(("44 COPIA SEGURA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("45 ALERTA FAMILIA", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("46 MODO NIÑO", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("47 PROTECTOR DE CAPITAL", "ESPERA" if precio > 4030 else "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    votos.append(("48 MODO OSCURO Y CLARO", "ESPERA"))
    votos.append(("49 IDIOMA", "ESPERA"))
    c_compra = sum(1 for _, v in votos if v == "COMPRA")
    c_venta = sum(1 for _, v in votos if v == "VENTA")
    c_espera = sum(1 for _, v in votos if v == "ESPERA")
    # === RAUDY QUIERE 28 = DIOS - YA CAMBIADO ===
    if c_compra >= 28:
        maestro = {"señal": "👑🔥 COMPRA DIOS - LA MEJOR DEL DIA", "color": "#00ff00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE FUERTE - COMPRA DIOS"}
    elif c_venta >= 28:
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
            print("FALTA BOT_TOKEN")
            return
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        for chat_id in CHAT_ID_VIP.split(","):
            chat_id = chat_id.strip()
            if not chat_id or "AQUI_PON" in chat_id:
                continue
            payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error telegram: {e}")

def telegram_bot_loop():
    global ultimo_update_id, alertado_compra, alertado_venta
    print("🤖 BOT TELEGRAM INICIADO - 6 ALERTAS + IA SWING + 50 ANALIZADORES")
    send_telegram(f"✅ *VIP ORO Raudy ACTIVO + IA SWING + 50 ANALIZADORES*\n\nTe avisaré automático:\n🟢 COMPRA: 3900, 3890, 3865\n🔴 VENTA: 3980, 3990, 4020\n\n📲 APP: raudy-vip-oro.onrender.com\nVence: {FECHA_VENCE.strftime('%d/%m/%Y')}")
    while True:
        try:
            if "AQUI_PON" not in BOT_TOKEN:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
                params = {"offset": ultimo_update_id + 1, "timeout": 5}
                resp = requests.get(url, params=params, timeout=10).json()
                if resp.get("ok"):
                    for upd in resp.get("result", []):
                        ultimo_update_id = upd["update_id"]
                        msg = upd.get("message", {})
                        texto = msg.get("text", "").lower().strip()
                        if texto in ["/start", "start", "hola", "hi"]:
                            send_telegram(f"🔥 *RAUDY ORO PRO VIP + IA SWING + 50 ANALIZADORES*\n\nBienvenido! Estás activo.\n🟢 BUY: 3900, 3890, 3865\n🔴 SELL: 3980, 3990, 4020\nAPP: raudy-vip-oro.onrender.com\n\nEscribe /precios para ver ORO ahora")
                        elif texto in ["/precios", "precios", "oro"]:
                            precio = get_oro_precio()
                            ia = analizar_ia_oro(precio)
                            filtro = filtro_noticias(precio)
                            reloj = reloj_mundial()
                            send_telegram(f"🟡 ORO AHORA: ${precio:.2f}\n{ia['señal']}\n🟡 ENTRADA: ${ia['entrada_grafico']}\n🟢 BOTIN: ${ia['botin']} | 🔴 SALIDA: ${ia['salida_emergencia']}\n{reloj['texto']}\n{filtro['texto']}\n{ia['analisis']}")
            precio = get_oro_precio()
            ia = analizar_ia_oro(precio)
            print(f"{hora_ginebra()} - ORO: {precio} IA: {ia['señal']}")
            for nivel in COMPRAS:
                if precio <= nivel and not alertado_compra[nivel]:
                    send_telegram(f"🔥 *RAUDY ORO - COMPRA SWING + IA*\n\nORO TOCO *${nivel}*\nActual: ${precio:.2f}\n🟡 ENTRADA: ${ia['entrada_grafico']}\n🟢 BOTIN: ${ia['botin']} | 🔴 SALIDA: ${ia['salida_emergencia']}\n{ia['analisis']}\n\n📲 raudy-vip-oro.onrender.com")
                    alertado_compra[nivel] = True
                if precio > nivel + 40:
                    alertado_compra[nivel] = False
            for nivel in VENTAS:
                if precio >= nivel and not alertado_venta[nivel]:
                    send_telegram(f"🔴 *RAUDY ORO - VENTA SWING + IA*\n\nORO TOCO *${nivel}*\nActual: ${precio:.2f}\n🟡 ENTRADA: ${ia['entrada_grafico']}\n🟢 BOTIN: ${ia['botin']} | 🔴 SALIDA: ${ia['salida_emergencia']}\n{ia['analisis']}\n\n📲 raudy-vip-oro.onrender.com")
                    alertado_venta[nivel] = True
                if precio < nivel - 40:
                    alertado_venta[nivel] = False
        except Exception as e:
            print(f"Error loop bot: {e}")
        time.sleep(60)

threading.Thread(target=telegram_bot_loop, daemon=True).start()

def esta_logueado():
    if not codigo_vigente():
        return False
    return session.get("vip") == CLAVE_BUENA

@app.route('/login', methods=['GET','POST'])
def login():
    if not codigo_vigente():
        return f'<body style="background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:20px"><div style="border:3px solid red;border-radius:20px;padding:25px;background:#1a0a0a;max-width:400px;margin:40px auto"><h1 style="color:red">⛔ CODIGO VENCIDO</h1><p>Tu VIP venció el {FECHA_VENCE.strftime("%d/%m/%Y")}</p><a href="https://www.paypal.me/RaudyManzueta/20" style="background:gold;color:black;padding:15px;display:block;border-radius:12px;text-decoration:none;font-weight:bold">💳 PAGAR $20</a><br><a href="https://wa.me/41767574050" style="background:#25D366;color:white;padding:15px;display:block;border-radius:12px;text-decoration:none;font-weight:bold">📱 WHATSAPP RAUDY</a></div></body>'
    error = ""
    dias = dias_restantes()
    if request.method == 'POST':
        clave = request.form.get("clave","").strip().upper()
        if clave == CLAVE_BUENA:
            session["vip"] = CLAVE_BUENA
            return redirect("/")
        error = "❌ CLAVE MALA - Revisa tu WhatsApp"
    return f'''
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY VIP</title>
<style>
body{{background:#0a0a0a;color:white;font-family:Arial;margin:0;padding:15px;text-align:center}}
.box{{border:2px solid #FFD700;border-radius:20px;padding:25px;background:#1a1a1a;max-width:400px;margin:40px auto}}
input{{width:90%;padding:18px;border-radius:12px;border:2px solid #FFD700;background:#0a0a0a;color:#FFD700;font-size:22px;text-align:center;font-weight:bold;margin:15px 0}}
.btn{{background:#FFD700;color:black;border-radius:15px;padding:18px;font-weight:bold;font-size:18px;width:100%;border:none;cursor:pointer}}
.btn-yellow{{background:#FFD700;color:black;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-blue{{background:#0a84ff;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-green{{background:#25D366;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:12px;display:block;text-decoration:none}}
.btn-telegram{{background:#229ED9;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:12px;display:block;text-decoration:none}}
.warn{{border:1px solid #ff4444;background:#1a0a0a;border-radius:12px;padding:12px;font-size:10px;color:#ffaaaa;text-align:left;margin-top:15px;line-height:1.4}}
.vence{{background:#FFD700;color:black;padding:8px;border-radius:8px;font-weight:bold;font-size:12px;margin-bottom:10px}}
</style></head><body>
<div class="box">
<h1 style="color:#FFD700;">🔒 RAUDY ORO PRO VIP</h1>
<div style="background:#FFD700;color:black;padding:6px;border-radius:8px;font-weight:bold;font-size:12px;margin-bottom:10px;">🇨🇭 CREADO POR RAUDY EN GINEBRA SUIZA - APP ÚNICA</div>
<div class="vence">⏰ VENCE EN {dias} DIAS - {FECHA_VENCE.strftime("%d/%m/%Y")}</div>
<form method="POST">
<input name="clave" placeholder="ESCRIBE TU CLAVE VIP" required>
<div style="color:#ff4444;font-weight:bold;margin:10px;">{error}</div>
<button class="btn">🔓 ENTRAR VIP</button>
</form>
<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050</a>
<a href="https://t.me/{BOT_USERNAME}?start=Hola_Raudy_quiero_VIP" target="_blank" class="btn-telegram">✈️ TELEGRAM - CONECTAR CON MI ROBOT</a>
<div class="warn"><b>⚠️ ADVERTENCIA DE RIESGO:</b> Solo educativo. No es consejo financiero. Trading Oro, Forex, Tesla, Apple es ALTO RIESGO. Puedes perder tu dinero. Vence en {dias} dias.</div>
</div></body></html>'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route('/api/precios')
def precios():
    if not esta_logueado():
        return jsonify({"error": "no autorizado o vencido"}), 401
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
    historial_senales.append({"hora": hora_ginebra().strftime("%H:%M"), "precio": oro_f, "señal": maestro50["señal"]})
    if len(historial_senales) > 100:
        historial_senales.pop(0)
    return {"oro": oro_f,"gbp": gbp_v,"eur": eur_v,"tesla": tesla_v,"apple": apple_v,"ia": ia, "filtro": filtro, "reloj": reloj, "maestro50": maestro50, "historial": historial_senales[-20:]}

@app.route('/')
def home():
    if not esta_logueado():
        return redirect("/login")
    dias = dias_restantes()
    return f'''
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY ORO PRO</title>
<script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
<style>
body {{ background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:10px; }}
.header {{ text-align:center; padding:15px; border:2px solid #FFD700; border-radius:15px; background:#1a1a1a; margin-bottom:12px; }}
.header h1 {{ margin:0; color:#FFD700; font-size:26px; }}
.box {{ border:2px solid #FFD700; border-radius:15px; padding:12px; text-align:center; margin-bottom:14px; background:#1a1a1a; }}
.precio {{ font-size:32px; color:#00ff00; font-weight:bold; }}
.zonas {{ font-size:11px; margin-top:6px; line-height:1.4; }}
.estado {{ border-radius:10px; padding:8px; font-weight:bold; font-size:13px; margin-top:8px; }}
.chart {{ width:100%; height:180px; margin-top:10px; border-radius:10px; background:#0f0f0f; }}
.btn-yellow {{ background:#FFD700; color:black; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }}
.btn-blue {{ background:#0a84ff; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }}
.btn-green {{ background:#25D366; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:12px; display:block; text-decoration:none; }}
.btn-telegram {{ background:#229ED9; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:12px; display:block; text-decoration:none; }}
.footer {{ text-align:center; font-size:10px; color:#666; padding:10px; }}
.warn-main {{ border:2px solid #ff4444; background:#1a0a0a; border-radius:15px; padding:12px; font-size:10px; color:#ffaaaa; line-height:1.4; text-align:left; margin-bottom:14px; }}
.warn-title {{ color:#ff4444; font-weight:bold; font-size:11px; text-align:center; margin-bottom:6px; }}
.vence-top{{background:#FFD700;color:black;padding:6px;border-radius:8px;font-weight:bold;font-size:11px;margin-top:6px}}
.luz {{ width:30px; height:30px; border-radius:50%; background:#333; margin:10px auto 5px auto; }}
@keyframes parpadeo {{ 0%{{opacity:1}} 50%{{opacity:0.3}} 100%{{opacity:1}} }}
.luz-activa {{ animation: parpadeo 0.8s infinite; }}
.ia-box {{ border:2px solid #00ff00; border-radius:15px; padding:12px; background:#0a1a0a; margin-bottom:14px; text-align:left; }}
.tpsl {{ display:flex; gap:8px; margin-top:8px; }}
.tpsl div {{ flex:1; border-radius:10px; padding:10px; font-weight:bold; text-align:center; }}
.mi-op {{ border:2px solid #FFD700; border-radius:15px; padding:14px; background:#1a1a1a; margin-bottom:14px; text-align:left; }}
.mi-op input {{ width:100%; padding:14px; border-radius:10px; border:2px solid #FFD700; background:#0a0a0a; color:#FFD700; font-size:20px; text-align:center; font-weight:bold; margin:6px 0; box-sizing:border-box; }}
.mi-op label {{ font-size:12px; color:#aaa; }}
.btn-compra {{ background:#00aa00; color:white; border:none; border-radius:12px; padding:16px; font-weight:bold; font-size:16px; width:48%; cursor:pointer; }}
.btn-venta {{ background:#ff0000; color:white; border:none; border-radius:12px; padding:16px; font-weight:bold; font-size:16px; width:48%; cursor:pointer; }}
.ghost-box {{ border:2px solid #FFD700; border-radius:15px; padding:12px; background:#f5f0d5; color:black; margin-bottom:14px; text-align:left; }}
.ghost-line {{ display:flex; justify-content:space-between; align-items:center; margin:8px 0; padding:6px 8px; font-weight:bold; font-size:14px; }}
.ghost-botin {{ background:#009933; color:white; }}
.ghost-entrada {{ background:#FFD700; color:black; }}
.ghost-salida {{ background:#cc0000; color:white; }}
.ghost-dash {{ border-top:3px dashed; flex:1; margin:0 8px; }}
.filtro-box {{ border:2px solid #FFD700; border-radius:15px; padding:12px; background:#1a1a00; margin-bottom:14px; text-align:center; }}
.reloj-box {{ border:2px solid #00ff00; border-radius:15px; padding:12px; background:#0a1a0a; margin-bottom:14px; text-align:center; }}
.maestro-box {{ border:3px solid #FFD700; border-radius:15px; padding:12px; background:#1a1a00; margin-bottom:14px; text-align:center; }}
.luz-grande {{ width:60px; height:60px; border-radius:50%; background:#333; margin:10px auto; box-shadow:0 0 30px 10px #333; }}
</style></head><body>
<div class="header">
<h1>🔥 RAUDY ORO PRO + IA SWING + 50 🔥</h1>
<div style="background:#FFD700;color:black;padding:6px;border-radius:8px;font-weight:bold;font-size:12px;margin-top:6px;">🇨🇭 CREADO POR RAUDY EN GINEBRA SUIZA - APP ÚNICA EN EL MUNDO</div>
<div style="font-size:11px;color:#FFD700;margin-top:4px;">⭐ SOLO PARA VIP DE RAUDY - NO COPIAR ⭐</div>
<div style="font-size:11px; color:#aaa;">APP OFICIAL - VELAS EN VIVO + BOT TELEGRAM 6 ALERTAS + IA SWING + RELOJ MUNDIAL + 50 ANALIZADORES</div>
<div style="font-size:11px; color:#00ff00;" id="hora">VIVO - RAUDY ORO PRO - VIP ✅ - BOT ACTIVO + IA</div>
<div class="vence-top">⏰ TU VIP VENCE EN {dias} DIAS - {FECHA_VENCE.strftime("%d/%m/%Y")}</div>
<div style="margin-top:5px;"><a href="/logout" style="color:#ff4444; font-size:11px; text-decoration:none;">SALIR</a></div>
</div>

<div class="maestro-box">
<div style="font-weight:bold; color:#FFD700; font-size:18px;">👑 MAESTRO SUPREMO - 50 ANALIZADORES - LUZ - CON 28 = DIOS</div>
<div id="luz-maestro" class="luz-grande luz-activa"></div>
<div id="maestro-texto" style="font-size:18px;font-weight:bold;">ESPERANDO MAESTRO...</div>
<div id="maestro-votos" style="font-size:12px;color:#aaa;">--</div>
<div id="maestro-lista" style="font-size:11px;text-align:left;max-height:120px;overflow:auto;margin-top:8px;"></div>
<button onclick="document.getElementById('modal-como').style.display='block'" style="background:#FFD700;color:black;border:none;padding:12px;border-radius:10px;font-weight:bold;width:100%;margin-top:10px;cursor:pointer;">❓ ¿COMO USAR LA APP? - TOCA AQUI</button>
<button onclick="sonidoPrueba()" style="background:#00aa00;color:white;border:none;padding:12px;border-radius:10px;font-weight:bold;width:100%;margin-top:8px;cursor:pointer;">🔔 PROBAR SONIDO</button>
</div>

<div id="modal-como" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:9999;padding:20px;box-sizing:border-box;overflow:auto;">
<div style="background:white;color:black;border-radius:15px;padding:20px;max-width:400px;margin:20px auto;">
<h2>¿COMO USAR LA APP RAUDY?</h2>
<p>1. Mira la LUZ grande. Verde = compra, Roja = venta, Amarilla = espera.<br><br>2. Si el Maestro dice COMPRA DIOS o VENTA DIOS, es porque 28 de los 50 estan de acuerdo.<br><br>3. Pon tu TP y SL en tu broker tal cual.<br><br>4. Si el Filtro dice ROJO, NO operes aunque haya señal.<br><br>5. Solo educativo, no es consejo financiero. Puedes perder dinero.</p>
<button onclick="document.getElementById('modal-como').style.display='none'" style="background:red;color:white;padding:12px;border:none;border-radius:10px;width:100%;font-weight:bold;">CERRAR</button>
</div>
</div>

<div class="reloj-box">
<div style="font-weight:bold; color:#00ff00; font-size:16px;">🌍 RELOJ MUNDIAL RAUDY - ¿CUANDO COMPRAR ORO?</div>
<div id="reloj-texto" style="font-size:14px; font-weight:bold; margin-top:6px;">REVISANDO HORA MUNDIAL...</div>
<div style="display:flex; gap:6px; margin-top:8px; font-size:11px;">
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇨🇭 GINEBRA<br><b id="h-ginebra">--:--</b></div>
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇬🇧 LONDRES<br><b id="h-londres">--:--</b></div>
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇺🇸 NEW YORK<br><b id="h-ny">--:--</b></div>
<div style="flex:1; background:#1a1a1a; border-radius:8px; padding:6px;">🇯🇵 TOKIO<br><b id="h-tokio">--:--</b></div>
</div>
<div id="reloj-sesion" style="font-size:12px; font-weight:bold; margin-top:6px; color:#FFD700;">--</div>
<div style="font-size:11px; color:#aaa; margin-top:4px;">🟢 Mejor hora: 09:00-11:00 Londres y 14:30-17:00 New York | 🔴 No operes de noche ni fin de semana</div>
</div>
<div class="filtro-box">
<div style="font-weight:bold; color:#FFD700; font-size:16px;">🛡️ FILTRO DE NOTICIAS RAUDY</div>
<div id="filtro-texto" style="font-size:14px; font-weight:bold; margin-top:6px;">REVISANDO FILTRO...</div>
<div style="font-size:11px; color:#aaa; margin-top:4px;">Si dice ROJO = NO OPERES aunque haya señal</div>
</div>
<div class="warn-main">
<div class="warn-title">⚠️ ADVERTENCIA DE RIESGO - SOLO EDUCATIVO - BOT 6 ALERTAS ACTIVO + IA SWING</div>
<b>NO ES CONSEJO FINANCIERO.</b> 3 COMPRAS: 3900,3890,3865 | 3 VENTAS: 3980,3990,4020
</div>
<div class="ia-box">
<div style="font-weight:bold; color:#00ff00; font-size:16px;">🤖 IA RAUDY - ANALISIS SWING</div>
<div id="ia-señal" style="font-size:18px; font-weight:bold; margin:6px 0;">ANALIZANDO...</div>
<div id="ia-analisis" style="font-size:12px; line-height:1.5;">Esperando datos...</div>
<div class="tpsl">
<div style="background:#00aa00;">🎯 TP<br><span id="ia-tp" style="font-size:20px;">--</span></div>
<div style="background:#ff0000;">🛑 SL<br><span id="ia-sl" style="font-size:20px;">--</span></div>
<div style="background:#FFD700; color:black;">💪 CONFIANZA<br><span id="ia-conf" style="font-size:20px;">--</span></div>
</div>
<div style="font-size:11px; margin-top:6px;">Entrada: <span id="ia-entrada">--</span></div>
</div>
<div class="ghost-box">
<div style="text-align:center; font-size:20px; font-weight:900; color:black;">EN EL GRÁFICO <span style="color:#cc0000; font-style:italic; font-weight:normal;">es igual.</span> <span style="font-size:10px; border:1px solid black; padding:2px 6px;">EJEMPLO</span></div>
<div style="font-size:11px; color:#666; text-align:center;">Entra. Coge lo tuyo. Sale.</div>
<div class="ghost-line ghost-botin"><span>BOTÍN (OBJETIVO)</span><span class="ghost-dash" style="border-color:#009933;"></span><span id="ghost-botin">$--</span></div>
<div class="ghost-line ghost-entrada"><span>ENTRADA</span><span class="ghost-dash" style="border-color:black;"></span><span id="ghost-entrada">$--</span></div>
<div class="ghost-line ghost-salida"><span>SALIDA DE EMERGENCIA (STOP)</span><span class="ghost-dash" style="border-color:#cc0000;"></span><span id="ghost-salida">$--</span></div>
<div style="text-align:center; background:#ff4444; color:white; font-weight:bold; padding:6px; border-radius:8px; margin-top:6px;">por dónde sales 👇 SI SE VA MAL, SALES AQUÍ</div>
</div>
<div class="mi-op">
<div style="font-weight:bold; color:#FFD700; font-size:17px; text-align:center;">💰 MI OPERACIÓN - DIME DONDE PONER TP Y SL</div>
<div style="font-size:12px; color:#aaa; text-align:center; margin:4px 0;">Pon donde compraste, cuanto quieres ganar y cuanto quieres perder</div>
<label>1 - ¿DONDE COMPRASTE / VENDISTE?</label>
<input id="mi-entrada" type="number" step="0.01" placeholder="Ej: 3880">
<label>2 - ¿CUANTO QUIERES GANAR? (Ej: 50)</label>
<input id="mi-ganar" type="number" step="0.01" value="50">
<label>3 - ¿CUANTO QUIERES PERDER? (Ej: 20)</label>
<input id="mi-perder" type="number" step="0.01" value="20">
<div style="display:flex; justify-content:space-between; gap:8px; margin-top:8px;">
<button class="btn-compra" onclick="calcularMiOp('COMPRA')">🟢 COMPRÉ AQUÍ</button>
<button class="btn-venta" onclick="calcularMiOp('VENTA')">🔴 VENDÍ AQUÍ</button>
</div>
<div id="mi-resultado" style="display:none; margin-top:12px; border:2px solid #00ff00; border-radius:12px; padding:12px; background:#0a1a0a; text-align:center;">
<div id="mi-titulo" style="font-weight:bold; font-size:16px;">--</div>
<div id="mi-texto" style="font-size:13px; line-height:1.5; margin-top:6px;">--</div>
<div style="display:flex; gap:8px; margin-top:10px;">
<div style="flex:1; background:#00aa00; border-radius:10px; padding:10px; font-weight:bold;">🎯 PON TP EN<br><span id="mi-tp" style="font-size:22px;">--</span></div>
<div style="flex:1; background:#ff0000; border-radius:10px; padding:10px; font-weight:bold;">🛑 PON SL EN<br><span id="mi-sl" style="font-size:22px;">--</span></div>
</div>
<div style="font-size:11px; margin-top:8px; color:#aaa;">Copia estos 2 números en tu MT5 / Broker tal cual</div>
</div>
</div>
<div class="box"><div style="font-weight:bold;">🟡 ORO (XAUUSD) - EN VIVO + SWING</div><div class="precio" id="oro">$3951.70</div><div class="zonas"><span style="color:#00ff00;">COMPRA SWING: $3900 - $3890 | $3865</span><br><span style="color:#ff4444;">VENTA SWING: $3980 - $3990 | $4020</span></div><div class="luz" id="luz-oro"></div><div id="texto-luz" style="font-size:13px;font-weight:bold;">ESPERANDO...</div><div class="estado" id="estado-oro" style="background:#ff0000;">🔴 VENTA 88% - ESPERANDO $3900</div><div class="chart" id="chart-oro"></div></div>
<div class="box"><div style="font-weight:bold;">📜 HISTORIAL - ULTIMAS SEÑALES</div><div id="historial-lista" style="font-size:12px;text-align:left;">--</div></div>
<div class="box"><div style="font-weight:bold;">💷 GBPUSD - LIBRA</div><div class="precio" id="gbp">1.3412</div><div class="zonas"><span style="color:#00ff00;">COMPRA: 1.2620 - 1.2580</span> | <span style="color:#ff4444;">VENTA: 1.2750 - 1.2820</span></div><div class="estado" id="estado-gbp" style="background:#333;">ESPERANDO</div><div class="chart" id="chart-gbp"></div></div>
<div class="box"><div style="font-weight:bold;">💶 EURO (EURUSD)</div><div class="precio" id="eur">1.1197</div><div class="zonas">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div><div class="chart" id="chart-eur"></div></div>
<div class="box"><div style="font-weight:bold;">🚗 TESLA (TSLA)</div><div class="precio" id="tesla">$245.80</div><div class="zonas"><span style="color:#00ff00;">COMPRA: $240 - $235 - $228</span><br><span style="color:#ff4444;">VENTA: $275 - $285 - $295</span></div><div class="estado" id="estado-tesla" style="background:#333;">ESPERANDO</div><div class="chart" id="chart-tesla"></div></div>
<div class="box"><div style="font-weight:bold;">🍎 APPLE (AAPL)</div><div class="precio" id="apple">$185.30</div><div class="zonas"><span style="color:#00ff00;">COMPRA: $172 - $168 - $165</span><br><span style="color:#ff4444;">VENTA: $195 - $200 - $205</span></div><div class="estado" id="estado-apple" style="background:#333;">ESPERANDO</div><div class="chart" id="chart-apple"></div></div>
<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA - PAYPAL</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050 - CONFIRMAR PAGO</a>
<a href="https://t.me/{BOT_USERNAME}?start=Hola_Raudy_quiero_VIP" target="_blank" class="btn-telegram">✈️ TELEGRAM - CONECTAR CON MI ROBOT</a>
<div class="footer">App: RAUDY ORO PRO + BOT 6 ALERTAS + IA SWING + 50 ANALIZADORES | raudy-vip-oro.onrender.com<br>© 2026 App Única Creada por Raudy Manzueta - Ginebra Suiza 🇨🇭<br>Velas en vivo + Telegram + IA - Vence {FECHA_VENCE.strftime("%d/%m/%Y")} - Solo Educativo</div>
<script>
function sonidoPrueba(){{ try{{ let a=new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg'); a.play(); }}catch(e){{}} }}
function calcularMiOp(tipo){{
  let entrada = parseFloat(document.getElementById('mi-entrada').value);
  let ganar = parseFloat(document.getElementById('mi-ganar').value);
  let perder = parseFloat(document.getElementById('mi-perder').value);
  if(!entrada || !ganar || !perder){{ alert('Raudy, pon los 3 números: donde compraste, cuanto quieres ganar y cuanto quieres perder'); return; }}
  let tp, sl, titulo, texto;
  if(tipo === 'COMPRA'){{
    tp = entrada + ganar;
    sl = entrada - perder;
    titulo = '🟢 COMPRASTE EN $' + entrada.toFixed(2);
    texto = 'Compraste en $' + entrada.toFixed(2) + ', quieres ganar $' + ganar + ' y perder max $' + perder + '. Pon esto en tu broker:';
  }} else {{
    tp = entrada - ganar;
    sl = entrada + perder;
    titulo = '🔴 VENDISTE EN $' + entrada.toFixed(2);
    texto = 'Vendiste en $' + entrada.toFixed(2) + ', quieres ganar $' + ganar + ' y perder max $' + perder + '. Pon esto en tu broker:';
  }}
  document.getElementById('mi-resultado').style.display = 'block';
  document.getElementById('mi-titulo').innerText = titulo;
  document.getElementById('mi-texto').innerText = texto;
  document.getElementById('mi-tp').innerText = '$' + tp.toFixed(2);
  document.getElementById('mi-sl').innerText = '$' + sl.toFixed(2);
  document.getElementById('mi-resultado').scrollIntoView({{behavior:'smooth', block:'center'}});
  document.getElementById('ghost-entrada').innerText = '$' + entrada.toFixed(2);
  document.getElementById('ghost-botin').innerText = '$' + tp.toFixed(2);
  document.getElementById('ghost-salida').innerText = '$' + sl.toFixed(2);
}}
function makeCandleChart(elemId){{ const chart = LightweightCharts.createChart(document.getElementById(elemId), {{ layout: {{ background: {{ color: '#0f0f0f' }}, textColor: '#888' }}, grid: {{ vertLines: {{ color: '#222' }}, horzLines: {{ color: '#222' }} }}, width: document.getElementById(elemId).clientWidth, height: 180, timeScale: {{ timeVisible: true, secondsVisible: true }} }}); const series = chart.addCandlestickSeries({{ upColor: '#00ff00', downColor: '#ff4444', borderVisible: false, wickUpColor: '#00ff00', wickDownColor: '#ff4444' }}); return {{ chart, series, data: [] }}; }}
let charts = {{ oro: makeCandleChart('chart-oro'), gbp: makeCandleChart('chart-gbp'), eur: makeCandleChart('chart-eur'), tesla: makeCandleChart('chart-tesla'), apple: makeCandleChart('chart-apple') }};
function addCandle(cObj, price){{ let now = Math.floor(Date.now() / 1000); let last = cObj.data[cObj.data.length - 1]; if(!last || (now - last.time) >= 15){{ let candle = {{ time: now, open: last ? last.close : price, high: price, low: price, close: price }}; cObj.data.push(candle); if(cObj.data.length > 60) cObj.data.shift(); }} else {{ last.high = Math.max(last.high, price); last.low = Math.min(last.low, price); last.close = price; }} cObj.series.setData(cObj.data); }}
let ultimaSenalMaestro = "";
async function actualizar(){{ try{{ let r = await fetch('/api/precios?v=' + Date.now()); if(r.status==401){{ window.location='/login'; return; }} let d = await r.json(); let hora = new Date().toLocaleTimeString(); document.getElementById('oro').innerText = '$' + d.oro.toFixed(2); document.getElementById('gbp').innerText = d.gbp.toFixed(4); document.getElementById('eur').innerText = d.eur.toFixed(4); document.getElementById('tesla').innerText = '$' + d.tesla.toFixed(2); document.getElementById('apple').innerText = '$' + d.apple.toFixed(2); document.getElementById('hora').innerText = 'Actualizado: ' + hora + ' VIVO - BOT 6 ALERTAS + IA SWING + 50'; addCandle(charts.oro, d.oro); addCandle(charts.gbp, d.gbp); addCandle(charts.eur, d.eur); addCandle(charts.tesla, d.tesla); addCandle(charts.apple, d.apple); let ia = d.ia; document.getElementById('ia-señal').innerText = ia.señal + ' - ' + ia.confianza; document.getElementById('ia-analisis').innerText = ia.analisis; document.getElementById('ia-tp').innerText = '$' + ia.tp; document.getElementById('ia-sl').innerText = '$' + ia.sl; document.getElementById('ia-conf').innerText = ia.confianza; document.getElementById('ia-entrada').innerText = '$' + ia.entrada; document.getElementById('ghost-entrada').innerText = '$' + ia.entrada; document.getElementById('ghost-botin').innerText = '$' + ia.tp; document.getElementById('ghost-salida').innerText = '$' + ia.sl; if(d.filtro){{ let f = document.getElementById('filtro-texto'); f.innerText = d.filtro.texto; f.style.color = d.filtro.color; }} if(d.reloj){{ let rt = document.getElementById('reloj-texto'); rt.innerText = d.reloj.texto; rt.style.color = d.reloj.color; document.getElementById('h-ginebra').innerText = d.reloj.hora_ginebra; document.getElementById('h-londres').innerText = d.reloj.hora_londres; document.getElementById('h-ny').innerText = d.reloj.hora_ny; document.getElementById('h-tokio').innerText = d.reloj.hora_tokio; document.getElementById('reloj-sesion').innerText = 'SESION: ' + d.reloj.sesion + ' | DIA: ' + d.reloj.dia; }} let eo = document.getElementById('estado-oro'); let luz = document.getElementById('luz-oro'); let textoLuz = document.getElementById('texto-luz'); eo.innerHTML = ia.señal; eo.style.background = ia.color; luz.style.background = ia.luz; luz.style.boxShadow = '0 0 20px 10px ' + ia.luz; luz.classList.add('luz-activa'); textoLuz.innerHTML = ia.texto_luz; textoLuz.style.color = ia.luz; if(d.maestro50){{ document.getElementById('maestro-texto').innerText = d.maestro50.señal; document.getElementById('maestro-texto').style.color = d.maestro50.color; let lm = document.getElementById('luz-maestro'); lm.style.background = d.maestro50.luz; lm.style.boxShadow = '0 0 30px 15px ' + d.maestro50.luz; document.getElementById('maestro-votos').innerText = 'COMPRA: '+d.maestro50.votos_compra+' | VENTA: '+d.maestro50.votos_venta+' | ESPERA: '+d.maestro50.votos_espera+' | TOTAL 50'; if(d.maestro50.lista){{ document.getElementById('maestro-lista').innerHTML = d.maestro50.lista.map(x=> x[0]+' : '+x[1]).join('<br>'); }} if(d.maestro50.señal !== ultimaSenalMaestro && d.maestro50.señal.includes('DIOS')){{ sonidoPrueba(); ultimaSenalMaestro = d.maestro50.señal; }} }} if(d.historial){{ document.getElementById('historial-lista').innerHTML = d.historial.slice().reverse().map(h=> h.hora+' - $'+h.precio.toFixed(2)+' - '+h.señal).join('<br>'); }} }}catch(e){{}} }}
setInterval(actualizar, 5000); actualizar();
</script></body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
