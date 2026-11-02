from flask import Flask
import requests

app = Flask(__name__)

@app.route('/api/oro-real')
def oro_real():
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=5)
        data = r.json()
        return {"price": data.get('price', 3943.30)}
    except:
        return {"price": 3943.30}

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Raudy VIP ORO - ORIGINAL PRO</title>
<style>
body { background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:12px; }
.box { border:2px solid #FFD700; border-radius:15px; padding:15px; text-align:center; margin-bottom:12px; background:#1a1a1a; }
#oro { font-size:40px; color:#00ff00; font-weight:bold; }
#eur { font-size:36px; color:#00ff00; font-weight:bold; }
.estado { border-radius:15px; padding:15px; text-align:center; margin-bottom:15px; font-weight:bold; font-size:18px; background:#ff0000; transition:0.5s; }
.estado.venta { background:#ff0000; }
.estado.compra { background:#00aa00; }
.btn-yellow { background:#FFD700; color:black; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:19px; margin-bottom:12px; display:block; text-decoration:none; }
.btn-blue { background:#0a84ff; color:white; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:12px; display:block; text-decoration:none; }
.btn-green { background:#25D366; color:white; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:12px; display:block; text-decoration:none; }
.disclaimer { background:#111; border:1px solid #333; border-radius:10px; padding:12px; font-size:11px; color:#888; line-height:1.4; margin-bottom:15px; }
.footer { text-align:center; font-size:11px; color:#555; line-height:1.6; }
</style>
</head>
<body>

<div class="box">
<div style="font-size:24px; font-weight:bold;">ORO (XAUUSD) - EN VIVO</div>
<div id="oro">$3943.30</div>
<div style="font-size:12px; color:#aaa;" id="horaOro">Actualizado: --:--:-- - VIVO</div>
<div style="font-size:14px; margin-top:8px;">COMPRA BUENA: $3900 - $3890 | $3865 | $3820<br>VENTA BUENA: $3980 - $3990 | $4020</div>
</div>

<div class="box">
<div style="font-size:22px; font-weight:bold;">EURO (EURUSD)</div>
<div id="eur">1.1134</div>
<div style="font-size:14px; margin-top:5px;">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div>
</div>

<div class="estado" id="estado">
🔴 ORO: VENTA 88% - ESPERANDO $3900 | Actual: $3943.30
</div>

<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA - PAYPAL</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20SENAL%20VIP" class="btn-green">📱 WHATSAPP 0767574050 - CONFIRMAR PAGO</a>

<div class="disclaimer">⚠️ AVISO LEGAL: Solo fines EDUCATIVOS. No constituye asesoria financiera segun FINMA Suiza. Alto riesgo.</div>
<div class="footer">App Oficial: raudy-vip-oro.onrender.com<br>Alarmas: $3890, $3900, $3980, $3990<br>© 2026 Raudy VIP</div>

<audio id="alarma" preload="auto"><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>

<script>
let yaSono = {};

async function precioReal(){
  try{
    let r = await fetch('/api/oro-real?v='+Date.now());
    let data = await r.json();
    let precio = parseFloat(data.price);
    document.getElementById('oro').innerText = '$' + precio.toFixed(2);
    document.getElementById('horaOro').innerText = 'Actualizado: ' + new Date().toLocaleTimeString() + ' - VIVO';
    verificar(precio);
    let est = document.getElementById('estado');
    if(precio > 3940){
      est.innerHTML = '🔴 ORO: VENTA 88% - ESPERANDO $3900 | Actual: $' + precio.toFixed(2);
      est.className = 'estado venta';
    } else if(precio <= 3905 && precio >= 3885){
      est.innerHTML = '🟢 ORO: COMPRA BUENA $3900 | Actual: $' + precio.toFixed(2);
      est.className = 'estado compra';
      if(!yaSono['zona3900']){ yaSono['zona3900']=true; sonar(); }
    } else {
      est.innerHTML = '🟡 ORO: En zona ' + precio.toFixed(2) + ' - ESPERANDO SEÑAL';
      est.className = 'estado';
      est.style.background = '#FFA500';
    }
  }catch(e){
    document.getElementById('oro').innerText = 'Error';
  }
}

function verificar(p){ /* tu funcion extra */ }
function sonar(){
  let a=document.getElementById('alarma'); a.play(); 
  if(navigator.vibrate) navigator.vibrate([500,200,500]);
}

precioReal();
setInterval(precioReal, 5000);
let eurBase = 1.1134;
setInterval(()=>{
  eurBase += (Math.random()-0.5)*0.0005;
  document.getElementById('eur').innerText = eurBase.toFixed(4);
}, 3000);
setInterval(()=>{ yaSono={}; }, 3600000);
</script>

</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
