# ============================================================
# MAQUINA CAMBIA MONEDA - RAUDY VIP - GINEBRA, SUIZA
# Jefe: Raudy Manzueta - Vive en Suiza
# ============================================================
import os
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# TUS TASAS EN SUIZA - TU LAS CAMBIAS AQUI
# Ejemplo real de Ginebra: 1 Euro = 0.94 Francos aprox
TASAS = {
    "EUR_COMPRA": 0.92,  # Tu compras Euro a 0.92 CHF
    "EUR_VENTA": 0.96,   # Tu vendes Euro a 0.96 CHF
    "USD_COMPRA": 0.88,  # Tu compras Dólar a 0.88 CHF
    "USD_VENTA": 0.92,   # Tu vendes Dólar a 0.92 CHF
}

HTML = """
<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MAQUINA CAMBIA MONEDA - RAUDY VIP SUIZA</title>
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
<h1>💱 MAQUINA CAMBIA MONEDA</h1><h2 style="color:#FFD700">👑 RAUDY VIP - GINEBRA, SUIZA 🇨🇭</h2>
<p>📍 Ginebra | Hoy: {{ fecha }}</p>

<div class="card">
<h3>📊 TASA DE HOY EN GINEBRA</h3>
<div class="tasa">💶 EURO COMPRA: <b style="color:#00ff88">{{ eur_compra }} CHF</b> | VENTA: <b style="color:#ff4444">{{ eur_venta }} CHF</b></div>
<div class="tasa">💵 DÓLAR COMPRA: <b style="color:#00ff88">{{ usd_compra }} CHF</b> | VENTA: <b style="color:#ff4444">{{ usd_venta }} CHF</b></div>
<p><small>Tu ganancia por cada €100: {{ ganancia_100 }} CHF</small></p>
</div>

<div class="card">
<h3>🧮 CALCULADORA - CLIENTE EN SUIZA</h3>
<label>¿QUÉ QUIERE CAMBIAR EL CLIENTE?</label>
<select id="tipo">
<option value="EUR_A_CHF">💶 Euro a Franco - Cliente trae Euro (Va a Francia)</option>
<option value="CHF_A_EUR">🇨🇭 Franco a Euro - Cliente trae Franco (Viene de Francia)</option>
<option value="USD_A_CHF">💵 Dólar a Franco - Turista trae Dólar</option>
<option value="CHF_A_USD">🇨🇭 Franco a Dólar - Cliente trae Franco</option>
</select>
<label>¿CUÁNTO TRAE?</label>
<input type="number" id="monto" placeholder="Ej: 100" value="100" oninput="calcular()">
<h2>LE TOCA:</h2>
<div class="grande" id="resultado">92.00 CHF</div>
<p id="detalle">Tasa: 0.92 | Tu ganancia: 4.00 CHF</p>
<button class="btn" onclick="hacerCambio()">✅ HACER CAMBIO + RECIBO</button>
<button class="btn" onclick="hablar()">🔊 ESCUCHAR CUÁNTO LE TOCA</button>
</div>

<div class="card" id="recibo" style="display:none">
<h3>🧾 RECIBO - RAUDY VIP GINEBRA</h3>
<p id="reciboTexto"></p>
<button class="btn2" onclick="window.print()">🖨️ IMPRIMIR</button>
<button class="btn2" onclick="document.getElementById('recibo').style.display='none'">CERRAR</button>
</div>

<div class="card">
<h3>💰 TU CAJA DE HOY EN SUIZA</h3>
<p>Cambios hoy: <b id="conteo">0</b> | Ganancia hoy: <b id="gananciaHoy" style="color:#00ff88">0 CHF</b></p>
<p><small>💡 En Suiza puedes cobrar por TWINT, PayPal o Efectivo</small></p>
<p><a href="https://paypal.me/RaudyManzueta/20" target="_blank" style="color:#FFD700">💳 MI PAYPAL</a> | <a href="https://t.me/raudy_vip_oro_bot" target="_blank" style="color:#FFD700">📩 MI TELEGRAM</a></p>
</div>

<script>
let cambios=0, gananciaTotal=0;
let tasas={eur_c:{{ eur_compra }}, eur_v:{{ eur_venta }}, usd_c:{{ usd_compra }}, usd_v:{{ usd_venta }}};
function calcular(){
 let tipo=document.getElementById('tipo').value;
 let monto=parseFloat(document.getElementById('monto').value)||0;
 let res=0, tasa=0, gan=0, texto="";
 if(tipo=="EUR_A_CHF"){tasa=tasas.eur_c; res=monto*tasa; gan=monto*(tasas.eur_v-tasas.eur_c); texto=res.toFixed(2)+" CHF";}
 if(tipo=="CHF_A_EUR"){tasa=tasas.eur_v; res=monto/tasa; gan=monto*0.04; texto=res.toFixed(2)+" €";}
 if(tipo=="USD_A_CHF"){tasa=tasas.usd_c; res=monto*tasa; gan=monto*(tasas.usd_v-tasas.usd_c); texto=res.toFixed(2)+" CHF";}
 if(tipo=="CHF_A_USD"){tasa=tasas.usd_v; res=monto/tasa; gan=monto*0.04; texto=res.toFixed(2)+" US$";}
 document.getElementById('resultado').innerText=texto;
 document.getElementById('detalle').innerText="Tasa: "+tasa+" | Tu ganancia: "+gan.toFixed(2)+" CHF";
 return {res,gan,tipo,monto,tasa};
}
function hacerCambio(){
 let d=calcular();
 cambios++; gananciaTotal+=d.gan;
 document.getElementById('conteo').innerText=cambios;
 document.getElementById('gananciaHoy').innerText=gananciaTotal.toFixed(2)+" CHF";
 document.getElementById('recibo').style.display='block';
 document.getElementById('reciboTexto').innerHTML="Cliente cambió: "+d.monto+" ("+d.tipo+")<br>Le tocó: "+document.getElementById('resultado').innerText+"<br>Tasa: "+d.tasa+"<br>Gracias por cambiar con RAUDY VIP GINEBRA 👑🇨🇭<br>Fecha: "+new Date().toLocaleString('es-DO');
 hablar();
}
function hablar(){
 let t="Cliente, le tocan "+document.getElementById('resultado').innerText+". Gracias por cambiar con Raudy Vip Ginebra.";
 let u=new SpeechSynthesisUtterance(t); u.lang='es-DO'; speechSynthesis.speak(u);
}
calcular();
</script>
</body></html>
"""

@app.route('/')
def inicio():
    ganancia_100 = (TASAS["EUR_VENTA"] - TASAS["EUR_COMPRA"]) * 100
    return render_template_string(HTML, fecha=datetime.now().strftime("%d/%m/%Y %H:%M"), eur_compra=TASAS["EUR_COMPRA"], eur_venta=TASAS["EUR_VENTA"], usd_compra=TASAS["USD_COMPRA"], usd_venta=TASAS["USD_VENTA"], ganancia_100=f"{ganancia_100:.2f} CHF")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
