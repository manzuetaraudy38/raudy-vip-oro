from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY VIP - ORO Y EURO</title>
</head>
<body style="background:#111;color:white;text-align:center;font-family:Arial;padding:10px;">
<h1 style="color:yellow;">RAUDY VIP - ORO Y EURO</h1>
<h2>ORO: <span id="oro">3957.95</span> | EUR: <span id="eur">1.11</span></h2>
<h2 id="estado" style="background:red;padding:15px;border-radius:10px;">ORO: VENTA 88% - ESPERA</h2>
<div style="margin-top:20px;background:#222;padding:15px;border-radius:10px;">
<p>COMPRA BUENA: $3900 - $3890 | $3865 | $3820</p>
<p>VENTA BUENA: $3980 - $3990 | $4020</p>
</div>

<a href="https://wa.me/41767574050?text=Hola%20Raudy%20VIP%20quiero%20info%20del%20ORO" style="background:#25D366;color:white;padding:18px 35px;display:inline-block;margin:20px;border-radius:10px;text-decoration:none;font-size:22px;font-weight:bold;">WhatsApp 0767574050</a>
<br>
<a href="https://raudy-vip-oro.onrender.com/" style="background:yellow;color:black;padding:15px 30px;display:inline-block;text-decoration:none;font-size:18px;border-radius:10px;font-weight:bold;">MI APP RAUDY VIP</a>

<script>
let alarmasORO={compra:[3900,3890,3865,3820],venta:[3980,3990,4020]};
let alarmasEUR={compra:[1.109,1.108,1.105],venta:[1.115,1.118,1.121]};
let yaSono={};
function sonar(tipo,precio){
 let k=tipo+precio; if(yaSono[k])return; yaSono[k]=true;
 let a=new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg'); a.play();
 alert('🚨 RAUDY VIP - '+tipo+' $'+precio+'\\nApp: https://raudy-vip-oro.onrender.com/\\nWA: 0767574050');
 document.getElementById('estado').innerHTML = '🚨 '+tipo+' $'+precio+' - ENTRA YA';
 document.getElementById('estado').style.background = 'green';
}
function verificar(o,e){
 alarmasORO.compra.forEach(p=>{if(o<=p)sonar('COMPRA BUENA ORO',p)});
 alarmasORO.venta.forEach(p=>{if(o>=p)sonar('VENTA BUENA ORO',p)});
}
// Prueba - cambia el numero 3957 por 3890 para probar alarma
let precioSimulado = 3957.95;
setInterval(()=>{
  document.getElementById('oro').innerText = precioSimulado;
  verificar(precioSimulado, 1.11);
}, 3000);
</script>
</body>
</html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
