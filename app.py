# ===== RAUDY - 50 ANALIZADORES + MOTOR =====
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
    # 50 ANALIZADORES EXTRA - MOTOR FUERZA TOTAL
    votos.append(("50 MOTOR FUERZA TOTAL", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
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
    motor = motor_fuerza_total(precio)
    maestro["motor"] = motor["fuerza"]
    maestro["velocidad"] = motor["velocidad"]
    maestro["total"] = 100
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
    print("🤖 BOT TELEGRAM INICIADO - 6 ALERTAS + IA SWING + 50 ANALIZADORES + MOTOR FUERZA TOTAL 100")
    send_telegram(f"✅ *VIP ORO Raudy ACTIVO + IA SWING + 50 ANALIZADORES + MOTOR FUERZA TOTAL*\n\nTe avisaré automático:\n🟢 COMPRA: 3900, 3890, 3865\n🔴 VENTA: 3980, 3990, 4020\n\n📲 APP: raudy-vip-oro.onrender.com\nVence: {FECHA_VENCE.strftime('%d/%m/%Y')}")
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
                            send_telegram(f"🔥 *RAUDY ORO PRO VIP + IA SWING + 50 ANALIZADORES + MOTOR FUERZA TOTAL*\n\nBienvenido! Estás activo.\n🟢 BUY: 3900, 3890, 3865\n🔴 SELL: 3980, 3990, 4020\nAPP: raudy-vip-oro.onrender.com\n\nEscribe /precios para ver ORO ahora")
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
        time.sleep(15)

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
    chat = chat_robots(oro_f, maestro50)
    historial_senales.append({"hora": hora_ginebra().strftime("%H:%M"), "precio": oro_f, "señal": maestro50["señal"]})
    if len(historial_senales) > 100:
        historial_senales.pop(0)
    return {"oro": oro_f,"gbp": gbp_v,"eur": eur_v,"tesla": tesla_v,"apple": apple_v,"ia": ia, "filtro": filtro, "reloj": reloj, "maestro50": maestro50, "historial": historial_senales[-20:], "chat_robots": chat, "robots_top": sorted(ROBOTS_RAUDY, key=lambda x: x["estrellas"], reverse=True)[:5]}
