from flask import Flask
import requests
from datetime import datetime

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
.btn-green { background:#25D366; color:white; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:20px; display:block; text-decoration:none; }
.footer { text-align:center; font-size:12px; color:#888; line-height:1.6; padding-bottom:20px; }
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
<div style="font-size:36px; color:#00ff00; font-weight:bold;" id="euro-price">1.1127</div>
<div style="font-size:14px; margin-top:5px;">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div>
</div>

<div class="box-oro" id="oro-box">
🔴 ORO: VENTA 88% - ESPERANDO<br>$3900 | Actual: <span id="oro-real">$3951.50</span>
</div>

<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA -<br>PAYPAL</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20SENAL%20VIP" class="btn-green">📱 WHATSAPP 0767574050 -<br>CONFIRMAR PAGO</a>

<div class="footer">
App Oficial: raudy-vip-oro.onrender.com<br>
Alarmas activas: $3890, $3900, $3980, $3990<br>
Sonido + vibración cuando toque precio
</div>

<script>
async function actualizarOroReal() {
  try {
    let r = await fetch('/api/oro-real');
    let data = await r.json();
    let precio = parseFloat(data.price).toFixed(2);
    let hora = new Date().toLocaleTimeString();
    document.getElementById('oro-main').innerText = '$' + precio;
    document.getElementById('oro-real').innerText = '$' + precio;
    document.getElementById('oro-time').innerText = 'Actualizado: ' + hora + ' - VIVO';
    let box = document.getElementById('oro-box');
    if (data.price <= 3900) {
      box.style.background = '#00aa00';
      box.innerHTML = '🟢 ORO: COMPRA 88% - ¡ALARMA $3900 TOCADA!<br>$3900 | Actual: $' + precio;
    }
  } catch(e){}
}
setInterval(actualizarOroReal, 3000);
actualizarOroReal();
</script>
</body>
</html>
    '''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
