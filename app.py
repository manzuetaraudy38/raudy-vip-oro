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
<title>RAUDY VIP PRECIO REAL</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center}
h1{color:#FFD700}
.box{border:3px solid #FFD700;border-radius:20px;padding:15px;margin:10px;display:inline-block;width:280px}
.vela{width:50px;height:110px;margin:10px auto;border-radius:10px;background:#333;border:2px solid #fff}
.verde{background:#00FF00;box-shadow:0 0 30px #00FF00}
.roja{background:#FF0000;box-shadow:0 0 30px #FF0000}
button{background:#FFD700;border:none;padding:15px 25px;font-size:18px;border-radius:10px;font-weight:bold}
.precio{font-size:32px;color:#FFD700;font-weight:bold}
#final{font-size:30px;font-weight:bold;padding:20px;border-radius:20px;margin:15px}
.real{color:#00FFFF;font-size:14px}
</style>
</head>
<body>
<h1>👑 RAUDY VIP ROBOT PRO</h1>
<h3 style='color:#00FF00'>● EN VIVO - PRECIO REAL DEL MERCADO - XAU/USD</h3>
<p>Precio Real Oro: <span class='precio' id='precio'>Cargando...</span></p>
<p class='real' id='hora'>Precio real del mercado mundial</p>
<div id='final'>Esperando...</div>
<div class='box'>
<h2>5 MINUTO</h2>
<div class='vela' id='vela5'></div>
<h2 id='t5'>...</h2>
<p id='d5'>...</p>
</div>
<div class='box'>
<h2>15 MINUTO</h2>
<div class='vela' id='vela15'></div>
<h2 id='t15'>...</h2>
<p id='d15'>...</p>
</div>
<div class='box'>
<h2>1 HORA</h2>
<div class='vela' id='vela1h'></div>
<h2 id='t1h'>...</h2>
<p id='d1h'>...</p>
</div>
<div class='box' style='border-color:#00FFFF'>
<h2>4 HORAS ⭐</h2>
<div class='vela' id='vela4h'></div>
<h2 id='t4h'>...</h2>
<p id='d4h'>...</p>
</div>
<br>
<button onclick='hablar()'>🔊 ACTIVAR VOZ</button>
<button onclick='cargar()'>🔄 VER SEÑAL</button>
<p>Raudy VIP - Precio Real XAU/USD - 5m 15m 1h 4h</p>
<script>
let vozOn=false;
let ultimaSenal='';
function hablarTexto(txt){
let u=new SpeechSynthesisUtterance(txt);
u.lang='es-ES';u.rate=1;
speechSynthesis.speak(u);
}
function hablar(){
vozOn=true;
hablarTexto('Robot Raudy activado. Precio real del mercado');
}
async function getPrecioReal(){
try{
let res=await fetch('https://data-asg.goldprice.org/dbXRates/USD.json');
let d=await res.json();
let p=d.items[0].curr+' '+d.items[0].pcurr;
let precio=parseFloat(d.items[0].pcurr);
document.getElementById('precio').innerHTML='$'+precio.toFixed(2);
let fecha=new Date(d.date);
document.getElementById('hora').innerHTML='Mercado Mundial XAU/USD - Actualizado: '+fecha.toLocaleTimeString();
return precio;
}catch(e){
return null;
}
}
async function getVela(tf){
let res=await fetch('https://api.binance.com/api/v3/klines?symbol=PAXGUSDT&interval='+tf+'&limit=2');
let d=await res.json();
let v=d[d.length-1];
return {open:parseFloat(v[1]), close:parseFloat(v[4])};
}
async function cargar(){
try{
let precioReal=await getPrecioReal();
let v5=await getVela('5m');
let v15=await getVela('15m');
let v1h=await getVela('1h');
let v4h=await getVela('4h');
if(precioReal==null){
document.getElementById('precio').innerHTML='$'+v5.close.toFixed(2)+' (PAXG)';
}
function pintar(idVela,idT,idD,v){
let el=document.getElementById(idVela);
if(v.close>v.open){el.className='vela verde';document.getElementById(idT).innerHTML='🟢 VERDE';document.getElementById(idT).style.color='#00FF00';document.getElementById(idD).innerHTML='Apertura $'+v.open.toFixed(2)+' Cierre $'+v.close.toFixed(2);return 'VERDE';}
else{el.className='vela roja';document.getElementById(idT).innerHTML='🔴 ROJA';document.getElementById(idT).style.color='#FF0000';document.getElementById(idD).innerHTML='Apertura $'+v.open.toFixed(2)+' Cierre $'+v.close.toFixed(2);return 'ROJA';}
}
let c5=pintar('vela5','t5','d5',v5);
let c15=pintar('vela15','t15','d15',v15);
let c1h=pintar('vela1h','t1h','d1h',v1h);
let c4h=pintar('vela4h','t4h','d4h',v4h);
let final=document.getElementById('final');
let verdes=[c5,c15,c1h,c4h].filter(x=>x=='VERDE').length;
let rojas=[c5,c15,c1h,c4h].filter(x=>x=='ROJA').length;
let senal='';
if(verdes>=3){
final.innerHTML='🟢🟢🟢 COMPRA - '+verdes+' DE 4 VERDES';
final.style.background='#00FF00';final.style.color='#000';
senal='COMPRA';
}else if(rojas>=3){
final.innerHTML='🔴🔴🔴 VENTA - '+rojas+' DE 4 ROJAS';
final.style.background='#FF0000';final.style.color='#fff';
senal='VENTA';
}else{
final.innerHTML='🟡 ESPERA - '+verdes+' VERDES de 4';
final.style.background='#333';final.style.color='#FFD700';
senal='ESPERA';
}
if(vozOn && senal!=ultimaSenal && (senal=='COMPRA' || senal=='VENTA')){
hablarTexto(senal+'. Tres de cuatro confirmaciones. Precio real del mercado. Oro');
ultimaSenal=senal;
}
if(senal=='ESPERA'){ultimaSenal='ESPERA';}
}catch(e){document.getElementById('precio').innerHTML='Sin internet';}
}
cargar();
setInterval(cargar,30000);
</script>
</body>
</html>
"""

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
