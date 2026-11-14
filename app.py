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
<title>RAUDY VIP ROBOT PRO</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center}
h1{color:#FFD700}
.box{border:3px solid #FFD700;border-radius:20px;padding:15px;margin:10px;display:inline-block;width:280px}
.vela{width:50px;height:110px;margin:10px auto;border-radius:10px;background:#333;border:2px solid #fff}
.verde{background:#00FF00;box-shadow:0 0 30px #00FF00}
.roja{background:#FF0000;box-shadow:0 0 30px #FF0000}
button{background:#FFD700;border:none;padding:15px 25px;font-size:18px;border-radius:10px;font-weight:bold}
.precio{font-size:26px;color:#FFD700;font-weight:bold}
#final{font-size:30px;font-weight:bold;padding:20px;border-radius:20px;margin:15px}
</style>
</head>
<body>
<h1>👑 RAUDY VIP ROBOT PRO</h1>
<h3 style='color:#00FF00'>● EN VIVO - ORO REAL - BANCO</h3>
<p>Precio Oro: <span class='precio' id='precio'>Cargando...</span></p>
<div id='final'>Esperando 3 confirmaciones...</div>
<div class='box'>
<h2>5 MINUTOS</h2>
<div class='vela' id='vela5'></div>
<h2 id='t5'>...</h2>
<p id='d5'>...</p>
</div>
<div class='box'>
<h2>15 MINUTOS</h2>
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
<br>
<button onclick='hablar()'>🔊 ACTIVAR VOZ</button>
<button onclick='cargar()'>🔄 VER SEÑAL</button>
<p>Raudy VIP - 3 Confirmaciones</p>
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
hablarTexto('Robot Raudy activado. Te aviso cuando haya compra o venta');
}
async function getVela(tf){
let res=await fetch('https://api.binance.com/api/v3/klines?symbol=PAXGUSDT&interval='+tf+'&limit=2');
let d=await res.json();
let v=d[d.length-1];
return {open:parseFloat(v[1]), close:parseFloat(v[4])};
}
async function cargar(){
try{
let v5=await getVela('5m');
let v15=await getVela('15m');
let v1h=await getVela('1h');
document.getElementById('precio').innerHTML='$'+v5.close.toFixed(2);
function pintar(idVela,idT,idD,v){
let el=document.getElementById(idVela);
if(v.close>v.open){el.className='vela verde';document.getElementById(idT).innerHTML='🟢 VERDE';document.getElementById(idT).style.color='#00FF00';document.getElementById(idD).innerHTML='Apertura $'+v.open.toFixed(2)+' Cierre $'+v.close.toFixed(2);return 'VERDE';}
else{el.className='vela roja';document.getElementById(idT).innerHTML='🔴 ROJA';document.getElementById(idT).style.color='#FF0000';document.getElementById(idD).innerHTML='Apertura $'+v.open.toFixed(2)+' Cierre $'+v.close.toFixed(2);return 'ROJA';}
}
let c5=pintar('vela5','t5','d5',v5);
let c15=pintar('vela15','t15','d15',v15);
let c1h=pintar('vela1h','t1h','d1h',v1h);
let final=document.getElementById('final');
let senal='';
if(c5=='VERDE' && c15=='VERDE' && c1h=='VERDE'){
final.innerHTML='🟢🟢🟢 COMPRA - 3 CONFIRMACIONES VERDES';
final.style.background='#00FF00';final.style.color='#000';
senal='COMPRA';
}else if(c5=='ROJA' && c15=='ROJA' && c1h=='ROJA'){
final.innerHTML='🔴🔴🔴 VENTA - 3 CONFIRMACIONES ROJAS';
final.style.background='#FF0000';final.style.color='#fff';
senal='VENTA';
}else{
let verdes=[c5,c15,c1h].filter(x=>x=='VERDE').length;
final.innerHTML='🟡 ESPERA - '+verdes+' de 3 VERDES';
final.style.background='#333';final.style.color='#FFD700';
senal='ESPERA';
}
if(vozOn && senal!=ultimaSenal && (senal=='COMPRA' || senal=='VENTA')){
hablarTexto(senal+'. Compra o venta confirmada. Oro. Tres confirmaciones');
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
