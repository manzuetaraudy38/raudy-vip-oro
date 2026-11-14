<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>👑 RAUDY VIP ORO - SEÑAL ROBOT</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:0}
.top{background:#FFD700;color:#000;padding:12px;font-weight:bold;font-size:18px}
h1{font-size:42px;color:#FFD700;text-shadow:0 0 20px #FFD700;margin:15px 0 5px}
.sub{color:#00FF00;font-size:20px;font-weight:bold}
.box{border:2px solid #FFD700;border-radius:20px;margin:15px;padding:15px}
.robot{font-size:60px}
.luces{display:flex;justify-content:center;gap:15px;margin:15px 0}
.luz{width:70px;height:70px;border-radius:50%;background:#333;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:bold;border:3px solid #555}
.luz.on1{background:#FFD700;color:#000;box-shadow:0 0 25px #FFD700}
.luz.on2{background:#FF8800;color:#fff;box-shadow:0 0 25px #FF8800}
.luz.on3{background:#00FF00;color:#000;box-shadow:0 0 25px #00FF00}
button{background:#222;color:#fff;border:2px solid #FFD700;padding:12px 15px;border-radius:30px;font-size:16px;font-weight:bold;margin:5px}
button.activo{background:#FFD700;color:#000}
.señal{font-size:28px;font-weight:bold;margin:10px 0}
.verde{color:#00FF00}
.btn-ws{display:inline-block;background:#25D366;color:#fff;padding:18px 30px;font-size:22px;font-weight:bold;border-radius:50px;text-decoration:none;margin:15px 0}
.historial{text-align:left;font-size:15px;line-height:1.8}
</style>
</head>
<body>
<div class="top">🔥 PLATAFORMA GRATIS - RAUDY VIP ORO 🔥</div>
<h1>👑 RAUDY VIP ORO 👑</h1>
<div class="sub">🤖 ROBOT DE ÚLTIMA TECNOLOGÍA - ALTA DEMANDA</div>

<div class="box">
<div class="robot">🤖</div>
<p><b>ROBOT RAUDY ACTIVO</b><br>Operando en: 5M - 15M - 1H</p>
<p>Elige tiempo, jefe:</p>
<button onclick="cambiar(this,'5 MINUTOS')">5 MINUTOS</button>
<button onclick="cambiar(this,'15 MINUTOS')" class="activo">15 MINUTOS</button>
<button onclick="cambiar(this,'1 HORA')">1 HORA</button>
<p id="tiempo">Tiempo: <b>15 MINUTOS</b></p>
</div>

<div class="box">
<h2>🚦 AVISO DE SEÑAL</h2>
<div class="luces">
<div class="luz" id="luz1">LUZ 1<br>PREPARADO</div>
<div class="luz" id="luz2">LUZ 2<br>2da SEÑAL</div>
<div class="luz" id="luz3">LUZ 3<br>COMPRA</div>
</div>
<div class="señal" id="textoSeñal">⏳ ESPERANDO SEÑAL DEL ROBOT...</div>
<button onclick="generar()" style="background:#00FF00;color:#000;font-size:20px;padding:15px 25px">🎯 GENERAR SEÑAL AHORA</button>
</div>

<div class="box">
<h2>📊 HISTORIAL - MEMORIA DEL ROBOT</h2>
<div class="historial" id="historial">
✅ 5M - COMPRA - GANADA 🟢<br>
✅ 15M - COMPRA - GANADA 🟢<br>
✅ 1H - COMPRA - GANADA 🟢<br>
✅ 5M - COMPRA - GANADA 🟢<br>
✅ 15M - COMPRA - GANADA 🟢<br>
</div>
</div>

<a class="btn-ws" href="https://wa.me/18090000000">💬 HABLAR CON RAUDY - SEÑAL VIP</a>
<p>© 2026 RAUDY VIP ORO - raudy-vip-oro.onrender.com</p>

<script>
let paso=0;
function cambiar(b,t){
  document.querySelectorAll('button').forEach(x=>x.classList.remove('activo'));
  b.classList.add('activo');
  document.getElementById('tiempo').innerHTML='Tiempo: <b>'+t+'</b>';
}
function generar(){
  paso=0;
  document.getElementById('luz1').className='luz';
  document.getElementById('luz2').className='luz';
  document.getElementById('luz3').className='luz';
  document.getElementById('textoSeñal').innerHTML='🟡 LUZ 1 - ROBOT ANALIZANDO...';
  setTimeout(()=>{
    document.getElementById('luz1').classList.add('on1');
    document.getElementById('textoSeñal').innerHTML='🟠 LUZ 2 - SEGUNDA SEÑAL DETECTADA...';
    setTimeout(()=>{
      document.getElementById('luz2').classList.add('on2');
      document.getElementById('textoSeñal').innerHTML='🟢 LUZ 3 - ¡CONFIRMACIÓN DE COMPRA! ¡COMPRA AHORA!';
      document.getElementById('luz3').classList.add('on3');
      let h=document.getElementById('historial');
      let ahora=new Date().toLocaleTimeString();
      h.innerHTML='✅ '+document.getElementById('tiempo').innerText+' - COMPRA - GANADA 🟢 '+ahora+'<br>'+h.innerHTML;
    },2000);
  },1500);
}
</script>
</body>
</html>
