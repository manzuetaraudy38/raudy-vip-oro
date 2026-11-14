<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>👑 RAUDY VIP ORO - DOBLE ROBOT</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:0}
.top{background:#FFD700;color:#000;padding:12px;font-weight:bold;font-size:18px}
h1{font-size:38px;color:#FFD700;text-shadow:0 0 20px #FFD700;margin:15px 0 5px}
.sub{color:#00FF00;font-size:18px;font-weight:bold}
.doble{display:flex;flex-wrap:wrap;justify-content:center;gap:15px;padding:10px}
.box{border:2px solid #FFD700;border-radius:20px;padding:15px;width:340px;max-width:90%}
.box2{border-color:#00FF00}
.robot{font-size:55px}
.luces{display:flex;justify-content:center;gap:10px;margin:15px 0}
.luz{width:65px;height:65px;border-radius:50%;background:#333;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;border:3px solid #555}
.luz.on1{background:#FFD700;color:#000;box-shadow:0 0 25px #FFD700}
.luz.on2{background:#FF8800;color:#fff;box-shadow:0 0 25px #FF8800}
.luz.on3{background:#00FF00;color:#000;box-shadow:0 0 25px #00FF00}
button{background:#222;color:#fff;border:2px solid #FFD700;padding:10px 12px;border-radius:30px;font-size:14px;font-weight:bold;margin:4px}
button.activo{background:#FFD700;color:#000}
.señal{font-size:20px;font-weight:bold;margin:10px 0;min-height:50px}
.btn-ws{display:inline-block;background:#25D366;color:#fff;padding:16px 28px;font-size:20px;font-weight:bold;border-radius:50px;text-decoration:none;margin:15px 0}
.historial{text-align:left;font-size:14px;line-height:1.8}
</style>
</head>
<body>
<div class="top">🔥 PLATAFORMA GRATIS - RAUDY VIP ORO 🔥</div>
<h1>👑 RAUDY VIP ORO 👑</h1>
<div class="sub">🤖 DOBLE ROBOT - ALTA DEMANDA</div>

<div class="doble">

<!-- ROBOT 1 -->
<div class="box">
<div class="robot">🤖</div>
<h2>ROBOT 1 - RAUDY ORO 🟡</h2>
<p>Operando en: 5M - 15M - 1H</p>
<button onclick="cambiar(this,'5 MINUTOS',1)">5 MIN</button>
<button onclick="cambiar(this,'15 MINUTOS',1)" class="activo">15 MIN</button>
<button onclick="cambiar(this,'1 HORA',1)">1 HORA</button>
<p id="tiempo1">Tiempo: <b>15 MINUTOS</b></p>
<h3>🚦 AVISO DE SEÑAL</h3>
<div class="luces">
<div class="luz" id="luz1-1">LUZ 1</div>
<div class="luz" id="luz2-1">LUZ 2</div>
<div class="luz" id="luz3-1">LUZ 3</div>
</div>
<div class="señal" id="texto1">⏳ ESPERANDO SEÑAL...</div>
<button onclick="generar(1)" style="background:#00FF00;color:#000;font-size:18px">🎯 GENERAR SEÑAL R1</button>
<div class="historial" id="historial1">✅ 15M - COMPRA - GANADA 🟢<br></div>
</div>

<!-- ROBOT 2 -->
<div class="box box2">
<div class="robot">🤖</div>
<h2>ROBOT 2 - RAUDY SATELITE 🛰️</h2>
<p>Operando en: 5M - 15M - 1H</p>
<button onclick="cambiar(this,'5 MINUTOS',2)">5 MIN</button>
<button onclick="cambiar(this,'15 MINUTOS',2)" class="activo">15 MIN</button>
<button onclick="cambiar(this,'1 HORA',2)">1 HORA</button>
<p id="tiempo2">Tiempo: <b>15 MINUTOS</b></p>
<h3>🚦 AVISO DE SEÑAL</h3>
<div class="luces">
<div class="luz" id="luz1-2">LUZ 1</div>
<div class="luz" id="luz2-2">LUZ 2</div>
<div class="luz" id="luz3-2">LUZ 3</div>
</div>
<div class="señal" id="texto2">⏳ ESPERANDO SEÑAL...</div>
<button onclick="generar(2)" style="background:#00FF00;color:#000;font-size:18px">🎯 GENERAR SEÑAL R2</button>
<div class="historial" id="historial2">✅ 15M - COMPRA - GANADA 🟢<br></div>
</div>

</div>

<a class="btn-ws" href="https://wa.me/18090000000">💬 HABLAR CON RAUDY - SEÑAL VIP</a>
<p>© 2026 RAUDY VIP ORO - raudy-oro.onrender.com</p>

<script>
function cambiar(b,t,num){
  document.getElementById('tiempo'+num).innerHTML='Tiempo: <b>'+t+'</b>';
}
function generar(num){
  document.getElementById('luz1-'+num).className='luz';
  document.getElementById('luz2-'+num).className='luz';
  document.getElementById('luz3-'+num).className='luz';
  document.getElementById('texto'+num).innerHTML='🟡 LUZ 1 - ANALIZANDO...';
  setTimeout(()=>{
    document.getElementById('luz1-'+num).classList.add('on1');
    document.getElementById('texto'+num).innerHTML='🟠 LUZ 2 - 2da SEÑAL...';
    setTimeout(()=>{
      document.getElementById('luz2-'+num).classList.add('on2');
      document.getElementById('texto'+num).innerHTML='🟢 LUZ 3 - ¡COMPRA AHORA!';
      document.getElementById('luz3-'+num).classList.add('on3');
      let h=document.getElementById('historial'+num);
      let ahora=new Date().toLocaleTimeString();
      h.innerHTML='✅ '+document.getElementById('tiempo'+num).innerText+' - COMPRA - GANADA 🟢 '+ahora+'<br>'+h.innerHTML;
    },2000);
  },1500);
}
</script>
</body>
</html>
