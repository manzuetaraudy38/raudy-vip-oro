# JEFE BOT - CUADRITOS TODO JUNTO - JEFE ORO
import os
from flask import Flask, request, jsonify
app = Flask(__name__)
ultima = {"accion": "ESPERANDO", "precio": "", "hora": ""}

HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>JEFE ORO - CUADRITOS</title>
<style>
body{background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:5px;margin:0}
h1{font-size:26px;margin:3px} h2{color:#FFD700;margin:3px;font-size:18px}
.voz{background:#FFD700;color:black;padding:14px;border-radius:15px;font-size:18px;font-weight:bold;border:none;width:98%}
#senal{font-size:22px;font-weight:bold;padding:12px;border-radius:15px;margin:8px;background:#333}
.regla{background:#1a1a1a;padding:8px;border-radius:12px;margin:8px;font-size:15px}
.cuadricula{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:2px}
.cajaGrafico{background:#111;border-radius:12px;overflow:hidden;border:2px solid #333}
.cajaGrafico.grande{grid-column:span 2;border-color:#FFD700}
.titulo{font-size:15px;font-weight:bold;padding:6px;background:#222}
.grafico{height:230px}
.graficoGrande{height:260px}
</style></head>
<body>
<h1>👑 JEFE ORO 👑</h1>
<h2>TODO JUNTO - 5 CUADRITOS</h2>

<button class="voz" onclick="activar()">🔊 ACTIVAR VOZ JEFE 🔊</button>
<div id="senal">⏳ ESPERANDO... MIRA LOS CUADRITOS, JEFE</div>

<div class="regla">
🟢🟢🟢🟢🟢 TODO VERDE = COMPRA JEFE<br>
🔴🔴🔴🔴🔴 TODO ROJO = VENTA JEFE<br>
🟢🔴 MEZCLADO = ESPERA JEFE
</div>

<div class="cuadricula">

  <div class="cajaGrafico">
    <div class="titulo">1️⃣ 1 MINUTO 🟢🔴</div>
    <div class="grafico"><div id="tv1"></div></div>
  </div>

  <div class="cajaGrafico">
    <div class="titulo">2️⃣ 5 MINUTOS 🟢🔴</div>
    <div class="grafico"><div id="tv5"></div></div>
  </div>

  <div class="cajaGrafico">
    <div class="titulo">3️⃣ 15 MINUTOS 🟢🔴</div>
    <div class="grafico"><div id="tv15"></div></div>
  </div>

  <div class="cajaGrafico">
    <div class="titulo">4️⃣ 1 HORA 🟢🔴</div>
    <div class="grafico"><div id="tv60"></div></div>
  </div>

  <div class="cajaGrafico grande">
    <div class="titulo">5️⃣ 4 HORAS - JEFE GRANDE 👑</div>
    <div class="graficoGrande"><div id="tv240"></div></div>
  </div>

</div>

<p>JEFE OK - ORO REAL</p>

<script src="https://s3.tradingview.com/tv.js"></script>
<script>
function crear(id, intervalo, alto){
  new TradingView.widget({"width":"100%","height":alto,"symbol":"OANDA:XAUUSD","interval":intervalo,"timezone":"America/Santo_Domingo","theme":"dark","style":"1","locale":"es","container_id":id});
}
crear("tv1","1",230); crear("tv5","5",230); crear("tv15","15",230); crear("tv60","60",230); crear("tv240","240",260);
var vozOn=false; var ultimaHablada="";
function hablar(t){ var v=new SpeechSynthesisUtterance(t); v.lang='es-ES'; speechSynthesis.cancel(); speechSynthesis.speak(v); }
function activar(){ vozOn=true; hablar('Jefe Oro listo. Cinco cuadritos, jefe. Todo junto, jefe. Cuando todo este verde, compra, jefe. Cuando todo este rojo, venta, jefe.'); }
async function revisar(){
  try{
    var r=await fetch('/
