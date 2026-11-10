# ============================================================
# MAQUINA CAMBIA MONEDA - RAUDY VIP - CASA DE CAMBIO
# Jefe: Raudy Manzueta
# ============================================================
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# TUS TASAS DE HOY - TU LA CAMBIAS AQUI JEFE
TASAS = {
    "USD_COMPRA": 60.50,  # Tu compras el dolar a esto
    "USD_VENTA": 62.00,   # Tu vendes el dolar a esto
    "EUR_COMPRA": 65.00,
    "EUR_VENTA": 67.50,
}

HTML = """
<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MAQUINA CAMBIA MONEDA - RAUDY VIP</title>
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;padding:12px;text-align:center}
.card{background:#1a1a1a;border:3px solid #FFD700;border-radius:20px;padding:16px;margin:10px 0}
.btn{background:#FFD700;color:#000;padding:15px 20px;border-radius:12px;font-weight:900;border:none;font-size:18px;width:100%;margin:8px 0}
.btn2{background:#00ff88;color:#000;padding:12px;border-radius:10px;font-weight:900;border:none;font-size:16px;width:48%}
input,select{width:100%;padding:14px;font-size:20px;border-radius:10px;border:2px solid #FFD700;background:#222;color:#fff;text-align:center;margin:8px 0}
.grande{font-size:32px;color:#00ff88;font-weight:900}
.tasa{background:#222;padding:10px;border-radius:10px;margin:5px}
</style></head>
<body>
<h1>💱 MAQUINA CAMBIA MONEDA</h1><h2 style="color:#FFD700">👑 RAUDY VIP - CASA DE CAMBIO</h2>
<p>📍 República Dominicana | Hoy: {{ fecha }}</p>

<div class="card">
<h3>📊 TASA DE HOY</h3>
<div class="tasa">💵 DÓLAR COMPRA: <b style="color:#00ff88">RD$ {{ usd_compra }}</b> | VENTA: <b style="color:#ff4444">RD$ {{ usd_venta }}</b></div>
<div class="tasa">💶 EURO COMPRA: <b style="color:#00ff88">RD$ {{ eur_compra }}</b> | VENTA: <b style="color:#ff4444">RD$ {{ eur_venta }}</b></div>
<p><small>Tu ganancia por cada $100: RD$ {{ ganancia_100 }}</small></p>
</div>

<div class="card">
<h3>🧮 CALCULADORA - EL CLIENTE PONE AQUÍ</h3>
<label>¿QUÉ QUIERE CAMBIAR EL CLIENTE?</label>
<select id="tipo">
<option value="USD_A_DOP">💵 Dólar a Peso - Cliente trae Dólar</option>
<option value="DOP_A_USD">🇩🇴 Peso a Dólar - Cliente trae Peso</option>
<option value="EUR_A_DOP">💶 Euro a Peso - Cliente trae Euro</option>
<option value="DOP_A_EUR">🇩🇴 Peso a Euro - Cliente trae Peso</option>
</select>
<label>¿CUÁNTO TRAE?</label>
<input type="number" id="monto" placeholder="Ej: 100" value="100" oninput="calcular()">
<h2>LE TOCA:</h2>
<div class="grande" id="resultado">RD$ 6,050.00</div>
<p id="detalle">Tasa: 60.50 | Tu ganancia: RD$ 150.00</p>
<button class="btn" onclick="hacerCambio()">✅ HACER CAMBIO + IMPRIMIR RECIBO</button>
<button class="btn" onclick="hablar()">🔊 ESCUCHAR CUÁNTO LE TOCA</button>
</div>

<div class="card" id="recibo" style="display:none">
<h3>🧾 RECIBO - RAUDY VIP</h3>
<p id="reciboTexto"></p>
<button class="btn2" onclick="window.print()">🖨️ IMPRIMIR</button>
<button class="btn2" onclick="document.getElementById('recibo').style.display='none'">CERRAR</button>
</div>

<div class="card">
<h3>💰 TU CAJA DE HOY</h3>
<p>Cambios hoy: <b id="conteo">0</b> | Ganancia hoy: <b id="gananciaHoy" style="color:#00ff88">RD$ 0</b></p>
<p><a href="https://paypal.me/RaudyManzueta/20" target="_blank" style="color:#FFD700">💳 MI PAYPAL</a> | <a href="https://t.me/raudy_vip_oro_bot" target="_blank" style="color:#FFD700">📩 MI TELEGRAM</a></p>
</div>

<script>
let cambios=0, gananciaTotal=0;
let tasas={usd_c:{{ usd_compra }}, usd_v:{{ usd_venta }}, eur_c:{{ eur_compra }}, eur_v:{{ eur_venta }}};
function calcular(){
 let tipo=document.getElementById('tipo').value;
 let monto=parseFloat(document.getElementById('monto').value)||0;
 let res=0, tasa=0, gan=0, texto="";
 if(tipo=="USD_A_DOP"){tasa=tasas.usd_c; res=monto*tasa; gan=monto*(tasas.usd_v-tasas.usd_c); texto="RD$ "+res.toLocaleString('en-US',{minimumFractionDigits:2});}
 if(tipo=="DOP_A_USD"){tasa=tasas.usd_v; res=monto/tasa; gan=monto*0.02; texto="US$ "+res.toFixed(2);}
 if(tipo=="EUR_A_DOP"){tasa=tasas.eur_c; res=monto*tasa; gan=monto*(tasas.eur_v-tasas.eur_c); texto="RD$ "+res.toLocaleString('en-US',{minimumFractionDigits:2});}
 if(tipo=="DOP_A_EUR"){tasa=tasas.eur_v; res=monto/tasa; gan=monto*0.02; texto="€ "+res.toFixed(2);}
 document.getElementById('resultado').innerText=texto;
 document.getElementById('detalle').innerText="Tasa: "+tasa+" | Tu ganancia en este cambio: RD$ "+gan.toFixed(2);
 return {res,gan,tipo,monto,tasa};
}
function hacerCambio(){
 let d=calcular();
 cambios++; gananciaTotal+=d.gan;
 document.getElementById('conteo').innerText=cambios;
 document.getElementById('gananciaHoy').innerText="RD$ "+gananciaTotal.toFixed(2);
 document.getElementById('recibo').style.display='block';
 document.getElementById('reciboTexto').innerHTML="Cliente cambió: "+d.monto+" ("+d.tipo+")<br>Le tocó: "+document.getElementById('resultado').innerText+"<br>Tasa: "+d.tasa+"<br>Gracias por cambiar con RAUDY VIP 👑<br>Fecha: "+new Date().toLocaleString('es-DO');
 hablar();
}
function hablar(){
 let t="Cliente, le tocan "+document.getElementById('resultado').innerText+". Gracias por cambiar con Raudy Vip.";
 let u=new SpeechSynthesisUtterance(t); u.lang='es-DO'; speechSynthesis.speak(u);
}
calcular();
</script>
</body></html>
"""

from datetime import datetime
@app.route('/')
def inicio():
    ganancia_100 = (TASAS["USD_VENTA"] - TASAS["USD_COMPRA"]) * 100
    return render_template_string(HTML, fecha=datetime.now().strftime("%d/%m/%Y %H:%M"), usd_compra=TASAS["USD_COMPRA"], usd_venta=TASAS["USD_VENTA"], eur_compra=TASAS["EUR_COMPRA"], eur_venta=TASAS["EUR_VENTA"], ganancia_100=f"{ganancia_100:.2f}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
