from flask import Flask, jsonify, render_template_string
import requests
import threading
import time

app = Flask(__name__)
cache = {'price': 0, 'candles': {}, 'signal': 'ESPERA', 'color': 'yellow', 'msg': 'Conectando...', 'status': {}}

BASE = "https://data-api.binance.vision"
SYMBOL = "PAXGUSDT"

def get_candles(tf):
    try:
        url = f"{BASE}/api/v3/klines?symbol={SYMBOL}&interval={tf}&limit=30"
        r = requests.get(url, timeout=10)
        data = r.json()
        out = []
        for c in data:
            out.append({'t': c[0], 'o': float(c[1]), 'h': float(c[2]), 'l': float(c[3]), 'c': float(c[4])})
        return out
    except Exception as e:
        print(f"Error {tf}: {e}")
        return []

def check():
    try:
        all_c = {}
        status = {}
        for tf in ['1m','5m','15m','1h','4h']:
            all_c[tf] = get_candles(tf)
            if all_c[tf]:
                last = all_c[tf][-1]
                is_green = last['c'] > last['o']
                status[tf] = {'green': is_green, 'price': last['c'], 'open': last['o'], 'close': last['c']}
        if all_c['5m']:
            price = all_c['5m'][-1]['c']
            cache['candles'] = all_c
            cache['price'] = price
            cache['status'] = status
            # CONTAR VERDES
            verdes = sum(1 for v in status.values() if v['green'])
            rojas = 5 - verdes
            if verdes == 5:
                cache['signal']='COMPRA'; cache['color']='green'
                cache['msg']=f"🟢🟢🟢🟢🟢 TODAS VERDES - COMPRA ORO a {price:.2f}"
            elif rojas == 5:
                cache['signal']='VENTA'; cache['color']='red'
                cache['msg']=f"🔴🔴🔴🔴🔴 TODAS ROJAS - VENTA ORO a {price:.2f}"
            else:
                cache['signal']='ESPERA'; cache['color']='yellow'
                cache['msg']=f"ESPERA - {verdes} VERDES / {rojas} ROJAS - Falta que se pongan todas verdes - Precio {price:.2f}"
        return True
    except Exception as e:
        print(e)
        return False

def update_loop():
    while True:
        check()
        time.sleep(10)

check()
threading.Thread(target=update_loop, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RAUDY ORO - TODAS JUNTAS</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:10px}
.price{font-size:44px;color:#FFD700;font-weight:bold}
.box{border:3px solid #333;border-radius:15px;padding:15px;margin:10px;background:#111}
.lights{display:flex;justify-content:center;gap:30px;margin:15px}
.light{width:90px;height:90px;border-radius:50%;background:#333;border:3px solid #555}
.light.green-on{background:#00ff00;box-shadow:0 0 40px #00ff00}
.light.red-on{background:#ff0000;box-shadow:0 0 40px #ff0000}
.light.yellow-on{background:#ffff00;box-shadow:0 0 40px #ffff00}
.signal{font-size:38px;font-weight:bold;padding:14px;border-radius:12px}
.COMPRA{background:#00ff00;color:#000}
.VENTA{background:#ff0000;color:#fff}
.ESPERA{background:#ffff00;color:#000}
canvas{background:#111;border:1px solid #333;width:100%;height:220px;border-radius:10px}
.tf-btn{padding:8px 12px;margin:3px;background:#222;color:#fff;border:1px solid #444;border-radius:8px}
.tf-btn.active{background:#FFD700;color:#000}
/* CUADRO TODAS JUNTAS */
.all-box{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}
.mini{flex:1;min-width:60px;padding:12px 5px;border-radius:12px;border:3px solid #555}
.mini.green{background:#00aa00;color:#fff;border-color:#00ff00}
.mini.red{background:#880000;color:#fff;border-color:#ff0000}
.mini .tf{font-size:20px;font-weight:bold}
.mini .dot{font-size:32px}
.mini .p{font-size:12px}
.count{font-size:22px;font-weight:bold;margin:8px}
</style></head>
<body>
<h1>💰 RAUDY ORO EN VIVO</h1>
<div class="price" id="price">Conectando...</div>

<div class="box">
<h2 style="margin:0">👀 TODAS JUNTAS EN UN SOLO CUADRO</h2>
<p style="color:#aaa;margin:5px">Cuando las 5 se pongan VERDES = COMPRA</p>
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
function toggleVoice(){ voiceOn=true; document.getElementById('voiceBtn').innerText='✅ VOZ ACTIVADA'; speak('Voz activada, te avisaré cuando todas estén verdes'); }
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
  let r=await fetch('/api/signal'); data=await r.json();
  if(data.price>0) document.getElementById('price').innerText='$ '+data.price.toFixed(2);
  let sig=document.getElementById('signal'); sig.innerText=data.signal; sig.className='signal '+data.signal;
  document.getElementById('msg').innerText=data.msg;
  document.getElementById('greenLight').className='light '+(data.color=='green'?'green-on':'');
  document.getElementById('redLight').className='light '+(data.color=='red'?'red-on':'');
  document.getElementById('yellowLight').className='light '+(data.color=='yellow'?'yellow-on':'');

  // TODAS JUNTAS
  let order=['1m','5m','15m','1h','4h'];
  let html=''; let verdes=0;
  order.forEach(tf=>{
    let s=data.status[tf];
    if(!s) return;
    if(s.green) verdes++;
    let cls=s.green?'green':'red';
    let dot=s.green?'🟢':'🔴';
    let txt=s.green?'VERDE':'ROJA';
    html+=`<div class="mini ${cls}"><div class="tf">${tf}</div><div class="dot">${dot}</div><div>${txt}</div><div class="p">$${s.price.toFixed(2)}</div></div>`;
  });
  document.getElementById('allBox').innerHTML=html;
  document.getElementById('count').innerText = verdes==5 ? '✅ 5 de 5 VERDES - ¡COMPRA!' : verdes==0 ? '🔴 0 de 5 VERDES - TODO ROJO' : `⏳ ${verdes} de 5 VERDES - Faltan ${5-verdes} para compra`;

  draw();
  if(data.signal!=lastSignal && data.signal!='ESPERA'){
    lastSignal=data.signal;
    if(data.signal=='COMPRA') speak('Atención, todas verdes, compra oro ahora, las cinco velas están verdes');
    if(data.signal=='VENTA') speak('Atención, todas rojas, venta oro');
  } else if(data.signal=='ESPERA'){ lastSignal='ESPERA'; }
 }catch(e){}
}
load(); setInterval(load,10000);
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
