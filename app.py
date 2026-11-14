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
<title>RAUDY VIP ORO - SENAL ROBOT</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0}
.top{background:#FFD700;color:#000;padding:12px;font-weight:bold}
h1{font-size:38px;color:#FFD700}
.box{border:2px solid #FFD700;border-radius:20px;margin:15px;padding:15px}
.luces{display:flex;justify-content:center;gap:15px}
.luz{width:70px;height:70px;border-radius:50%;background:#333;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;border:3px solid #555}
.on1{background:#FFD700;color:#000;box-shadow:0 0 25px #FFD700}
.on2{background:#FF8800;color:#fff;box-shadow:0 0 25px #FF8800}
.on3{background:#00FF00;color:#000;box-shadow:0 0 25px #00FF00}
button{background:#222;color:#fff;border:2px solid #FFD700;padding:12px;border-radius:30px;margin:5px;font-weight:bold}
.activo{background:#FFD700;color:#000}
.btn-ws{display:inline-block;background:#25D366;color:#fff;padding:18px 30px;font-size:20px;font-weight:bold;border-radius:50px;text-decoration:none;margin:15px}
</style>
</head>
<body>
<div class="top">PLATAFORMA GRATIS - RAUDY VIP ORO</div>
<h1>RAUDY VIP ORO</h1>
<p style="color:#00FF00;font-weight:bold">ROBOT DE ULTIMA TECNOLOGIA - ALTA DEMANDA</p>
<div class="box">
<div style="font-size:60px">🤖</div>
<p><b>ROBOT RAUDY ACTIVO</b><br>Operando: 5M - 15M - 1H</p>
<button onclick="cambiar(this,'5 MINUTOS')">5 MINUTOS</button>
<button onclick="cambiar(this,'15 MINUTOS')" class="activo">15 MINUTOS</button>
<button onclick="cambiar(this,'1 HORA')">1 HORA</button>
<p id="tiempo">Tiempo: <b>15 MINUTOS</b></p>
</div>
<div class="box">
<h2>AVISO DE SENAL</h2>
<div class="luces">
<div class="luz" id="luz1">LUZ 1</div>
<div class="luz" id="luz2">LUZ 2</div>
<div class="luz" id="luz3">LUZ 3</div>
</div>
<p id="texto" style="font-size:24px;font-weight:bold">ESPERANDO SENAL...</p>
<button onclick="generar()" style="background:#00FF00;color:#000;font-size:20px">GENERAR SENAL AHORA</button>
</div>
<div class="box">
<h2>HISTORIAL - MEMORIA ROBOT</h2>
<div id="historial" style="text-align:left">✅ 5M - COMPRA - GANADA<br>✅ 15M - COMPRA - GANADA<br>✅ 1H - COMPRA - GANADA<br></div>
</div>
<a class="btn-ws" href="https://wa.me/18090000000">HABLAR CON RAUDY</a>
<p>raudy-vip-oro.onrender.com</p>
<script>
function cambiar(b,t){document.querySelectorAll('button').forEach(x=>x.classList.remove('activo'));b.classList.add('activo');document.getElementById('tiempo').innerHTML='Tiempo: <b>'+t+'</b>';}
function generar(){
document.getElementById('luz1').className='luz';
document.getElementById('luz2').className='luz';
document.getElementById('luz3').className='luz';
document.getElementById('texto').innerHTML='LUZ 1 - ROBOT ANALIZANDO...';
setTimeout(()=>{
document.getElementById('luz1').classList.add('on1');
document.getElementById('texto').innerHTML='LUZ 2 - SEGUNDA SENAL...';
setTimeout(()=>{
document.getElementById('luz2').classList.add('on2');
document.getElementById('texto').innerHTML='LUZ 3 - CONFIRMACION DE COMPRA! COMPRA AHORA!';
document.getElementById('luz3').classList.add('on3');
let h=document.getElementById('historial');
h.innerHTML='✅ '+document.getElementById('tiempo').innerText+' - COMPRA - GANADA '+new Date().toLocaleTimeString()+'<br>'+h.innerHTML;
},2000);
},1500);
}
</script>
</body>
</html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
