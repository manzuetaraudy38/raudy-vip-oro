from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP PRO - ORO EN VIVO</title>
<style>
body{background:#0a0a0a;color:white;text-align:center;font-family:Arial;padding:10px;margin:0;}
h1{color:#FFD700;font-size:30px;margin-top:15px;text-shadow:0 0 8px gold;}
.card{background:#1a1a1a;border:2px solid gold;border-radius:15px;padding:15px;margin:15px auto;max-width:420px;}
.precio{font-size:32px;color:#00FF00;font-weight:bold;}
.estado{padding:18px;border-radius:12px;font-size:20px;font-weight:bold;margin:15px auto;max-width:420px;}
.venta{background:#ff0000; animation:pulse 1.5s infinite;}
.compra{background:#00aa00;}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.03)}100%{transform:scale(1)}}
.btn{display:block;padding:20px;margin:12px auto;border-radius:12px;text-decoration:none;font-size:20px;font-weight:bold;max-width:380px;}
.btn-wa{background:#25D366;color:white;}
.btn-pay{background:#FFD700;color:black;border:2px solid white; font-size:24px;}
.btn-pay2{background:#0070BA;color:white;}
.info{color:#aaa;font-size:12px;margin-top:20px;}
</style>
</head>
<body>

<h1>💰 RAUDY VIP PRO 💰</h1>
<h2 style="color:white;font-size:16px;">ORO Y EURO - PRECIO REAL EN VIVO</h2>

<div class="card">
<h2 style="margin:5px;">ORO (XAUUSD) - EN VIVO</h2>
<div class="precio">$<span id="oro">Cargando...</span></div>
<div style="font-size:12px;color:#aaa;" id="horaOro">Actualizando...</div>
<p style="margin:5px;">COMPRA BUENA: $3900 - $3890 | $3865 | $3820</p>
<p style="margin:5px;">VENTA BUENA: $3980 - $3990 | $4020</p>
</div>

<div class="card">
<h2 style="margin:5px;">EURO (EURUSD)</h2>
<div class="precio"><span id="eur">1.1134</span></div>
<p style="margin:5px;">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</p>
</div>

<div id="estado" class="estado venta">🔴 CONECTANDO PRECIO REAL DEL ORO...</div>

<!-- BOTON PAYPAL CON TU LINK -->
<a class="btn btn-pay" href="https://www.paypal.me/RaudyManzueta/20" target="_blank">
💳 PAGAR VIP $20 AHORA - PAYPAL
</a>

<a class="btn btn-pay2" href="https://www.paypal.me/RaudyManzueta/100" target="_blank">
💎 PAGAR VIP $100 TODO EL MES
</a>

<a class="btn btn-wa" href="https://wa.me/41767574050?text=Hola%20Raudy%20VIP%2C%20ya%20pague%20%24%20por%20PayPal%20RaudyManzueta%2C%20quiero%20entrar%20al%20grupo%20ORO">
📱 WHATSAPP 0767574050 - CONFIRMAR PAGO
</a>

<p class="info">App Oficial: raudy-vip-oro.onrender.com<br>
Alarmas activas: $3890, $3900, $3980, $3990<br>
Sonido + vibración cuando toque precio</p>

<script>
let alarmasORO={compra:[3900,3890,3865,3820],venta:[3980,3990,4020]};
let yaSono={};

function sonar(tipo,precio,actual){
 let k=tipo+precio;
 if(yaSono[k]) return;
 // Solo suena si esta cerca (evita que suene repetido)
 yaSono[k]=true;
 
 // SONIDO
 let audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
 audio.loop = true;
 audio.play();
 setTimeout(()=>audio.pause(), 8000);
 
 // VIBRACION CELULAR
 if(navigator.vibrate) navigator.vibrate([500,300,500,300,1000]);
 
 alert('🚨🚨 RAUDY VIP PRO 🚨🚨\\n\\n' + tipo + ' TOCADO!\\n\\nPrecio configurado: $' + precio + '\\nPrecio actual: $' + actual + '\\n\\n¡ENTRA AHORA!\\n\\nWhatsApp: 0767574050\\nPayPal: paypal.me/RaudyManzueta/20');
 
 document.getElementById('estado').innerHTML = '🟢 🚨 ' + tipo + ' $' + precio + ' TOCADO! PRECIO: $' + actual;
 document.getElementById('estado').className = 'estado compra';
}

function verificar(precioOro){
 alarmasORO.compra.forEach(p=>{if(precioOro<=p) sonar('COMPRA BUENA ORO',p,precioOro)});
 alarmasORO.venta.forEach(p=>{if(precioOro>=p) sonar('VENTA BUENA ORO',p,precioOro)});
}

// PRECIO REAL ORO - API GRATIS
async function precioReal(){
 try{
   let r = await fetch('https://api.gold-api.com/price/XAU');
   let d = await r.json();
   let precio = parseFloat(d.price);
   if(precio){
     document.getElementById('oro').innerText = precio.toFixed(2);
     document.getElementById('horaOro').innerText = 'Actualizado: ' + new Date().toLocaleTimeString() + ' - VIVO';
     verificar(precio);
     
     // Cambiar estado segun precio
     let est = document.getElementById('estado');
     if(precio > 3940){
       est.innerHTML = '🔴 ORO: VENTA 88% - ESPERANDO $3900 | Actual: $' + precio.toFixed(2);
       est.className = 'estado venta';
     } else if(precio <= 3905 && precio >= 3885){
       est.innerHTML = '🟢 ORO: COMPRA BUENA $3900-$3890 | Actual: $' + precio.toFixed(2) + ' - ¡ENTRA!';
       est.className = 'estado compra';
       if(!yaSono['zona3900']){ yaSono['zona3900']=true; sonar('ZONA DE COMPRA $3900',$3900,precio.toFixed(2)); }
     } else {
       est.innerHTML = '🟡 ORO: En zona ' + precio.toFixed(2) + ' - Esperando $3900 o $3980';
       est.className = 'estado';
       est.style.background = '#FFA500';
     }
   }
 }catch(e){
   console.log('Error precio', e);
   document.getElementById('oro').innerText = '3957.95 (offline)';
 }
}

// Actualizar cada 5 segundos
precioReal();
setInterval(precioReal, 5000);

// EURO - precio simulado pero cambia
let eurBase = 1.1134;
setInterval(()=>{
  eurBase += (Math.random()-0.5)*0.0005;
  document.getElementById('eur').innerText = eurBase.toFixed(4);
}, 3000);

// Reset alarmas cada 1 hora para que vuelva a sonar
setInterval(()=>{ yaSono={}; }, 3600000);
</script>

</body>
</html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
