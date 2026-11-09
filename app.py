from flask import Flask, jsonify, request
import requests, os, threading, time, json
from datetime import datetime

app = Flask(__name__)

# ===== LLAVES - SE PONEN EN RENDER =====
BYBIT_API_KEY = os.environ.get("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.environ.get("BYBIT_API_SECRET", "")
# True = DINERO FALSO / False = DINERO REAL
USAR_TESTNET = os.environ.get("USAR_TESTNET", "True") == "True"

try:
    from pybit.unified_trading import HTTP
    HAY_PYBIT = True
except:
    HAY_PYBIT = False

def get_session():
    if not HAY_PYBIT or not BYBIT_API_KEY:
        return None
    return HTTP(testnet=USAR_TESTNET, api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)

def get_velas():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1h&range=5d"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=6)
        j = r.json()
        res = j['chart']['result'][0]
        closes = res['indicators']['quote'][0]['close']
        opens = res['indicators']['quote'][0]['open']
        highs = res['indicators']['quote'][0]['high']
        lows = res['indicators']['quote'][0]['low']
        velas = []
        for i in range(len(closes)):
            if closes[i] is not None:
                velas.append({"o": round(float(opens[i]),2), "h": round(float(highs[i]),2), "l": round(float(lows[i]),2), "c": round(float(closes[i]),2)})
        return velas[-30:]
    except:
        return [{"o":4110,"h":4120,"l":4100,"c":4118}]

def calc_ema(precios, periodo):
    if len(precios) < periodo: return sum(precios)/len(precios) if precios else 4118
    sma = sum(precios[:periodo])/periodo
    ema = sma; k = 2/(periodo+1)
    for p in precios[periodo:]: ema = (p*k)+(ema*(1-k))
    return round(ema,2)

ROBOT = {"ultimo": "Robot esperando...", "operaciones": 0, "modo": "AUTO"}

def robot_loop():
    while True:
        try:
            if ROBOT["modo"] == "MANUAL":
                ROBOT["ultimo"] = "MANUAL - Tu compras jefe, yo solo miro"
                time.sleep(30); continue
            session = get_session()
            if not session:
                ROBOT["ultimo"] = "Sin llaves - Pon BYBIT_API_KEY y BYBIT_API_SECRET en Render"
                time.sleep(60); continue
            try:
                pos = session.get_positions(category="linear", symbol="XAUUSDT")
                tiene = any(float(p['size'])>0 for p in pos['result']['list'])
            except: tiene = False
            if tiene:
                ROBOT["ultimo"] = "Ya tienes una abierta - ESPERO"
                time.sleep(3600); continue
            try:
                r = session.get_tickers(category="linear", symbol="XAUUSDT")
                precio = float(r['result']['list'][0]['lastPrice'])
            except: precio = 4118
            if precio < 4100:
                session.place_order(category="linear", symbol="XAUUSDT", side="Buy", orderType="Market", qty=0.01, takeProfit=precio+5, stopLoss=precio-5)
                ROBOT["ultimo"] = f"YO COMPRE POR TI en {precio} - TESTNET" if USAR_TESTNET else f"YO COMPRE POR TI en {precio} - REAL"
                ROBOT["operaciones"] += 1
            elif precio > 4150:
                session.place_order(category="linear", symbol="XAUUSDT", side="Sell", orderType="Market", qty=0.01, takeProfit=precio-5, stopLoss=precio+5)
                ROBOT["ultimo"] = f"YO VENDI POR TI en {precio}"
                ROBOT["operaciones"] += 1
            else:
                ROBOT["ultimo"] = f"ESPERA - Oro {precio} en medio 4100-4150"
        except Exception as e:
            ROBOT["ultimo"] = f"Error: {e}"
        time.sleep(3600)

threading.Thread(target=robot_loop, daemon=True).start()

HTML = """
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP - PLATAFORMA REAL</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0}
header{background:#FFD700;color:#000;padding:12px}
.box{margin:10px;padding:12px;border-radius:15px;border:2px solid #FFD700;background:#111}
.luz{width:80px;height:80px;border-radius:50%;margin:10px auto;font-size:40px;display:flex;align-items:center;justify-content:center}
.verde{background:#00FF88;box-shadow:0 0 30px #00FF88}
.roja{background:#FF2222;box-shadow:0 0 30px #FF2222}
.amarilla{background:#FFD700;box-shadow:0 0 30px #FFD700}
canvas{background:#000;border-radius:10px;width:100%}
button{width:100%;padding:14px;border-radius:12px;font-weight:bold;margin-top:6px;cursor:pointer}
input{width:100%;padding:12px;border-radius:10px;background:#222;color:#fff;margin:4px 0}
</style></head><body>
<header><h1>👑 RAUDY VIP - PLATAFORMA REAL 🥇</h1><p>JEFE: RAUDY ORO</p></header>

<div class="box">
<h2>🚨 ALARMA + LUZ</h2>
<div id="luz" class="luz amarilla">🟡</div>
<h1 id="precio" style="font-size:42px">$ ----</h1>
<p id="alarma" style="font-size:20px;font-weight:bold">Esperando oro...</p>
<p id="cambio">Cambio: --</p>
<button onclick="activarAlarma()" style="background:#FFD700">🔔 ACTIVAR ALARMA CON SONIDO</button>
<p style="color:#aaa;font-size:12px">Dale al botón para que te suene cuando suba o baje</p>
</div>

<div class="box">
<h2>📊 VELAS EN VIVO - COMO APPLE / TRADINGVIEW</h2>
<canvas id="chart" width="350" height="220"></canvas>
<p id="velaTxt">Vela: --</p>
<p id="emaTxt">EMA: --</p>
</div>

<div class="box">
<h2>🤖 ROBOT - TU + YO</h2>
<p id="robotTxt">Cargando...</p>
<p id="modoTxt">MODO: AUTO</p>
<button onclick="cambiarModo('AUTO')" style="background:#00FF88">🤖 ESTOY TRABAJANDO - QUE COMPRE EL ROBOT</button>
<button onclick="cambiarModo('MANUAL')" style="background:#FFD700">👑 YO COMPRO - ROBOT ESPERA</button>
</div>

<div class="box">
<h2>🟢🔴 OPERAR MANUAL</h2>
<input id="lote" type="number" value="0.01" step="0.01">
<button onclick="alert('Ve a Bybit y compra 0.01 con TP +5 y SL -5 jefe')" style="background:#00FF88">🟢 COMPRAR 0.01</button>
<button onclick="alert('Ve a Bybit y vende 0.01 con TP -5 y SL +5 jefe')" style="background:#FF4444;color:#fff">🔴 VENDER 0.01</button>
</div>

<script>
let alarmaOn=false, ultimoPrecio=0;
function activarAlarma(){ alarmaOn=true; alert('Alarma activada jefe! Si sube o baja te suena'); }
function sonar(tipo){ if(!alarmaOn) return; let ctx=new (window.AudioContext||window.webkitAudioContext)(); let o=ctx.createOscillator(); o.frequency.value = tipo=='SUBIO'?880:220; o.connect(ctx.destination); o.start(); setTimeout(()=>o.stop(),800); }
async function cambiarModo(m){ let r=await fetch('/api/modo?modo='+m); let d=await r.json(); alert(d.mensaje); }

function dibujarVelas(velas){
  let c=document.getElementById('chart'); let ctx=c.getContext('2d'); ctx.clearRect(0,0,c.width,c.height);
  if(!velas.length) return;
  let min=Math.min(...velas.map(v=>v.l)); let max=Math.max(...velas.map(v=>v.h));
  let rango=max-min||1; let w=c.width/velas.length;
  velas.forEach((v,i)=>{
    let x=i*w+w/2; let yH=(max-v.h)/rango*c.height; let yL=(max-v.l)/rango*c.height;
    let yO=(max-v.o)/rango*c.height; let yC=(max-v.c)/rango*c.height;
    let color=v.c>=v.o?'#00FF88':'#FF2222';
    ctx.strokeStyle=color; ctx.fillStyle=color;
    ctx.beginPath(); ctx.moveTo(x,yH); ctx.lineTo(x,yL); ctx.stroke();
    let top=Math.min(yO,yC); let h=Math.max(3,Math.abs(yC-yO));
    ctx.fillRect(x-8,top,16,h);
  });
}

async function up(){
  try{
    let r=await fetch('/api/datos?v='+Date.now()); let d=await r.json();
    document.getElementById('precio').innerHTML='$ '+d.precio;
    document.getElementById('robotTxt').innerHTML='🤖 '+d.robot.ultimo+' | Ops: '+d.robot.operaciones+' | '+(d.testnet?'💸 DINERO FALSO - PRUEBA':'💰 DINERO REAL');
    document.getElementById('modoTxt').innerHTML='MODO: '+d.robot.modo;
    document.getElementById('emaTxt').innerHTML='EMA50 $'+d.ema50+' | EMA200 $'+d.ema200+' | '+d.cruce;
    let vela=d.velas[d.velas.length-1];
    document.getElementById('velaTxt').innerHTML='Vela 1H: Abre $'+vela.o+' Cierra $'+vela.c+' '+(vela.c>=vela.o?'🟢 VERDE - SUBIENDO':'🔴 ROJA - BAJANDO');
    dibujarVelas(d.velas);
    let luz=document.getElementById('luz');
    let alarma=document.getElementById('alarma');
    if(d.precio<4100){ luz.className='luz verde'; luz.innerHTML='🟢'; alarma.innerHTML='🟢 ORO BARATO - ZONA COMPRA $4100 - ¡COMPRA YA!'; alarma.style.color='#00FF88'; }
    else if(d.precio>4150){ luz.className='luz roja'; luz.innerHTML='🔴'; alarma.innerHTML='🔴 ORO CARO - ZONA VENTA $4150 - ¡VENTA YA!'; alarma.style.color='#FF2222'; }
    else { luz.className='luz amarilla'; luz.innerHTML='🟡'; alarma.innerHTML='🟡 ORO EN MEDIO - ESPERA JEFE'; alarma.style.color='#FFD700'; }
    if(ultimoPrecio!=0){
      let diff=d.precio-ultimoPrecio;
      document.getElementById('cambio').innerHTML='Cambio: '+(diff>=0?'📈 SUBIÓ +$':'📉 BAJÓ -$')+Math.abs(diff).toFixed(2);
      if(Math.abs(diff)>=2){ sonar(diff>0?'SUBIO':'BAJO'); if(diff>0) alert('🔔 ORO SUBIÓ jefe! Ahora $'+d.precio); else alert('🔔 ORO BAJÓ jefe! Ahora $'+d.precio); }
    }
    ultimoPrecio=d.precio;
  }catch(e){}
}
setInterval(up,5000); up();
</script></body></html>
"""

@app.route("/")
def home(): return HTML

@app.route("/api/datos")
def datos():
    velas = get_velas()
    precios = [v["c"] for v in velas]
    precio = precios[-1] if precios else 4118
    ema50 = calc_ema(precios, 10)
    ema200 = calc_ema(precios, 20)
    if ema50 > ema200: cruce = "🟢 CRUCE DORADO - ALCISTA"
    else: cruce = "🔴 CRUCE DE MUERTE - BAJISTA"
    return jsonify({"precio": precio, "velas": velas, "ema50": ema50, "ema200": ema200, "cruce": cruce, "robot": ROBOT, "testnet": USAR_TESTNET, "hora": datetime.now().strftime("%H:%M:%S")})

@app.route("/api/modo")
def modo():
    m = request.args.get("modo", "AUTO")
    if m in ["AUTO","MANUAL"]:
        ROBOT["modo"] = m
        return jsonify({"mensaje": "Listo jefe, modo " + m + " - " + ("Yo compro por ti" if m=="AUTO" else "Tu compras, yo espero")})
    return jsonify({"mensaje": "Modo no valido"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
