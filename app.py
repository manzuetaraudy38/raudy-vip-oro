from flask import Flask
import requests

app = Flask(__name__)

@app.route('/api/oro-real')
def oro_real():
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=5)
        data = r.json()
        return {"price": data.get('price', 3951.50)}
    except:
        return {"price": 3951.50}

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Raudy VIP ORO PRO REAL</title>
<style>
body { background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:12px; }
.box { border:2px solid #FFD700; border-radius:15px; padding:15px; text-align:center; margin-bottom:12px; background:#1a1a1a; }
.box-oro { background:#ff0000; border-radius:15px; padding:15px; text-align:center; margin-bottom:15px; font-weight:bold; font-size:18px; }
.btn-yellow { background:#FFD700; color:black; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:19px; margin-bottom:12px; display:block; text-decoration:none; }
.btn-blue { background:#0a84ff; color:white; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:12px; display:block; text-decoration:none; }
.btn-green { background:#25D366; color:white; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:12px; display:block; text-decoration:none; }
.btn-alarm { background:#333; color:#FFD700; border:1px solid #FFD700; border-radius:10px; padding:10px; text-align:center; font-size:13px; margin-bottom:15px; display:block; cursor:pointer; }
.disclaimer { background:#111; border:1px solid #333; border-radius:10px; padding:12px; font-size:11px; color:#888; line-height:1.4; margin-bottom:15px; }
.footer { text-align:center; font-size:11px; color:#555; line-height:1.6; padding-bottom:20px; }
</style>
</head>
<body>

<div class="box">
<div style="font-size:24px; font-weight:bold;">ORO (XAUUSD) - EN VIVO</div>
<div style="font-size:40px; color:#00ff00; font-weight:bold;" id="oro-main">$3951.50</div>
<div style="font-size:12px; color:#aaa;" id="oro-time">Actualizado: --:--:-- - VIVO</div>
<div style="font-size:14px; margin-top:8px;">COMPRA BUENA: $3900 - $3890 | $3865 | $3820<br>VENTA BUENA: $3980 - $3990 | $4020</div>
</div>

<div class="box">
<div style="font-size:22px; font-weight:bold;">EURO (EURUSD)</div>
<div style="font-size:36px; color:#00ff00; font-weight:bold;">1.1130</div>
<div style="font-size:14px; margin-top:5px;">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div>
</div>

<div class="box-oro" id="oro-box">
🔴 ORO: VENTA 88% - ESPERANDO<br>$3900 | Actual: <span id="oro-real">$3951.50</span>
</div>

<div class="btn-alarm" id="btn-activar" onclick="activarAlarma()">🔔 TOCA AQUI PARA ACTIVAR ALARMA SONORA $3900</div>

<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA -<br>PAYPAL</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20SENAL%20VIP" class="btn-green">📱 WHATSAPP 0767574050 -<br>CONFIRMAR PAGO</a>

<div class="disclaimer">⚠️ AVISO LEGAL - DISCLAIMER:<br>Este contenido es solo con fines EDUCATIVOS. No constituye asesoria financiera segun FINMA Suiza. El trading de ORO y FOREX implica ALTO RIESGO.</div>
<div class="footer">App Oficial: raudy-vip-oro.onrender.com<br>Alarmas: $3890, $3900, $3980, $3990 | Sonido + vibracion</div>

<audio id="alarma-audio" preload="auto"><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>

<script>
let alarmaActivada=false, yaSono=false;
function activarAlarma(){alarmaActivada=true; document.getElementById('btn-activar').innerText='✅ ALARMA ACTIVA - SONARA EN $3900'; document.getElementById('btn-activar').style.background='#00aa00'; if(Notification&&Notification.permission!=="granted")Notification.requestPermission(); let a=document.getElementById('alarma-audio'); a.play().then(()=>{a.pause();}).catch(()=>{}); if(navigator.vibrate)navigator.vibrate(200);}
function sonarAlarma(p){if(yaSono)return; yaSono=true; let a=document.getElementById('alarma-audio'); a.loop=true; a.play(); if(navigator.vibrate)navigator.vibrate([500,200,500,200,1000]); if(Notification&&Notification.permission==="granted"){new Notification("🔴 RAUDY VIP - ORO TOCO $3900!",{body:"Precio: $"+p+" - ¡COMPRA!"})} alert("🟢 ¡ALARMA RAUDY VIP! ORO TOCO $3900\\nActual: $"+p); }
async function actualizarOroReal(){try{let r=await fetch('/api/oro-real?v='+Date.now()); let d=await r.json(); let precio=parseFloat(d.price).toFixed(2); let hora=new Date().toLocaleTimeString(); document.getElementById('oro-main').innerText='$'+precio; document.getElementById('oro-real').innerText='$'+precio; document.getElementById('oro-time').innerText='Actualizado: '+hora+' - VIVO'; let box=document.getElementById('oro-box'); if(d.price<=3900){box.style.background='#00aa00'; box.innerHTML='🟢 ORO: COMPRA 88% - ¡ALARMA $3900 TOCADA!<br>$3900 | Actual: $'+precio; if(alarmaActivada)sonarAlarma(precio);} else {box.style.background='#ff0000'; box.innerHTML='🔴 ORO: VENTA 88% - ESPERANDO<br>$3900 | Actual: $'+precio; if(d.price>3905)yaSono=false;}}catch(e){}} setInterval(actualizarOroReal,3000); actualizarOroReal();
</script>
</body>
</html>
    '''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
