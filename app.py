from flask import Flask, jsonify, render_template_string
import requests
import threading
import time
from datetime import datetime
from collections import deque

app = Flask(__name__)
cache = {'price': 0, 'avg_price': 0, 'prices': {}, 'candles': {}, 'signal': 'ESPERA', 'color': 'yellow', 'msg': 'Conectando...', 'status': {}, 'last_update': 'nunca', 'live': False, 'consensus': '...', 'entry': '...', 'spread': 0, 'entry_price': 0, 'stop': 0, 'tp1': 0, 'tp2': 0}

BASE = "https://data-api.binance.vision"
SYMBOL = "PAXGUSDT"
history = deque(maxlen=60)

def get_binance_ticker(sym):
    try:
        r = requests.get(f"{BASE}/api/v3/ticker/price?symbol={sym}", timeout=8)
        return float(r.json()['price'])
    except:
        return 0

def get_coingecko_paxg():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd", timeout=8)
        return float(r.json()['pax-gold']['usd'])
    except:
        return 0

def get_all_prices():
    paxg = get_binance_ticker("PAXGUSDT")
    xaut = get_binance_ticker("XAUTUSDT")
    cg = get_coingecko_paxg()
    prices = {}
    if paxg > 0: prices['Binance PAXG'] = paxg
    if xaut > 0: prices['Binance XAUT'] = xaut
    if cg > 0: prices['Global PAXG'] = cg
    return prices

def get_candles(tf):
    try:
        url = f"{BASE}/api/v3/klines?symbol={SYMBOL}&interval={tf}&limit=30"
        r = requests.get(url, timeout=10)
        data = r.json()
        return [{'t': c[0], 'o': float(c[1]), 'h': float(c[2]), 'l': float(c[3]), 'c': float(c[4])} for c in data]
    except:
        return []

def check():
    try:
        prices = get_all_prices()
        if not prices:
            cache['live'] = False
            return False
        vals = list(prices.values())
        avg_price = sum(vals) / len(vals)
        spread = max(vals) - min(vals) if len(vals) > 1 else 0
        history.append(avg_price)

        all_c = {}
        status = {}
        for tf in ['1m','5m','15m','1h','4h']:
            all_c[tf] = get_candles(tf)
            if all_c[tf]:
                last = all_c[tf][-1]
                is_green = last['c'] > last['o']
                status[tf] = {'green': is_green, 'price': last['c'], 'open': last['o'], 'close': last['c']}

        cache['prices'] = prices
        cache['avg_price'] = avg_price
        cache['price'] = avg_price
        cache['spread'] = spread
        cache['candles'] = all_c
        cache['status'] = status
        cache['last_update'] = datetime.now().strftime("%H:%M:%S")
        cache['live'] = True

        verdes = sum(1 for v in status.values() if v['green'])
        rojas = 5 - verdes

        entry = "ESPERANDO"
        pullback_ok = False
        if len(history) >= 20:
            reciente = list(history)[-20:]
            minimo = min(reciente)
            if avg_price > minimo + 2.0:
                pullback_ok = True
                entry = f"✅ PULLBACK LISTO - Bajo a ${minimo:.2f} y volvio a subir a ${avg_price:.2f}"
            else:
                entry = f"⏳ Esperando que baje un poco y suba - Minimo ${minimo:.2f}"
        else:
            entry = "⏳ Calentando motor... recogiendo precios (1 min)"
        cache['entry'] = entry

        mercados_de_acuerdo = spread < 20 and len(prices) >= 2
        if mercados_de_acuerdo:
            consensus = f"✅ LOS {len(prices)} MERCADOS DE ACUERDO - Diferencia solo ${spread:.2f}"
        else:
            consensus = f"⚠️ MERCADOS EN DESACUERDO - Diferencia ${spread:.2f}"
        cache['consensus'] = consensus

        # --- NUMEROS AUTOMATICOS: -20 y +40 ---
        # COMPRA: STOP = precio -20, TP1 = +20, TP2 = +40
        # VENTA: STOP = precio +20, TP1 = -20, TP2 = -40
        if verdes == 5 and mercados_de_acuerdo and pullback_ok:
            cache['signal'] = 'COMPRA'; cache['color'] = 'green'
            cache['entry_price'] = avg_price
            cache['stop'] = avg_price - 20
            cache['tp1'] = avg_price + 20
            cache['tp2'] = avg_price + 40
            cache['msg'] = f"🟢 MOMENTO PRECISO - COMPRA ORO a ${avg_price:.2f} - STOP ${avg_price-20:.2f} - GANA ${avg_price+40:.2f}"
        elif rojas == 5 and mercados_de_acuerdo and len(history) >= 20 and avg_price < max(list(history)[-20:]) - 2.0:
            cache['signal'] = 'VENTA'; cache['color'] = 'red'
            cache['entry_price'] = avg_price
            cache['stop'] = avg_price + 20
            cache['tp1'] = avg_price - 20
            cache['tp2'] = avg_price - 40
            cache['msg'] = f"🔴 MOMENTO PRECISO - VENTA ORO a ${avg_price:.2f} - STOP ${avg_price+20:.2f} - GANA ${avg_price-40:.2f}"
        else:
            cache['signal'] = 'ESPERA'; cache['color'] = 'yellow'
            # Aunque este en ESPERA, te muestra cuales SERIAN los numeros si compraras ahora, para que practiques
            cache['entry_price'] = avg_price
            cache['stop'] = avg_price - 20
            cache['tp1'] = avg_price + 20
            cache['tp2'] = avg_price + 40
            faltan = []
            if verdes < 5: faltan.append(f"Faltan {5-verdes} velas verdes")
            if not mercados_de_acuerdo: faltan.append("Mercados no de acuerdo")
            if not pullback_ok: faltan.append("Esperando pullback")
            cache['msg'] = f"ESPERA - {verdes}/5 VERDES - {' | '.join(faltan)} - Precio ${avg_price:.2f}"
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
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RAUDY ORO - TODO EL MERCADO</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:10px}
.price{font-size:42px;color:#FFD700;font-weight:bold}
.sub{font-size:13px;color:#aaa}
.live{font-size:14px;color:#00ff00}
.live.off{color:#ff0000}
.box{border:3px solid #333;border-radius:15px;padding:15px;margin:10px;background:#111}
.lights{display:flex;justify-content:center;gap:30px;margin:15px}
.light{width:90px;height:90px;border-radius:50%;background:#333;border:3px solid #555}
.light.green-on{background:#00ff00;box-shadow:0 0 40px #00ff00}
.light.red-on{background:#ff0000;box-shadow:0 0 40px #ff0000}
.light.yellow-on{background:#ffff00;box-shadow:0 0 40px #ffff00}
.signal{font-size:34px;font-weight:bold;padding:14px;border-radius:12px}
.COMPRA{background:#00ff00;color:#000}
.VENTA{background:#ff0000;color:#fff}
.ESPERA{background:#ffff00;color:#000}
canvas{background:#111;border:1px solid #333;width:100%;height:220px;border-radius:10px}
.tf-btn{padding:8px 12px;margin:3px;background:#222;color:#fff;border:1px solid #444;border-radius:8px}
.tf-btn.active{background:#FFD700;color:#000}
.all-box{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}
.mini{flex:1;min-width:60px;padding:12px 5px;border-radius:12px;border:3px solid #555}
.mini.green{background:#00aa00;color:#fff;border-color:#00ff00}
.mini.red{background:#880000;color:#fff;border-color:#ff0000}
.mini .tf{font-size:20px;font-weight:bold}
.mini .dot{font-size:32px}
.mini .p{font-size:12px}
.count{font-size:22px;font-weight:bold;margin:8px}
.price-box{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.pcard{flex:1;min-width:100px;background:#222;border:2px solid #444;border-radius:12px;padding:10px}
.pcard b{font-size:12px;color:#FFD700}
.pcard div{font-size:18px;font-weight:bold}
.info{font-size:14px;padding:8px;border-radius:8px;background:#222;margin:5px 0}
.num-box{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}
.num{flex:1;min-width:100px;padding:12px;border-radius:12px;border:3px solid #FFD700;background:#222}
.num b{font-size:12px;color:#FFD700;display:block}
.num span{font-size:22px;font-weight:bold}
.num.stop{border-color:#ff0000}
.num.tp{border-color:#00ff00}
</style></head>
<body>
<h1>💰 RAUDY ORO - TODO EL MERCADO</h1>
<div class="sub">PRECIO PROMEDIO DE LOS 3 MERCADOS</div>
<div class="price" id="price">Conectando...</div>
<div id="liveTag" class="live">● EN VIVO</div>
<div style="font-size:12px;color:#aaa">Actualizado: <span id="upd">--:--:--</span> | Cada 5 seg</div>

<div class="box">
<h3 style="margin:0">🌍 LOS 3 PRECIOS DEL MERCADO</h3>
<div class="price-box" id="pricesBox"></div>
<div class="info" id="consensus">...</div>
<div class="info" id="entryInfo">...</div>
</div>

<div class="box" style="border-color:#FFD700">
<h2 style="margin:0;color:#FFD700">🎯 TUS NUMEROS - SOLO COPIAR EN TU BROKER</h2>
<div class="num-box">
<div class="num"><b>🟢 COMPRA / ENTRADA</b><span id="entryNum">--</span></div>
<div class="num stop"><b>🔴 STOP - FRENO</b><span id="stopNum">--</span></div>
<div class="num tp"><b>💰 GANA 1</b><span id="tp1Num">--</span></div>
<div class="num tp"><b>💰💰 GANA 2</b><span id="tp2Num">--</span></div>
</div>
<p style="font-size:13px;color:#aaa;margin:0">Formula: STOP = Entrada - 20 | GANA = Entrada + 20 / +40<br>Si es VENTA, es al reves: STOP = Entrada + 20 | GANA = Entrada - 20 / -40</p>
</div>

<div class="box">
<h2 style="margin:0">👀 TODAS JUNTAS EN UN SOLO CUADRO</h2>
<div class="all-box" id="allBox"></div>
<div class="count" id="count">Cargando...</div>
</div>

<div class="box">
<div class="lights">
<div><div id="greenLight" class="light"></div><b>COMPRA</b></div>
<div><div id="yellowLight" class="light"></div><b>ESPERA</b></div>
<div><div id="redLight" class="light"></div><b>VENTA</b></div>
</div>
<div id="signal" class="signal ESPERA">ESPERA</div>
<p id="msg">Conectando...</p>
<button onclick="toggleVoice()" id="voiceBtn" style="padding:12px;background:#FFD700;border:none;border-radius:10px;font-weight:bold">🔊 ACTIVAR VOZ</button>
</div>

<div class="box">
<div>
<button class="tf-btn active" onclick="setTF('1m',this)">1m</button>
<button class="tf-btn" onclick="setTF('5m',this)">5m</button>
<button class="tf-btn" onclick="setTF('15m',this)">15m</button>
<button class="tf-btn" onclick="setTF('1h',this)">1H</button>
<button class="tf-btn" onclick="setTF('4h',this)">4H</button>
</div>
<canvas id="chart" width="800" height="220"></canvas>
</div>

<script>
let curTF='1m'; let voiceOn=false; let lastSignal='';
function toggleVoice(){ voiceOn=true; document.getElementById('voiceBtn').innerText='✅ VOZ ACTIVADA'; speak('Voz activada, te dire tus numeros cuando sea el momento preciso'); }
function speak(t){ if(!voiceOn) return; let u=new SpeechSynthesisUtterance(t); u.lang='es-ES'; u.rate=1.1; speechSynthesis.cancel(); speechSynthesis.speak(u); }
function setTF(tf,btn){ curTF=tf; document.querySelectorAll('.tf-btn').forEach(b=>b.classList.remove('active')); btn.classList.add('active'); draw(); }
let data=null;
function draw(){
 if(!data||!data.candles[curTF]) return;
 let c=document.getElementById('chart'); let ctx=c.getContext('2d'); ctx.clearRect(0,0,c.width,c.height);
 let candles=data.candles[curTF]; let min=Math.min(...candles.map(x=>x.l)); let max=Math.max(...candles.map(x=>x.h)); let range=max-min||1;
 let w=c.width/candles.length;
 candles.forEach((k,i)=>{
   let x=i*w+w/2; let yH=(max-k.h)/range*c.height; let yL=(max-k.l)/range*c.height;
   let yO=(max-k.o)/range*c.height; let yC=(max-k.c)/range*c.height;
   let green=k.c>k.o; ctx.strokeStyle=green?'#00ff00':'#ff0000'; ctx.fillStyle=green?'#00ff00':'#ff0000';
   ctx.beginPath(); ctx.moveTo(x,yH); ctx.lineTo(x,yL); ctx.stroke();
   let top=Math.min(yO,yC); let h=Math.max(2,Math.abs(yC-yO)); ctx.fillRect(x-w*0.35,top,w*0.7,h);
 });
}
async function load(){
 try{
  let r=await fetch('/api/signal?t='+Date.now()); data=await r.json();
  if(data.avg_price>0) document.getElementById('price').innerText='$ '+data.avg_price.toFixed(2)+'  PROMEDIO';
  document.getElementById('upd').innerText=data.last_update||'--:--:--';
  document.getElementById('consensus').innerText=data.consensus||'';
  document.getElementById('entryInfo').innerText=data.entry||'';
  document.getElementById('entryNum').innerText='$'+(data.entry_price||0).toFixed(2);
  document.getElementById('stopNum').innerText='$'+(data.stop||0).toFixed(2);
  document.getElementById('tp1Num').innerText='$'+(data.tp1||0).toFixed(2);
  document.getElementById('tp2Num').innerText='$'+(data.tp2||0).toFixed(2);
  let lt=document.getElementById('liveTag');
  if(data.live){ lt.innerText='● EN VIVO - Vigilando todo el mercado'; lt.className='live'; } else { lt.innerText='● DESCONECTADO'; lt.className='live off'; }
  let sig=document.getElementById('signal'); sig.innerText=data.signal; sig.className='signal '+data.signal;
  document.getElementById('msg').innerText=data.msg;
  document.getElementById('greenLight').className='light '+(data.color=='green'?'green-on':'');
  document.getElementById('redLight').className='light '+(data.color=='red'?'red-on':'');
  document.getElementById('yellowLight').className='light '+(data.color=='yellow'?'yellow-on':'');
  let htmlP='';
  for(let k in data.prices){ htmlP+=`<div class="pcard"><b>${k}</b><div>$${data.prices[k].toFixed(2)}</div></div>`; }
  document.getElementById('pricesBox').innerHTML=htmlP;
  let order=['1m','5m','15m','1h','4h'];
  let html=''; let verdes=0;
  order.forEach(tf=>{
    let s=data.status[tf]; if(!s) return;
    if(s.green) verdes++;
    let cls=s.green?'green':'red'; let dot=s.green?'🟢':'🔴'; let txt=s.green?'VERDE':'ROJA';
    html+=`<div class="mini ${cls}"><div class="tf">${tf}</div><div class="dot">${dot}</div><div>${txt}</div><div class="p">$${s.price.toFixed(2)}</div></div>`;
  });
  document.getElementById('allBox').innerHTML=html;
  document.getElementById('count').innerText = verdes==5 ? '✅ 5 de 5 VERDES' : `⏳ ${verdes} de 5 VERDES`;
  draw();
  if(data.signal!=lastSignal && data.signal!='ESPERA'){
    lastSignal=data.signal;
    if(data.signal=='COMPRA') speak('Momento preciso, compra oro en '+data.entry_price.toFixed(0)+', pon tu freno en '+data.stop.toFixed(0)+', y tu ganancia en '+data.tp2.toFixed(0));
    if(data.signal=='VENTA') speak('Momento preciso, venta oro en '+data.entry_price.toFixed(0)+', freno en '+data.stop.toFixed(0));
  } else if(data.signal=='ESPERA'){ lastSignal='ESPERA'; }
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
