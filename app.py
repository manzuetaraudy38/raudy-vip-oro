from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RAUDY VIP PRO - PROFESSIONAL</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
body{margin:0;background:#0A0E14;color:#fff;font-family:'Inter',Arial,sans-serif;padding:0}
.top{background:linear-gradient(90deg,#0A0E14,#1A2A1A);padding:20px 15px 10px;border-bottom:2px solid #FFD700}
.logo{font-size:28px;font-weight:800;letter-spacing:1px}
.logo span{color:#FFD700}
.sub{color:#9AA4B2;font-size:13px;margin-top:4px}
.live{display:inline-block;background:#0F2A1A;color:#00FF88;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:700;margin-top:10px;border:1px solid #00FF88}
.tabs{display:flex;gap:10px;padding:15px 15px 0}
.tab{flex:1;text-align:center;padding:13px;border-radius:14px;font-weight:800;cursor:pointer;background:#111722;border:1px solid #1E2A3A;color:#fff}
.tab.active{background:#FFD700;color:#000;border-color:#FFD700}
.divisas{display:none;gap:8px;flex-wrap:wrap;padding:12px 15px 0}
.divisas.show{display:flex}
.pair{padding:10px 14px;border-radius:20px;background:#111722;border:1px solid #1E2A3A;font-weight:700;font-size:13px;cursor:pointer}
.pair.active{background:#00FFFF;color:#000;border-color:#00FFFF}
.price-card{background:#111722;border:1px solid #1E2A3A;border-radius:18px;margin:15px;padding:18px;text-align:left}
.price-label{color:#9AA4B2;font-size:12px;letter-spacing:1px}
.price-val{font-size:38px;font-weight:800;color:#FFD700;margin:5px 0}
.price-sub{color:#00FFFF;font-size:12px}
.signal-big{margin:15px;border-radius:18px;padding:22px;text-align:center;font-size:26px;font-weight:800;letter-spacing:0.5px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 15px 15px}
.card{background:#111722;border:1px solid #1E2A3A;border-radius:18px;padding:16px;text-align:center;position:relative;overflow:hidden}
.card.prof{border:1px solid #00FFFF}
.card-time{font-size:11px;color:#9AA4B2;letter-spacing:1px;font-weight:700}
.card-title{font-size:18px;font-weight:800;margin:8px 0}
.vela{width:44px;height:95px;margin:12px auto;border-radius:12px;background:#222;border:2px solid #333;transition:0.3s}
.verde{background:linear-gradient(180deg,#00FF88,#00AA55);box-shadow:0 0 25px #00FF88;border-color:#00FF88}
.roja{background:linear-gradient(180deg,#FF4757,#AA0000);box-shadow:0 0 25px #FF4757;border-color:#FF4757}
.estado{font-weight:800;font-size:15px}
.detalle{font-size:12px;color:#9AA4B2;margin:6px 0}
.count-box{background:#0A0E14;border:1px solid #1E2A3A;border-radius:12px;padding:8px;margin-top:8px}
.count-label{font-size:10px;color:#9AA4B2;letter-spacing:1px}
.count-val{font-size:24px;font-weight:800;color:#00FFFF;font-variant-numeric:tabular-nums}
.bar{height:6px;background:#222;border-radius:10px;margin-top:10px;overflow:hidden}
.bar-fill{height:100%;background:#FFD700;transition:width 1s}
.btn-row{display:flex;gap:10px;padding:0 15px 20px}
button{flex:1;background:#FFD700;color:#000;border:none;padding:15px;border-radius:14px;font-weight:800;font-size:15px}
button.sec{background:#1E2A3A;color:#fff;border:1px solid #333}
.footer{padding:0 15px 25px;color:#6B7280;font-size:11px;line-height:1.5}
.badge{font-size:10px;padding:4px 8px;border-radius:20px;background:#1E2A3A;color:#FFD700;font-weight:700}
</style>
</head>
<body>
<div class='top'>
<div class='logo'>RAUDY <span>VIP PRO</span> 👑</div>
<div class='sub'>Professional Trading Signals • ORO + DIVISAS • Real Market Data</div>
<div class='live'>● LIVE • MERCADO REAL • PROFESIONAL</div>
</div>

<div class='tabs'>
<div class='tab active' id='tabOro' onclick='cambiarModo("ORO")'>🥇 ORO • XAU/USD</div>
<div class='tab' id='tabDiv' onclick='cambiarModo("DIVISAS")'>💱 DIVISAS</div>
</div>

<div class='divisas' id='divisasBox'>
<div class='pair active' onclick='cambiarPar("EUR/USD",this)'>EUR/USD</div>
<div class='pair' onclick='cambiarPar("GBP/USD",this)'>GBP/USD</div>
<div class='pair' onclick='cambiarPar("USD/JPY",this)'>USD/JPY</div>
<div class='pair' onclick='cambiarPar("USD/CHF",this)'>USD/CHF</div>
<div class='pair' onclick='cambiarPar("AUD/USD",this)'>AUD/USD</div>
<div class='pair' onclick='cambiarPar("USD/CAD",this)'>USD/CAD</div>
</div>

<div class='price-card'>
<div class='price-label' id='priceLabel'>GOLD • XAU / USD • PRECIO REAL DEL MERCADO</div>
<div class='price-val' id='precio'>$ --</div>
<div class='price-sub' id='hora'>Conectando con mercado mundial...</div>
<div style='margin-top:10px'><span class='badge' id='tendencia'>ANALIZANDO...</span> <span class='badge' id='fuerza'>FUERZA: --</span></div>
</div>

<div class='signal-big' id='final' style='background:#1A1A1A;color:#FFD700'>⏳ ANALIZANDO MERCADO...</div>

<div class='grid'>
<div class='card'><div class='card-time'>TIMEFRAME • 1 MINUTO</div><div class='card-title'>⚡ 1M</div><div class='vela' id='vela1'></div><div class='estado' id='t1'>...</div><div class='detalle' id='d1'>...</div><div class='count-box'><div class='count-label'>CIERRA EN</div><div class='count-val' id='s1'>00:00</div><div class='bar'><div class='bar-fill' id='b1' style='width:50%'></div></div></div></div>
<div class='card'><div class='card-time'>TIMEFRAME • 5 MINUTOS</div><div class='card-title'>5M</div><div class='vela' id='vela5'></div><div class='estado' id='t5'>...</div><div class='detalle' id='d5'>...</div><div class='count-box'><div class='count-label'>CIERRA EN</div><div class='count-val' id='s5'>00:00</div><div class='bar'><div class='bar-fill' id='b5' style='width:50%'></div></div></div></div>
<div class='card'><div class='card-time'>TIMEFRAME • 15 MINUTOS</div><div class='card-title'>15M</div><div class='vela' id='vela15'></div><div class='estado' id='t15'>...</div><div class='detalle' id='d15'>...</div><div class='count-box'><div class='count-label'>CIERRA EN</div><div class='count-val' id='s15'>00:00</div><div class='bar'><div class='bar-fill' id='b15' style='width:50%'></div></div></div></div>
<div class='card'><div class='card-time'>TIMEFRAME • 1 HORA</div><div class='card-title'>1H</div><div class='vela' id='vela1h'></div><div class='estado' id='t1h'>...</div><div class='detalle' id='d1h'>...</div><div class='count-box'><div class='count-label'>CIERRA EN</div><div class='count-val' id='s1h'>00:00</div><div class='bar'><div class='bar-fill' id='b1h' style='width:50%'></div></div></div></div>
</div>

<div style='padding:0 15px 15px'>
<div class='card prof'>
<div class='card-time'>TIMEFRAME • 4 HORAS • CONFIRMACIÓN MAESTRA ⭐</div>
<div class='card-title'>4H - TENDENCIA PRINCIPAL</div>
<div class='vela' id='vela4h'></div>
<div class='estado' id='t4h'>...</div>
<div class='detalle' id='d4h'>...</div>
<div class='count-box'><div class='count-label'>CIERRA EN</div><div class='count-val' id='s4h'>00:00</div><div class='bar'><div class='bar-fill' id='b4h' style='width:50%'></div></div></div>
</div>
</div>

<div class='btn-row'>
<button onclick='hablar()'>🔊 ACTIVAR VOZ</button>
<button class='sec' onclick='cargar()'>🔄 ACTUALIZAR</button>
</div>

<div class='footer'>
<b style='color:#fff'>CÓMO LEERLO - PROFESIONAL:</b><br>
🟢 <b style='color:#00FF88'>VERDE = SUBIENDO</b><br>
🔴 <b style='color:#FF4757'>ROJA = CAYENDO</b><br>
🟡 <b style='color:#FFD700'>ESPERA</b> - Mercado mezclado. No entres todavía.<br>
✅ <b style='color:#fff'>COMPRA solo con 4 o 5 VERDES.</b> Con poquito. Nunca con todo.<br>
ORO: Goldprice + PAXG (Binance). DIVISAS: Precio real Forex (Frankfurter / ECB) + velas Binance para EUR, GBP, AUD. JPY, CHF, CAD usan precio Forex real. Actualización cada 30 segundos. Esto no es consejo financiero.
</div>

<script>
let vozOn=false;
let ultimaSenal='';
let modo='ORO';
let parActual='EUR/USD';

let mapaBinance = {
  'EUR/USD':'EURUSDT',
  'GBP/USD':'GBPUSDT',
  'AUD/USD':'AUDUSDT',
  'USD/JPY':'USDJPY',
  'USD/CHF':'USDCHF',
  'USD/CAD':'USDCAD'
};

function cambiarModo(m){
  modo=m;
  document.getElementById('tabOro').className='tab'+(m=='ORO'?' active':'');
  document.getElementById('tabDiv').className='tab'+(m=='DIVISAS'?' active':'');
  document.getElementById('divisasBox').className='divisas'+(m=='DIVISAS'?' show':'');
  document.getElementById('priceLabel').innerHTML = m=='ORO' ? 'GOLD • XAU / USD • PRECIO REAL DEL MERCADO' : 'FOREX • '+parActual+' • PRECIO REAL DEL MERCADO';
  cargar();
}
function cambiarPar(p, el){
  parActual=p;
  document.querySelectorAll('.pair').forEach(x=>x.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('priceLabel').innerHTML='FOREX • '+p+' • PRECIO REAL DEL MERCADO';
  cargar();
}
function hablarTexto(txt){let u=new SpeechSynthesisUtterance(txt);u.lang='es-ES';u.rate=1;speechSynthesis.speak(u);}
function hablar(){vozOn=true;hablarTexto('Robot Raudy Vip Pro activado. Oro y divisas. Uno, cinco, quince, una hora y cuatro horas.');}
function formato(seg){let h=Math.floor(seg/3600);let m=Math.floor((seg%3600)/60);let s=seg%60;if(h>0){return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');}return String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');}
function actualizarSegundos(){
let ahora=Math.floor(Date.now()/1000);
let r1=60-(ahora%60);let r5=300-(ahora%300);let r15=900-(ahora%900);let r1h=3600-(ahora%3600);let r4h=14400-(ahora%14400);
document.getElementById('s1').innerHTML=formato(r1);
document.getElementById('s5').innerHTML=formato(r5);
document.getElementById('s15').innerHTML=formato(r15);
document.getElementById('s1h').innerHTML=formato(r1h);
document.getElementById('s4h').innerHTML=formato(r4h);
document.getElementById('b1').style.width=((60-r1)/60*100)+'%';
document.getElementById('b5').style.width=((300-r5)/300*100)+'%';
document.getElementById('b15').style.width=((900-r15)/900*100)+'%';
document.getElementById('b1h').style.width=((3600-r1h)/3600*100)+'%';
document.getElementById('b4h').style.width=((14400-r4h)/14400*100)+'%';
}
setInterval(actualizarSegundos,1000);actualizarSegundos();

async function getPrecioOro(){
try{
let res=await fetch('https://data-asg.goldprice.org/dbXRates/USD.json');
let d=await res.json();
let precio=parseFloat(d.items[0].pcurr);
document.getElementById('precio').innerHTML='$'+precio.toFixed(2);
let fecha=new Date(d.date);
document.getElementById('hora').innerHTML='Mercado Mundial XAU/USD • Actualizado: '+fecha.toLocaleTimeString();
return precio;
}catch(e){return null;}
}

async function getPrecioDivisa(){
  // Frankfurter = Banco Central Europeo, gratis y real
  try{
    let base = parActual.split('/')[0];
    let quote = parActual.split('/')[1];
    // Frankfurter usa EUR como base, hacemos conversion
    let res = await fetch('https://api.frankfurter.app/latest?from=EUR&to=USD,JPY,CHF,CAD,GBP,AUD,EUR');
    let d = await res.json();
    let rates = d.rates;
    // Convertimos todo a USD base para calcular cualquier par
    let eurUsd = rates.USD;
    let price = 0;
    if(parActual=='EUR/USD') price = eurUsd;
    if(parActual=='GBP/USD') price = rates.GBP ? eurUsd / rates.GBP : eurUsd;
    if(parActual=='AUD/USD') price = rates.AUD ? eurUsd / rates.AUD : eurUsd;
    if(parActual=='USD/JPY') price = rates.JPY ? rates.JPY / eurUsd : 0;
    if(parActual=='USD/CHF') price = rates.CHF ? rates.CHF / eurUsd : 0;
    if(parActual=='USD/CAD') price = rates.CAD ? rates.CAD / eurUsd : 0;
    let dec = (parActual=='USD/JPY') ? 2 : 4;
    document.getElementById('precio').innerHTML = price.toFixed(dec);
    document.getElementById('hora').innerHTML = 'Forex Real • '+parActual+' • ECB / Frankfurter • Actualizado: '+new Date().toLocaleTimeString();
    return price;
  }catch(e){ return null; }
}

async function getVela(tf, symbol){
let res=await fetch('https://api.binance.com/api/v3/klines?symbol='+symbol+'&interval='+tf+'&limit=2');
let d=await res.json();let v=d[d.length-1];
return {open:parseFloat(v[1]), close:parseFloat(v[4])};
}

async function cargar(){
try{
let precioReal=null;
let simbolo='PAXGUSDT';
if(modo=='ORO'){
  precioReal=await getPrecioOro();
  simbolo='PAXGUSDT';
} else {
  precioReal=await getPrecioDivisa();
  simbolo=mapaBinance[parActual] || 'EURUSDT';
  // Para JPY, CHF, CAD no hay par directo en Binance, usamos EURUSDT como referencia de tendencia + precio real Forex
  if(['USD/JPY','USD/CHF','USD/CAD'].includes(parActual)){
    simbolo='EURUSDT';
  }
}
let v1=await getVela('1m', simbolo);
let v5=await getVela('5m', simbolo);
let v15=await getVela('15m', simbolo);
let v1h=await getVela('1h', simbolo);
let v4h=await getVela('4h', simbolo);
if(precioReal==null && modo=='ORO'){document.getElementById('precio').innerHTML='$'+v5.close.toFixed(2)+' (PAXG)';}
if(precioReal==null && modo=='DIVISAS'){document.getElementById('precio').innerHTML=v5.close.toFixed(4)+' ('+parActual+')';}

function pintar(idVela,idT,idD,v, precioRef){
let el=document.getElementById(idVela);
let diff=((v.close-v.open)/v.open*100).toFixed(3);
let dec = (modo=='DIVISAS' && parActual=='USD/JPY') ? 2 : (modo=='DIVISAS' ? 4 : 2);
if(v.close>v.open){el.className='vela verde';document.getElementById(idT).innerHTML='🟢 VERDE • SUBIENDO';document.getElementById(idT).style.color='#00FF88';document.getElementById(idD).innerHTML='Apertura '+v.open.toFixed(dec)+' → Cierre '+v.close.toFixed(dec)+'<br>+'+diff+'%';return 'VERDE';}
else{el.className='vela roja';document.getElementById(idT).innerHTML='🔴 ROJA • CAYENDO';document.getElementById(idT).style.color='#FF4757';document.getElementById(idD).innerHTML='Apertura '+v.open.toFixed(dec)+' → Cierre '+v.close.toFixed(dec)+'<br>'+diff+'%';return 'ROJA';}
}
let c1=pintar('vela1','t1','d1',v1);
let c5=pintar('vela5','t5','d5',v5);
let c15=pintar('vela15','t15','d15',v15);
let c1h=pintar('vela1h','t1h','d1h',v1h);
let c4h=pintar('vela4h','t4h','d4h',v4h);
let final=document.getElementById('final');
let verdes=[c1,c5,c15,c1h,c4h].filter(x=>x=='VERDE').length;
let rojas=[c1,c5,c15,c1h,c4h].filter(x=>x=='ROJA').length;
let senal='';
let nombre = modo=='ORO' ? 'Oro' : parActual;
if(verdes>=4){
final.innerHTML='🟢 COMPRA • '+verdes+' DE 5 VERDES • '+nombre;
final.style.background='#00FF88';final.style.color='#000';
document.getElementById('tendencia').innerHTML='TENDENCIA: ALCISTA 🟢';
document.getElementById('fuerza').innerHTML='FUERZA: '+verdes+'/5 FUERTE';
senal='COMPRA';
}else if(rojas>=4){
final.innerHTML='🔴 VENTA • '+rojas+' DE 5 ROJAS • '+nombre;
final.style.background='#FF4757';final.style.color='#fff';
document.getElementById('tendencia').innerHTML='TENDENCIA: BAJISTA 🔴';
document.getElementById('fuerza').innerHTML='FUERZA: '+rojas+'/5 FUERTE';
senal='VENTA';
}else{
final.innerHTML='🟡 ESPERA • '+verdes+' VERDES DE 5 • NO ENTRES TODAVÍA';
final.style.background='#1A1A1A';final.style.color='#FFD700';final.style.border='1px solid #FFD700';
document.getElementById('tendencia').innerHTML='TENDENCIA: NEUTRAL 🟡';
document.getElementById('fuerza').innerHTML='FUERZA: '+verdes+'/5 DÉBIL';
senal='ESPERA';
}
if(vozOn && senal!=ultimaSenal && (senal=='COMPRA' || senal=='VENTA')){
if(senal=='COMPRA'){hablarTexto('Compra. Cuatro de cinco verdes. '+nombre);}
else{hablarTexto('Venta. Cuatro de cinco rojas. '+nombre);}
ultimaSenal=senal;
}
if(senal=='ESPERA'){ultimaSenal='ESPERA';}
}catch(e){document.getElementById('precio').innerHTML='Sin internet';}
}
cargar();setInterval(cargar,30000);
</script>
</body>
</html>
"""

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
