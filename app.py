from flask import Flask, jsonify, render_template_string
import requests
import threading
import time
from datetime import datetime

app = Flask(__name__)

# TU PRECIO DE LA FOTO - JEFE
PRECIO_FOTO = 3603.67
TU_ENTRADA = 3603.67
TU_STOP = 3598.67   # 3603.67 - 5 = pierdes 5
TU_GANA = 3613.67   # 3603.67 + 10 = ganas 10
LOTE = 0.01
ESPERAR_HASTA = 3610.00  # No comprar hasta que suba a 3610

cache = {'price': 0, 'signal': 'ESPERA', 'msg': 'Conectando...', 'entry': TU_ENTRADA, 'sl': TU_STOP, 'tp': TU_GANA, 'last_update': 'nunca', 'live': False}

BASE = "https://data-api.binance.vision"

def get_price():
    try:
        r = requests.get(f"{BASE}/api/v3/ticker/price?symbol=PAXGUSDT", timeout=8)
        return float(r.json()['price'])
    except:
        return 0

def check():
    price = get_price()
    if price <= 0:
        cache['live'] = False
        return
    cache['price'] = price
    cache['last_update'] = datetime.now().strftime("%H:%M:%S")
    cache['live'] = True

    # LOGICA CON TU PRECIO DE LA FOTO
    if price < ESPERAR_HASTA:
        cache['signal'] = 'ESPERA'
        cache['msg'] = f"ESPERA JEFE - Precio ahora ${price:.2f} - Tu precio de la foto era ${PRECIO_FOTO:.2f} - Esperando que suba a ${ESPERAR_HASTA:.2f} para comprar"
    elif price >= ESPERAR_HASTA and price < TU_GANA:
        cache['signal'] = 'COMPRA'
        cache['msg'] = f"🟢 COMPRA JEFE - Precio ${price:.2f} ya subio a ${ESPERAR_HASTA:.2f} - ENTRADA ${TU_ENTRADA:.2f} - STOP ${TU_STOP:.2f} (-5) - GANA ${TU_GANA:.2f} (+10) - Lote {LOTE}"
    else:
        cache['signal'] = 'ESPERA'
        cache['msg'] = f"Ya paso tu GANA de ${TU_GANA:.2f} - No entres tarde, jefe"

def loop():
    while True:
        check()
        time.sleep(5)

check()
threading.Thread(target=loop, daemon=True).start()

HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ROBOT JEFE - PRECIO FOTO 3603.67</title>
<style>body{background:#000;color:#fff;font-family:Arial;text-align:center;padding:10px}
.price{font-size:42px;color:#FFD700;font-weight:bold}
.box{border:3px solid #333;border-radius:15px;padding:15px;margin:10px;background:#111}
.signal{font-size:32px;font-weight:bold;padding:14px;border-radius:12px}
.COMPRA{background:#00ff00;color:#000}.ESPERA{background:#ffff00;color:#000}
.big{font-size:22px;font-weight:bold}
</style></head><body>
<h1>💰 ROBOT JEFE - TU PRECIO</h1>
<div class="price" id="price">...</div>
<div id="upd">...</div>
<div class="box"><div class="big">TU PRECIO DE LA FOTO: $3603.67</div>
<div>ENTRADA: $3603.67 | STOP: $3598.67 (-5) | GANA: $3613.67 (+10)</div>
<div>Lote: 0.01 | Esperar hasta: $3610.00</div></div>
<div class="box"><div id="signal" class="signal ESPERA">ESPERA</div><p id="msg">...</p></div>
<script>
async function load(){
 let r=await fetch('/api/signal?t='+Date.now()); let d=await r.json();
 document.getElementById('price').innerText='$ '+d.price.toFixed(2);
 document.getElementById('upd').innerText='Actualizado: '+d.last_update;
 let s=document.getElementById('signal'); s.innerText=d.signal; s.className='signal '+(d.signal=='COMPRA'?'COMPRA':'ESPERA');
 document.getElementById('msg').innerText=d.msg;
}
load(); setInterval(load,5000);
</script></body></html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/signal')
def signal():
    return jsonify(cache)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
