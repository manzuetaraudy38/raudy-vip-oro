from flask import Flask, jsonify, render_template_string
import requests
import threading
import time
from datetime import datetime
from collections import deque

app = Flask(__name__)

# TU PLAN DE JEFE - 50 EN 100 - 4H
LOTE = 0.01
RIESGO = 5.0   # Pierdes max 5
GANANCIA = 10.0 # Ganas 10
TIMEFRAME = "4h"

cache = {'price': 0, 'signal': 'ESPERA', 'color': 'yellow', 'msg': 'Conectando...', 'entry': 0, 'sl': 0, 'tp': 0, 'last_update': 'nunca', 'live': False, 'candle_4h': '...', 'trend': '...'}

BASE = "https://data-api.binance.vision"
SYMBOL = "PAXGUSDT"
history = deque(maxlen=60)

def get_price():
    try:
        r = requests.get(f"{BASE}/api/v3/ticker/price?symbol={SYMBOL}", timeout=8)
        return float(r.json()['price'])
    except:
        return 0

def get_candles_4h():
    try:
        url = f"{BASE}/api/v3/klines?symbol={SYMBOL}&interval=4h&limit=30"
        r = requests.get(url, timeout=10)
        data = r.json()
        return [{'o': float(c[1]), 'h': float(c[2]), 'l': float(c[3]), 'c': float(c[4])} for c in data]
    except:
        return []

def check():
    try:
        price = get_price()
        if price <= 0:
            cache['live'] = False
            return False
        history.append(price)
        candles = get_candles_4h()
        if not candles:
            return False

        last = candles[-1]
        prev = candles[-2]
        is_green = last['c'] > last['o']
        # Tendencia 4H: ¿Subiendo?
        trend_up = last['c'] > prev['c']

        cache['price'] = price
        cache['candle_4h'] = 'VERDE 🟢 - Subiendo' if is_green else 'ROJA 🔴 - Bajando'
        cache['trend'] = 'PARA ARRIBA' if trend_up else 'PARA ABAJO'
        cache['last_update'] = datetime.now().strftime("%H:%M:%S")
        cache['live'] = True

        # TU PLAN: Entrada = precio actual, SL = -5, TP = +10
        entry = price
        sl = entry - RIESGO
        tp = entry + GANANCIA

        # PULLBACK: ¿Bajó y volvió a subir?
        pullback_ok = False
        if len(history) >= 20:
            minimo = min(list(history)[-20:])
            if price > minimo + 2.0:
                pullback_ok = True

        # REGLA JEFE - Solo 4H
        if trend_up and is_green and pullback_ok:
            cache['signal'] = 'COMPRA'
            cache['color'] = 'green'
            cache['entry'] = round(entry, 2)
            cache['sl'] = round(sl, 2)
            cache['tp'] = round(tp, 2)
            cache['msg'] = f"🟢 COMPRA ORO 4H a ${entry:.2f} - Lote {LOTE} - STOP ${sl:.2f} (pierdes 5) - GANA ${tp:.2f} (ganas 10)"
        elif not trend_up and not is_green:
            cache['signal'] = 'ESPERA - NO VENDAS'
            cache['color'] = 'yellow'
            cache['entry'] = round(entry, 2)
            cache['sl'] = 0
            cache['tp'] = 0
            cache['msg'] = f"ESPERA JEFE - 4H bajando. No compres ahora. Precio ${entry:.2f}"
        else:
            cache['signal'] = 'ESPERA'
            cache['color'] = 'yellow'
            cache['entry'] = round(entry, 2)
            cache['sl'] = round(sl, 2)
            cache['tp'] = round(tp, 2)
            cache['msg'] = f"ESPERA - 4H no está claro. Precio ${entry:.2f} - Si compras, STOP ${sl:.2f} / GANA ${tp:.2f}"
        return True
    except Exception as e:
        print(e)
        cache['live'] = False
        return False

def update_loop():
    while True:
        check()
        time.sleep(5)

check()
threading.Thread(target=update_loop, daemon=True).start()

HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ROBOT JEFE - ORO 4H - 50</title>
<style>body{background:#000;color:#fff;font-family:Arial;text-align:center;padding:10px}
.price{font-size:42px;color:#FFD700;font-weight:bold}
.box{border:3px solid #333;border-radius:15px;padding:15px;margin:10px;background:#111}
.signal{font-size:32px;font-weight:bold;padding:14px;border-radius:12px}
.COMPRA{background:#00ff00;color:#000}.ESPERA{background:#ffff00;color:#000}
.big{font-size:22px;font-weight:bold;margin:5px}
</style></head><body>
<h1>💰 ROBOT JEFE - ORO 4H - 50</h1>
<div class="price" id="price">Conectando...</div>
<div id="upd">--:--:--</div>
<div class="box"><div class="big" id="trend">...</div><div id="candle">...</div></div>
<div class="box"><div id="signal" class="signal ESPERA">ESPERA</div><p id="msg">...</p>
<div class="big" id="plan"></div></div>
<script>
async function load(){
 try{
  let r=await fetch('/api/signal?t='+Date.now()); let d=await r.json();
  document.getElementById('price').innerText='$ '+d.price.toFixed(2);
  document.getElementById('upd').innerText='Actualizado: '+d.last_update+' | 4H | Lote 0.01';
  document.getElementById('trend').innerText='Tendencia 4H: '+d.trend;
  document.getElementById('candle').innerText='Vela 4H: '+d.candle_4h;
  let s=document.getElementById('signal'); s.innerText=d.signal; s.className='signal '+(d.signal=='COMPRA'?'COMPRA':'ESPERA');
  document.getElementById('msg').innerText=d.msg;
  if(d.entry>0) document.getElementById('plan').innerText='Entrada: $'+d.entry+' | STOP: $'+d.sl+' (-5) | GANA: $'+d.tp+' (+10)';
 }catch(e){}
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
