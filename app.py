# app.py - RAUDY VIP 1000 - FINAL BOT QUE SI HABLA
import os, json, urllib.request, threading, time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# TUS LINKS
LINK_PAYPAL = "https://paypal.me/RaudyManzueta/20"
LINK_WHATSAPP = "https://wa.me/41767574050"
LINK_TELEGRAM = "https://t.me/raudy_vip_oro_bot"

# LEE LA LLAVE COMO SEA QUE SE LLAME EN RENDER
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "") or os.getenv("BOT_TOKEN", "") or os.getenv("BOT_TOKE", "") or os.getenv("BOT_TO", "")
print(f"TOKEN ENCONTRADO? {'SI - largo ' + str(len(TELEGRAM_TOKEN)) if TELEGRAM_TOKEN else 'NO - VACIO'}")

YAHOO = {"ORO": "GC=F", "TESLA": "TSLA", "APPLE": "AAPL", "META": "META", "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/CHF": "CHF=X", "SP500": "^GSPC"}

def get_precio_real(sym):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            return float(data["chart"]["result"][0]["meta"]["regularMarketPrice"])
    except:
        return 4115.0

def enviar_telegram(chat_id, texto):
    if not TELEGRAM_TOKEN:
        print("No puedo enviar, no hay TOKEN")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        datos = json.dumps({"chat_id": chat_id, "text": texto}).encode()
        req = urllib.request.Request(url, data=datos, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
        print(f"Mensaje enviado a {chat_id}")
    except Exception as e:
        print("Error enviar Telegram", e)

def bot_loop():
    offset = 0
    print("BOT ENCENDIDO - esperando mensajes...")
    while True:
        try:
            if not TELEGRAM_TOKEN:
                print("BOT ESPERANDO TOKEN... revisa Render Environment")
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
                    print(f"Mensaje recibido: {texto} de {chat_id}")
                    oro = get_precio_real("GC=F")
                    if texto in ["/start", "start", "hola", "hi", "bb", "nn", "/vip", "/todo"]:
                        enviar_telegram(chat_id, f"👑 BIENVENIDO JEFE A RAUDY VIP 1000\n\n🥇 ORO EN VIVO: {oro}\n🚗 TESLA: {get_precio_real('TSLA')}\n🍎 APPLE: {get_precio_real('AAPL')}\n📘 META: {get_precio_real('META')}\n📈 SP500: {get_precio_real('^GSPC')}\n\n🎯 TP: 4000\n🛑 SL: 3950\n\n💳 Pagar $20: {LINK_PAYPAL}\n💬 WhatsApp: {LINK_WHATSAPP}\n\nEscribe /precio para ver el ORO")
                    elif texto in ["/precio", "precio"]:
                        enviar_telegram(chat_id, f"🥇 JEFE ORO EN VIVO: {oro}\nSi baja de 3950 te aviso.")
                    else:
                        enviar_telegram(chat_id, f"Jefe, te entendi: {texto}\nEscribe /start para el menu o /precio para el ORO en vivo")
        except Exception as e:
            print("Bot error", e)
            time.sleep(3)

threading.Thread(target=bot_loop, daemon=True).start()

HTML = """
<!DOCTYPE html><html lang="es"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY VIP 1000</title>
<style>body{margin:0;font-family:Arial;background:#0a0a0a;color:white;padding:15px}.top{background:gold;color:black;padding:18px;border-radius:18px;text-align:center}.top h1{margin:0;font-size:32px}.card{background:#1a1a1a;border-radius:20px;padding:20px;margin-top:15px}.precio-grande{font-size:65px;font-weight:bold;text-align:center;color:#00ff88}select,input{width:100%;padding:18px;font-size:22px;border-radius:14px;margin-top:10px}.btn-comprar{width:100%;padding:22px;font-size:26px;background:#00c853;color:white;border:none;border-radius:16px;margin-top:15px}.btn-vender{width:100%;padding:22px;font-size:26px;background:#d50000;color:white;border:none;border-radius:16px;margin-top:12px}.btn-tg{width:100%;padding:18px;font-size:20px;background:#0088cc;color:white;border:none;border-radius:14px}.btn-wa{width:100%;padding:18px;font-size:20px;background:#25D366;color:white;border:none;border-radius:14px;margin-top:10px}.btn-pago{width:100%;padding:22px;font-size:22px;background:gold;border:none;border-radius:16px;margin-top:12px;font-weight:bold}</style></head><body>
<div class="top"><h1>RAUDY VIP 1000 👑</h1><p>PRECIOS REALES EN VIVO + BOT QUE HABLA</p><p id="estado">CONECTANDO...</p></div>
<div class="card"><div style="text-align:center;font-size:22px;">PRECIOS REALES</div><div id="lista" style="font-size:18px;line-height:2;">Cargando...</div></div>
<div class="card"><select id="activo"><option value="ORO">🥇 ORO</option><option value="TESLA">🚗 TESLA</option><option value="APPLE">🍎 APPLE</option><option value="META">📘 META</option><option value="SP500">📈 SP500</option></select><div id="precio" class="precio-grande">----</div><button class="btn-comprar" onclick="hablar('Jefe, voy a COMPRAR')">🟢 COMPRAR</button><button class="btn-vender" onclick="hablar('Jefe, voy a VENDER')">🔴 VENDER</button></div>
<div class="card"><a href="LINK_TELEGRAM_PLACEHOLDER"><button class="btn-tg">📩 TELEGRAM - @raudy_vip_oro_bot</button></a><a href="LINK_WHATSAPP_PLACEHOLDER"><button class="btn-wa">💬 WHATSAPP - 076 757 40 50</button></a><a href="LINK_PAYPAL_PLACEHOLDER"><button class="btn-pago">💳 PAGAR $20 - PAYPAL</button></a></div>
<script>function hablar(t){let v=new SpeechSynthesisUtterance(t);v.lang='es-DO';speechSynthesis.speak(v)}async function cargar(){let r=await fetch('/api/precios');let d=await r.json();document.getElementById('lista').innerHTML=Object.keys(d).map(k=>k+": <b>"+d[k]+"</b>").join("<br>");document.getElementById('precio').innerText=d['ORO'];document.getElementById('estado').innerText="✅ EN VIVO - "+new Date().toLocaleTimeString()}cargar();setInterval(cargar,3000)</script></body></html>
"""
HTML = HTML.replace("LINK_TELEGRAM_PLACEHOLDER", LINK_TELEGRAM).replace("LINK_WHATSAPP_PLACEHOLDER", LINK_WHATSAPP).replace("LINK_PAYPAL_PLACEHOLDER", LINK_PAYPAL)

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/precios")
def api_precios():
    out = {}
    for n,s in YAHOO.items():
        p = get_precio_real(s)
        if p: out[n]=p
    return jsonify(out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
