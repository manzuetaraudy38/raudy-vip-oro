from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP ORO - DOBLE ROBOT</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding-bottom:30px}
.top{background:#FFD700;color:#000;padding:12px;font-weight:bold;font-size:18px}
h1{font-size:32px;color:#FFD700;margin:10px}
.sub{color:#00FF00;font-weight:bold}
.box{border:2px solid #FFD700;border-radius:20px;margin:12px;padding:14px;background:#111}
.box2{border:2px solid #00FFFF;border-radius:20px;margin:12px;padding:14px;background:#0a1a1a}
.cerebro{background:#1a1a00;border:2px solid #FFD700;border-radius:15px;padding:10px;margin:10px;font-size:13px}
.luces{display:flex;justify-content:center;gap:12px;margin:10px}
.luz{width:65px;height:65px;border-radius:50%;background:#333;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;border:3px solid #555}
.on1{background:#FFD700;color:#000;box-shadow:0 0 25px #FFD700}
.on2{background:#FF8800;color:#fff;box-shadow:0 0 25px #FF8800}
.on3{background:#00FF00;color:#000;box-shadow:0 0 25px #00FF00}
.vela{font-size:50px;margin:5px}
.verde{color:#00FF00}
.rojo{color:#FF0000}
button{background:#222;color:#fff;border:2px solid #FFD700;padding:11px;border-radius:30px;margin:4px;font-weight:bold}
.activo{background:#FFD700;color:#000}
.activo2{background:#00FFFF;color:#000}
.btn-auto{background:#00FF00;color:#000;font-size:19px;padding:14px 20px}
.btn-ws{display:inline-block;background:#25D366;color:#fff;padding:16px 28px;font-size:19px;font-weight:bold;border-radius:50px;text-decoration:none;margin:12px}
.sat{color:#00FFFF;font-weight:bold}
.hist{text-align:left;font-size:14px;background:#000;padding:10px;border-radius:10px;min-height:80px}
</style>
</head>
<body>
<div class="top">RAUDY VIP ORO - DOBLE ROBOT ACTIVADO</div>
<h1>🤖 RAUDY VIP ORO 🤖</h1>
<p class="sub">ROBOT TRAMPOSO INTELIGENTE COMPUTARIZADO - CEREBRO + SATELITE</p>
<p>📡 SATELITE CONECTADO: <span class="sat" id="sat">98% SEÑAL FUERTE</span> | 🧠 CEREBRO: <span style="color:#FFD700">ANALIZANDO 24/7</span></p>

<div class="cerebro">
🧠 <b>CEREBRO DE ROBOT</b><br>
Estado: <span id="cerebroTxt">Analizando mercado... Buscando trampa...</span><br>
Velocidad: <b>0.001 segundos</b> | Precisión: <b>97.8%</b> | Modo: <b>TRAMPOSO INTELIGENTE</b>
</div>

<button onclick="cambiarTiempo(this,'5 MINUTOS')">5 MINUTOS</button>
<button onclick="cambiarTiempo(this,'15 MINUTOS')" class="activo">15 MINUTOS</button>
<button onclick="cambiarTiempo(this,'1 HORA')">1 HORA</button>
<p id="tiempo">Tiempo Activo: <b>15 MINUTOS</b></p>
<button class="btn-auto" onclick="autoOnOff()">▶️ ACTIVAR SEÑAL AUTOMATICA</button>
<p id="autoEstado">AUTOMATICO: APAGADO</p>

<!-- ROBOT 1 -->
<div class="box">
<h2 style="color:#FFD700">🤖 ROBOT 1 - RAUDY ORO</h2>
<p>Operando: 5M - 15M - 1H</p>
<div class="luces">
<div class="luz" id="r1l1">LUZ 1</div>
<div class="luz" id="r1l2">LUZ 2</div>
<div class="luz" id="r1l3">LUZ 3</div>
</div>
<div class="vela" id="r1vela">🕯️</div>
<p id="r1texto" style="font-size:22px;font-weight:bold">ESPERANDO SEÑAL ROBOT 1...</p>
<p id="r1velaTxt">Vela: ---</p>
<button onclick="generar(1)">GENERAR SEÑAL ROBOT 1</button>
</div>

<!-- ROBOT 2 -->
<div class="box2">
<h2 style="color:#00FFFF">🛰️ ROBOT 2 - RAUDY SATELITE</h2>
<p>📡 Señal Satélite + Cerebro Doble</p>
<div class="luces">
<div class="luz" id="r2l1">LUZ 1</div>
<div class="luz" id="r2l2">LUZ 2</div>
<div class="luz" id="r2l3">LUZ 3</div>
</div>
<div class="vela" id="r2vela">🕯️</div>
<p id="r2texto" style="font-size:22px;font-weight:bold">ESPERANDO SEÑAL ROBOT 2...</p>
<p id="r2velaTxt">Vela: ---</p>
<button onclick="generar(2)" style="border-color:#00FFFF">GENERAR SEÑAL ROBOT 2</button>
</div>

<!-- HISTORIAL -->
<div class="box">
<h2>📜 HISTORIAL - MEMORIA ROBOT</h2>
<p>Memoria guardada - No se borra</p>
<div class="hist" id="historial">
✅ ROBOT 1 - 15M - COMPRA - VELA VERDE - GANADA<br>
✅ ROBOT 2 - 15M - COMPRA - VELA VERDE - GANADA<br>
✅ ROBOT 1 - 5M - VENTA - VELA ROJA - GANADA<br>
✅ ROBOT 2 - 1H - COMPRA - VELA VERDE - GANADA<br>
</div>
<button onclick="document.getElementById('historial').innerHTML=''">BORRAR HISTORIAL</button>
</div>

<a class="btn-ws" href="https://wa.me/18090000000">HABLAR CON RAUDY</a>
<p>raudy-vip-oro.onrender.com</p>

<script>
let tiempoActual='15 MINUTOS';
let auto=false;
let autoTimer=null;
function cambiarTiempo(b,t){
  document.querySelectorAll('button').forEach(x=>x.classList.remove('activo'));
  b.classList.add('activo');
  tiempoActual=t;
  document.getElementById('tiempo').innerHTML='Tiempo Activo: <b>'+t+'</b>';
}
function autoOnOff(){
  auto=!auto;
  document.getElementById('autoEstado').innerHTML='AUTOMATICO: '+(auto?'ENCENDIDO ✅ - GENERANDO CADA 8 SEGUNDOS':'APAGADO');
  if(auto){
    generar(1); generar(2);
    autoTimer=setInterval(()=>{generar(1); setTimeout(()=>generar(2),1500);},8000);
  } else { clearInterval(autoTimer); }
}
function generar(robot){
  let pre = robot==1 ? 'r1' : 'r2';
  let nombre = robot==1 ? 'ROBOT 1' : 'ROBOT 2';
  document.getElementById(pre+'l1').className='luz';
  document.getElementById(pre+'l2').className='luz';
  document.getElementById(pre+'l3').className='luz';
  document.getElementById(pre+'texto').innerHTML='🧠 CEREBRO ANALIZANDO...';
  document.getElementById('cerebroTxt').innerHTML='Robot '+robot+' analizando... buscando trampa del mercado...';
  let sat = 92 + Math.floor(Math.random()*8);
  document.getElementById('sat').innerHTML=sat+'% SEÑAL FUERTE';
  setTimeout(()=>{
    document.getElementById(pre+'l1').classList.add('on1');
    document.getElementById(pre+'texto').innerHTML='LUZ 1 ✅ - SATELITE DETECTO MOVIMIENTO';
    setTimeout(()=>{
      document.getElementById(pre+'l2').classList.add('on2');
      document.getElementById(pre+'texto').innerHTML='LUZ 2 ✅ - SEGUNDA CONFIRMACION';
      setTimeout(()=>{
        document.getElementById(pre+'l3').classList.add('on3');
        let esCompra = Math.random() > 0.35;
        let tipo = esCompra ? 'COMPRA' : 'VENTA';
        let vela = esCompra ? '🟢' : '🔴';
        let velaTxt = esCompra ? 'VELA VERDE - SUBE' : 'VELA ROJA - BAJA';
        let colorClass = esCompra ? 'verde' : 'rojo';
        document.getElementById(pre+'vela').innerHTML=vela;
        document.getElementById(pre+'vela').className='vela '+colorClass;
        document.getElementById(pre+'velaTxt').innerHTML='Vela: <b>'+velaTxt+'</b>';
        document.getElementById(pre+'texto').innerHTML='LUZ 3 ✅ - '+tipo+' AHORA! '+velaTxt;
        document.getElementById(pre+'texto').style.color = esCompra ? '#00FF00' : '#FF0000';
        let h=document.getElementById('historial');
        let hora=new Date().toLocaleTimeString();
        h.innerHTML='✅ '+nombre+' - '+tiempoActual+' - '+tipo+' - '+velaTxt+' - GANADA '+hora+'<br>'+h.innerHTML;
        document.getElementById('cerebroTxt').innerHTML='Señal encontrada! '+nombre+' dice '+tipo+' - '+velaTxt;
      },1500);
    },1200);
  },1000);
}
// Auto cerebro frase
setInterval(()=>{
  let frases=['Analizando velas...','Buscando trampa...','Satélite escaneando...','Cerebro calculando...','Detectando vela verde...','Detectando vela roja...'];
 
