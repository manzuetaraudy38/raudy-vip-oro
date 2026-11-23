from flask import Flask, jsonify, render_template_string
import requests
import threading
import time

app = Flask(__name__)
cache = {'price': 0, 'candles': {}, 'signal': 'ESPERA', 'color': 'yellow', 'msg': 'Cargando...'}

def get_yahoo(tf):
    # Yahoo Oro Futuro GC=F - Oro real en vivo
    interval_map = {'1m':'1m','5m':'5m','15m':'15m','1h':'60m','4h':'60m'}
    interval = interval_map.get(tf, '5m')
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval={interval}&range=5d"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        j = r.json()
        result = j['chart']['result'][0]
        ts = result['timestamp']
        q = result['indicators']['quote'][0]
        candles = []
        for i in range(len(ts)):
            if q['open'][i] is None: continue
            candles.append({'t': ts[i]*1000, 'o': q['open'][i], 'h': q['high'][i], 'l': q['low'][i], 'c': q['close'][i]})
        # Para 4h agrupar cada 4 velas de 1h
        if tf == '4h':
            grouped = []
            for i in range(0, len(candles)-3, 4):
                chunk = candles[i:i+4]
                grouped.append({'t': chunk[0]['t'], 'o': chunk[0]['o'], 'h': max(x['h'] for x in chunk), 'l': min(x['l'] for x in chunk), 'c': chunk[-1]['c']})
            return grouped
        return candles[-30:]
    except Exception as e:
        print(f"Error {tf}: {e}")
        return []

def update_loop():
    while True:
        try:
            all_c = {}
            for tf in ['1m','5m','15m','1h','4h']:
                all_c[tf] = get_yahoo(tf)
                time.sleep(0.2)
            if all_c['5m']:
                last_5m = all_c['5m'][-1]
                last_1m = all_c['1m'][-1] if all_c['1m'] else last_5m
                price = last_5m['c']
                g5 = last_5m['c'] > last_5m['o']
                g1 = last_1m['c'] > last_1m['o']
                cache['candles'] = all_c
                cache['price'] = price
                if g5 and g1:
                    cache['signal']='COMPRA'; cache['color']='green'
                    cache['msg']=f"COMPRA ORO a {price:.2f} - Vela 5m VERDE"
                elif not g5 and not g1:
                    cache['signal']='VENTA'; cache['color']='red'
                    cache['msg']=f"VENTA ORO a {price:.2f} - Vela 5m ROJA"
                else:
                    cache['signal']='ESPERA'; cache['color']='yellow'
                    cache['msg']=f"ESPERA - 5m {'VERDE' if g5 else 'ROJA'} - Precio {price:.2f}"
            time.sleep(15)
        except Exception as e:
            print(e); time.sleep(10)

threading.Thread(target=update_loop, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RAUDY ORO EN VIVO</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:10px}
.price{font-size:42px;color:#FFD700;font-weight:bold}
.box{border:3px solid #333;border-radius:15px;padding:15px;margin:10px;background:#111}
.lights{display:flex;justify-content:center;gap:30px;margin:15px}
.light{width:90px;height:90px;border-radius:50%;background:#333;border:3px solid #555}
.light.green-on{background:#00ff00;box-shadow:0 0 40px #00ff00}
.light.red-on{background:#ff0000;box-shadow:0 0 40px #ff0000}
.light.yellow-on{background:#ffff00;box-shadow:0 0 40px #ffff00}
.signal{font-size:36px;font-weight:bold;padding:12px;border-radius:10px}
.COMPRA{background:#00ff00;color:#000}
.VENTA{background:#ff0000;color:#fff}
.ESPERA{background:#ffff00;color:#000}
canvas{background:#111;border:1px solid #333;width:100%;height:220px;border-radius:10px}
.tf-btn{padding:8px 12px;margin:3px;background:#222;color:#fff;border:1px solid #444;border-radius:8px}
.tf-btn.active{background:#FFD700;color:#000}
table{width:100%;margin-top:10px}
td{padding:8px;border-bottom:1px solid #222}
</style></head>
<body>
<h1>💰 RAUDY ORO EN VIVO</h1>
<div class="price" id="price">Cargando...</div>
<div class="box">
<div class="lights">
<div><div id="greenLight" class="light"></div><b>COMPRA</b></div>
<div><div id="yellowLight" class="light"></div><b>ESPERA</b></div>
<div><div id="redLight" class="light"></div><b>VENTA</b></div>
</div>
<div id="signal" class="signal ESPERA">ESPERA</div>
<p id="msg">Cargando...</p>
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
<div class="box"><h3>Velas Actuales</h3><table id="tfTable"></table></div>
<script>
let curTF='1m'; let voiceOn=false; let lastSignal='';
function toggleVoice(){ voiceOn=true; document.getElementById('voiceBtn').innerText='✅ VOZ ACTIVADA'; speak('Voz activada, te avisaré cuando sea compra'); }
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
  let html=''; ['1m','5m','15m','1h','4h'].forEach(tf=>{
    let cs=data.candles[tf]; if(!cs||!cs.length) return; let last=cs[cs.length-1];
    let green=last.c>last.o; let emoji=green?'🟢 VERDE':'🔴 ROJA';
    html+=`<tr><td><b>${tf}</b></td><td>${emoji}</td><td>$${last.c.toFixed(2)}</td></tr>`;
  });
  document.getElementById('tfTable').innerHTML=html;
  draw();
  if(data.signal!=lastSignal && data.signal!='ESPERA'){
    lastSignal=data.signal;
    if(data.signal=='COMPRA') speak('Atención, compra oro ahora, vela de cinco minutos verde');
    if(data.signal=='VENTA') speak('Atención, venta oro, vela roja');
  } else if(data.signal=='ESPERA'){ lastSignal='ESPERA'; }
 }catch(e){}
}
load(); setInterval(load,15000);
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
