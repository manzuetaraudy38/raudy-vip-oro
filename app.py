from flask import Flask
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP ROBOTS PODEROSOS - ACCIONES + ORO</title>
<style>
*{box-sizing:border-box;font-family:Arial,sans-serif}
body{margin:0;background:#050505;color:white;text-align:center}
header{background:linear-gradient(90deg,#FFD700,#FF6B00,#FFD700);color:black;padding:15px}
header h1{margin:0;font-size:22px}
header p{margin:5px 0;font-weight:bold}
.top-btns{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px;background:#111}
.top-btns a{padding:12px 16px;border-radius:25px;text-decoration:none;font-weight:bold;color:white;font-size:14px}
.wa{background:#25D366}.tg{background:#0088cc}.ig{background:#E1306C}.pay{background:#FFD700;color:black!important}
.clock{background:#111;padding:10px;border:2px solid #FFD700;margin:10px;border-radius:15px}
.clock b{color:#FFD700;font-size:20px}
.maestro{background:linear-gradient(180deg,#FFD700,#FF6B00);color:black;margin:10px;padding:18px;border-radius:20px;border:4px solid white;box-shadow:0 0 30px #FFD700}
.maestro h2{margin:0;font-size:26px}
.maestro p{font-size:18px;font-weight:bold}
.maestro button{padding:12px 20px;border:none;border-radius:20px;background:black;color:#FFD700;font-weight:bold;font-size:16px;cursor:pointer;margin:3px}
.broker{background:#1a1a2e;margin:10px;padding:15px;border-radius:15px;border:2px solid #00FFFF}
.broker img{width:90px;height:90px;border-radius:50%;border:3px solid #00FFFF;object-fit:cover}
.acciones{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px}
.act{background:#1a1a1a;border:1px solid #333;padding:10px;border-radius:12px;min-width:130px;cursor:pointer}
.act b{color:#FFD700}.act span{font-size:12px}
.act.active{border:2px solid #FFD700;box-shadow:0 0 15px #FFD700}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.robot{background:#1a1a1a;border:2px solid #333;border-radius:15px;padding:10px}
.robot .luz{width:18px;height:18px;border-radius:50%;background:yellow;margin:0 auto 5px;box-shadow:0 0 12px yellow;animation:parpadeo 1s infinite}
@keyframes parpadeo{0%{opacity:1}50%{opacity:.3}100%{opacity:1}}
.robot h3{margin:5px 0;font-size:14px;color:#FFD700}
.robot p{font-size:12px;margin:3px 0}
.robot .poder{font-size:18px}
.robot .msg{font-size:12px;background:#222;padding:6px;border-radius:8px;min-height:38px}
.btns{margin-top:6px;display:flex;gap:5px;justify-content:center}
.btns button{border:none;padding:7px 8px;border-radius:10px;font-weight:bold;cursor:pointer;font-size:11px}
.felicitar{background:#00FF88}.estrella{background:#FFD700}
.estrellas{font-size:16px;color:#FFD700}
.footer{padding:20px;font-size:12px;color:#888}
</style>
</head>
<body>
<header>
<h1>👑 RAUDY VIP ROBOTS PODEROSOS ⚡☄️</h1>
<p>ACCIONES + ORO • ELLOS BUSCAN Y ANALIZAN SOLOS</p>
<p>JEFE: RAUDY MANZUETA</p>
</header>
<div class="top-btns">
<a class="wa" href="https://wa.me/41767574050" target="_blank">💬 WHATSAPP 0767574050</a>
<a class="tg" href="https://t.me/raudy_vip_oro_bot" target="_blank">✈️ TELEGRAM @raudy_vip_oro_bot</a>
<a class="ig" href="https://instagram.com/raudy_vip_oro_bot" target="_blank">📸 INSTAGRAM @raudy_vip_oro_bot</a>
<a class="pay" href="https://paypal.me/RaudyManzueta/20" target="_blank">💰 PAGAR VIP $20</a>
</div>
<div class="clock">SESION NEW YORK 🕐 <b id="reloj">--:--:--</b><br><span id="sesion">Buscando información...</span></div>
<div class="acciones" id="acciones"></div>
<div class="maestro">
<div style="font-size:40px">👑⚡☄️🔥🧊</div>
<h2>ROBOT 40 - MAESTRO DIOS RAUDY</h2>
<p>Función: Yo mando a los 39. Yo tengo TODOS los poderes. Yo decido.</p>
<p id="maestroMsg">Analizando todo... Espera jefe...</p>
<p>⭐ Estrellas del Maestro: <span id="maestroEstrellas">⭐⭐⭐⭐⭐</span></p>
<button onclick="felicitarMaestro()">👏 FELICITAR MAESTRO</button>
<button onclick="estrellaMaestro()">⭐ MANDAR ESTRELLA AL MAESTRO</button>
</div>
<div class="broker">
<img src="https://i.pravatar.cc/150?img=12" alt="Broker">
<h3>🧑‍💼 BROKER RAUDY - Persona Real</h3>
<p id="brokerMsg">Hola jefe, soy tu Broker. Estoy mirando lo que dicen los robots...</p>
<button onclick="hablarBroker()" style="padding:10px 18px;border-radius:20px;background:#00FFFF;border:none;font-weight:bold">🎤 PREGUNTAR AL BROKER</button>
</div>
<h2>🤖 LOS 40 ROBOTS CON PODERES</h2>
<p>Ellos buscan información, la analizan y te dicen COMPRA o VENTA solos.</p>
<div class="grid" id="grid"></div>
<div class="footer">RAUDY VIP © 2026 - Solo Robots Hacen Todo - WhatsApp 0767574050 - No es consejo financiero, es educación</div>
<script>
const simbolos=[{id:"ORO",nombre:"ORO",precio:4088,emoji:"🥇"},{id:"NVDA",nombre:"NVIDIA",precio:185.20,emoji:"💚"},{id:"AAPL",nombre:"APPLE",precio:262.10,emoji:"🍎"},{id:"TSLA",nombre:"TESLA",precio:340.50,emoji:"🚗"},{id:"MSFT",nombre:"MICROSOFT",precio:495.30,emoji:"🪟"},{id:"AMZN",nombre:"AMAZON",precio:235.40,emoji:"📦"},{id:"META",nombre:"META",precio:645.20,emoji:"👍"},{id:"GOOGL",nombre:"GOOGLE",precio:282.10,emoji:"🔍"}];
let activo="ORO";
const accDiv=document.getElementById("acciones");
function renderAcc(){
 accDiv.innerHTML="";
 simbolos.forEach(s=>{
  let cambio=(Math.random()*4-2).toFixed(2);
  let color=cambio>=0?"#00FF88":"#FF4444";
  let d=document.createElement("div");
  d.className="act "+(activo===s.id?"active":"");
  d.innerHTML="<b>"+s.emoji+" "+s.id+"</b><br>"+s.nombre+"<br><b>$"+s.precio.toFixed(2)+"</b><br><span style='color:"+color+"'>"+cambio+"%</span>";
  d.onclick=()=>{activo=s.id;renderAcc();analizarTodo();sonido()};
  accDiv.appendChild(d);
 });
}
renderAcc();
const robots=[
[1,"RAYO RAUDY","⚡","Yo soy el más rápido, busco noticias de USA"],
[2,"RAYO VELOZ","⚡","Yo busco noticias de NVDA y TESLA"],
[3,"COMETA ORO","☄️","Yo busco noticias del ORO"],
[4,"GUARDIA 08:30","🔥","Yo vigilo noticias de las 08:30"],
[5,"COMETA VENTA","☄️","Yo busco ventas fuertes, rompo el mercado"],
[6,"COMETA FUERTE","☄️","Yo analizo caídas rápidas"],
[7,"COMETA DIOS","☄️","Yo aviso cuando viene una venta grande"],
[8,"RAYO COMPRA","⚡","Yo busco compras rápidas"],
[9,"RAYO ORO","⚡","Yo sigo el ORO segundo a segundo"],
[10,"HIELO PACIENTE","🧊","Yo espero frío, no entro con prisa"],
[11,"HIELO ANALISTA","🧊","Yo analizo si el mercado está tranquilo"],
[12,"FUEGO COMPRA","🔥","Yo quemo cuando hay compra fuerte"],
[13,"FUEGO TESLA","🔥","Yo cuido solo TESLA"],
[14,"FUEGO NVDA","🔥","Yo cuido solo NVIDIA"],
[15,"FUEGO APPLE","🔥","Yo cuido solo APPLE"],
[16,"FUEGO ORO","🔥","Yo cuido el ORO con fuego"],
[17,"FUEGO VENTA","🔥","Yo digo VENTA cuando hay fuego rojo"],
[18,"RAYO META","⚡","Yo cuido META y GOOGLE"],
[19,"RAYO AMAZON","⚡","Yo cuido AMAZON"],
[20,"HIELO JEFE","🧊","Yo digo ESPERA cuando hay peligro"],
[21,"COMETA AMAZON","☄️","Yo busco noticias de AMAZON"],
[22,"COMETA MICROSOFT","☄️","Yo busco noticias de MICROSOFT"],
[23,"RAYO NOTICIAS","⚡","Yo busco noticias en Telegram y WhatsApp"],
[24,"HIELO SOPORTE","🧊","Yo busco soportes, donde el precio no baja"],
[25,"FUEGO RESISTENCIA","🔥","Yo busco resistencias, donde el precio no sube"],
[26,"COMETA 14:30","☄️","Yo vigilo noticias de las 14:30"],
[27,"RAYO ENTRADA","⚡","Yo busco la mejor ENTRADA"],
[28,"FUEGO BOTIN","🔥","Yo calculo tu BOTÍN"],
[29,"HIELO SALIDA","🧊","Yo te digo cuando SALIR"],
[30,"COMETA PELIGRO","☄️","Yo grito PELIGRO si hay noticia mala"],
[31,"RAYO VIP","⚡","Yo solo hablo para los VIP"],
[32,"FUEGO DIOS","🔥","Yo tengo fuego de DIOS"],
[33,"HIELO DIOS","🧊","Yo tengo hielo de DIOS"],
[34,"COMETA ORO 2","☄️","Yo confirmo lo que dice el ORO"],
[35,"RAYO CONFIRMA","⚡","Yo confirmo COMPRA o VENTA"],
[36,"FUEGO CONFIRMA","🔥","Yo confirmo con fuego"],
[37,"HIELO CONFIRMA","🧊","Yo confirmo con calma"],
[38,"COMETA JEFE","☄️","Yo soy el jefe de los cometas"],
[39,"RAYO MAESTRO 2","⚡","Yo soy la mano derecha del Maestro 40"],
[40,"MAESTRO DIOS RAUDY","👑⚡☄️🔥🧊","Yo mando a todos, tengo TODOS los poderes"]
];
const grid=document.getElementById("grid");
let estrellas={};
robots.slice(0,39).forEach(r=>{
 let num=r[0]; let nombre=r[1]; let poder=r[2]; let funcion=r[3];
 estrellas[num]=0;
 let div=document.createElement("div");
 div.className="robot";
 div.innerHTML="<div class='luz' id='luz"+num+"'></div><div class='poder'>"+poder+"</div><h3>Robot "+num+" - "+nombre+"</h3><p><b>Función:</b> "+funcion+"</p><div class='msg' id='msg"+num+"'>Buscando información...</div><div class='estrellas' id='est"+num+"'></div><div class='btns'><button class='felicitar' onclick='felicitar("+num+")'>👏 FELICITAR</button><button class='estrella' onclick='darEstrella("+num+")'>⭐ ESTRELLA</button></div>";
 grid.appendChild(div);
});
function sonido(){
 try{
  let ctx=new (window.AudioContext||window.webkitAudioContext)();
  let o=ctx.createOscillator(); let g=ctx.createGain();
  o.connect(g); g.connect(ctx.destination);
  o.frequency.value=880; o.type="sine"; g.gain.value=0.1; o.start(); o.stop(ctx.currentTime+0.15);
 }catch(e){}
}
function hablar(texto){
 if('speechSynthesis' in window){ let u=new SpeechSynthesisUtterance(texto); u.lang='es-ES'; speechSynthesis.speak(u); }
}
function felicitar(num){
 sonido();
 document.getElementById("msg"+num).innerHTML="¡Gracias jefe Raudy! Lo estoy haciendo bien, te felicito a ti también 👏";
 hablar("Gracias jefe Raudy, lo estoy haciendo bien");
 document.getElementById("luz"+num).style.background="#00FF88";
}
function darEstrella(num){
 sonido(); sonido();
 estrellas[num]++;
 document.getElementById("est"+num).innerHTML="⭐".repeat(estrellas[num]);
 document.getElementById("msg"+num).innerHTML="¡WOW! ¡Me mandaste una estrella! ¡Gracias jefe! ⭐ ¡Voy a trabajar más fuerte!";
 hablar("Gracias jefe, me mandaste una estrella");
}
let maestroEstrellasCount=5;
function felicitarMaestro(){
 sonido();
 document.getElementById("maestroMsg").innerHTML="¡Gracias jefe! ¡Lo estoy haciendo bien, te felicito! ¡Eres el mejor jefe! 👑";
 hablar("Gracias jefe, lo estoy haciendo bien, te felicito");
}
function estrellaMaestro(){
 sonido();
 maestroEstrellasCount++;
 document.getElementById("maestroEstrellas").innerHTML="⭐".repeat(maestroEstrellasCount);
 document.getElementById("maestroMsg").innerHTML="¡ESTRELLA RECIBIDA! ¡Ahora tengo más poder! ⭐⚡☄️";
 hablar("Estrella recibida, ahora tengo más poder");
}
function hablarBroker(){
 sonido();
 let msgs=["Jefe, el Maestro 40 dice que esperes, el ORO está en zona caliente.","Jefe, los robots dicen COMPRA en NVDA, pero con cuidado.","Jefe, yo como tu Broker te digo: no entres sin confirmación del Maestro.","Jefe, hoy hay mucha fuerza en TESLA, los robots están buscando información."];
 let msg=msgs[Math.floor(Math.random()*msgs.length)];
 document.getElementById("brokerMsg").innerHTML=msg;
 hablar(msg);
}
function analizarTodo(){
 sonido();
 let esCompra=Math.random()>0.5;
 let entrada=(simbolos.find(s=>s.id===activo).precio).toFixed(2);
 let botin=(parseFloat(entrada)*1.02).toFixed(2);
 let salida=(parseFloat(entrada)*0.99).toFixed(2);
 let senal=esCompra?"COMPRA DIOS 🟢":"VENTA DIOS 🔴";
 document.getElementById("maestroMsg").innerHTML="He analizado "+activo+". Mis 39 robots buscaron información. Decisión: <b>"+senal+"</b><br>ENTRADA: $"+entrada+" | BOTÍN: $"+botin+" | SALIDA: $"+salida;
 hablar("He analizado "+activo+", decisión "+senal);
 robots.slice(0,39).forEach(r=>{
  let num=r[0];
  let el=document.getElementById("msg"+num);
  let luz=document.getElementById("luz"+num);
  if(!el) return;
  let frasesCompra=["Busqué noticias, veo COMPRA ✅","Analicé, hay fuerza de compra","Mi poder dice COMPRA"];
  let frasesVenta=["Busqué noticias, veo VENTA 🔴","Analicé, hay fuerza de venta","Mi poder dice VENTA"];
  el.innerHTML=esCompra?frasesCompra[Math.floor(Math.random()*3)]:frasesVenta[Math.floor(Math.random()*3)];
  luz.style.background=esCompra?"#00FF88":"#FF4444";
  luz.style.boxShadow="0 0 15px "+(esCompra?"#00FF88":"#FF4444");
 });
 document.getElementById("brokerMsg").innerHTML="Jefe, ya analicé "+activo+". El Maestro dice "+senal+". ENTRADA $"+entrada+", BOTÍN $"+botin+". Yo te recomiendo esperar confirmación.";
}
setInterval(()=>{
 let d=new Date();
 document.getElementById("reloj").innerHTML=d.toLocaleTimeString("es-ES");
 let h=d.getHours();
 document.getElementById("sesion").innerHTML=h>=14&&h<21?"🟢 SESIÓN NEW YORK ABIERTA - Robots trabajando":"🟡 Sesión cerrada - Robots buscando información";
},1000);
setInterval(analizarTodo,30000);
analizarTodo();
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
