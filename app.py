<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY SEÑAL</title>
<style>
  body{ background:#0a0f0d; color:white; font-family:Arial; text-align:center; margin:0; padding:15px; }
  h1{ color:#39ff6a; font-size:32px; margin:5px; }
  .sub{ color:#aaa; font-size:13px; }
  .times button{ background:#222; color:white; border:1px solid #39ff6a; padding:10px 18px; margin:5px; border-radius:12px; font-size:18px; cursor:pointer; }
  .times button.active{ background:#39ff6a; color:black; font-weight:bold; }
  .semaforo{ background:#111; border:1px solid #39ff6a; border-radius:15px; padding:15px; margin:15px 0; }
  .luz{ width:70px; height:70px; border-radius:50%; background:#333; margin:10px auto; display:flex; align-items:center; justify-content:center; font-size:12px; }
  .on1{ background:#ffcc00; color:black; box-shadow:0 0 20px #ffcc00; }
  .on2{ background:#ffaa00; color:black; box-shadow:0 0 20px #ffaa00; }
  .on3{ background:#00ff44; color:black; box-shadow:0 0 25px #00ff44; font-weight:bold; }
  .mercado{ background:#111; border:1px solid #222; border-radius:12px; padding:12px; margin:8px 0; display:flex; justify-content:space-between; text-align:left; }
  .mercado b{ font-size:16px; }
  .mercado small{ color:#aaa; }
  .up{ color:#39ff6a; } .down{ color:#ff4444; }
  .btn{ background:#39ff6a; color:black; border:none; padding:15px; width:100%; font-size:20px; font-weight:bold; border-radius:12px; cursor:pointer; margin-top:10px; }
  .aviso{ font-size:11px; color:#aaa; margin-top:10px; }
</style>
</head>
<body>

<h1>RAUDY SEÑAL</h1>
<p class="sub">Señales educativas en tiempo real - Solo para aprender</p>

<div class="robot">
  <p>🤖 <b>Robot Raudy:</b> <span id="vozTexto">Esperando señal...</span></p>
  <button onclick="hablarRobot()">🔊 Escuchar Robot</button>
</div>

<div class="times">
  <button onclick="cambiarTiempo('5m',this)">5m</button>
  <button onclick="cambiarTiempo('15m',this)" class="active">15m</button>
  <button onclick="cambiarTiempo('1h',this)">1h</button>
</div>

<div class="semaforo">
  <h3>SEMÁFORO DE TRADING - <span id="tiempoActual">15m</span></h3>
  <div id="luz1" class="luz">LUZ 1<br>Espera</div>
  <div id="luz2" class="luz">LUZ 2<br>Confirmando</div>
  <div id="luz3" class="luz">LUZ 3<br>Confirmación</div>
  <p id="estado">Analizando historial con memoria...</p>
</div>

<h3>Lista de mercados</h3>
<div id="mercados"></div>

<button class="btn" onclick="generarSenal()">SEÑAL GRATIS</button>
<p class="aviso">Análisis con fines educativos. Los mercados son volátiles. Gestiona tu riesgo. Raudy Señal no garantiza ganancias y no es asesoría financiera.</p>

<script>
let mercados = [
  { nombre:"Divisas - EUR/USD", precio:"1.0924", cambio:"-0.12%", tipo:"down" },
  { nombre:"Acciones - Apple", precio:"$227.56", cambio:"+1.45%", tipo:"up" },
  { nombre:"Oro - XAU/USD", precio:"$2,356.10", cambio:"+0.62%", tipo:"up" },
  { nombre:"Café - Arábica", precio:"$245.80", cambio:"-0.84%", tipo:"down" },
  { nombre:"Cacao - Futuro", precio:"$7,120", cambio:"-1.27%", tipo:"down" }
];

function mostrarMercados(){
  let html = "";
  mercados.forEach(m => {
    html += `<div class="mercado"><div><b>${m.nombre}</b><br><small>En vivo demo - Raudy Señal</small></div><div><b>${m.precio}</b><br><span class="${m.tipo}">${m.cambio}</span></div></div>`;
  });
  document.getElementById("mercados").innerHTML = html;
}
mostrarMercados();

function cambiarTiempo(t, btn){
  document.getElementById("tiempoActual").innerText = t;
  document.querySelectorAll(".times button").forEach(b=>b.classList.remove("active"));
  btn.classList.add("active");
  // Reinicia luces al cambiar tiempo
  document.getElementById("luz1").className="luz";
  document.getElementById("luz2").className="luz";
  document.getElementById("luz3").className="luz";
  document.getElementById("estado").innerText = "Analizando historial de " + t + " con memoria...";
}

function hablarRobot(){
  let texto = document.getElementById("vozTexto").innerText;
  let voz = new SpeechSynthesisUtterance(texto);
  voz.lang = "es-ES";
  speechSynthesis.speak(voz);
}

function generarSenal(){
  // Simulación de memoria: revisa historial de 5m, 15m, 1h
  document.getElementById("luz1").className="luz on1";
  document.getElementById("estado").innerText = "Luz 1: Primera señal detectada...";
  document.getElementById("vozTexto").innerText = "Luz 1 activada, estoy analizando";

  setTimeout(()=>{
    document.getElementById("luz2").className="luz on2";
    document.getElementById("estado").innerText = "Luz 2: Segunda señal, confirmando...";
    document.getElementById("vozTexto").innerText = "Luz 2 activada, confirmando señal";
  }, 1500);

  setTimeout(()=>{
    document.getElementById("luz3").className="luz on3";
    document.getElementById("estado").innerText = "Luz 3 VERDE: Confirmación - Revisa tu estrategia";
    document.getElementById("vozTexto").innerText = "Luz 3 activada, revisa tu estrategia";
    hablarRobot();
    // Pequeña variación de precios demo
    mercados.forEach(m=>{ m.precio = m.precio + " "; });
    mostrarMercados();
  }, 3000);
}
</script>
</body>
</html>
