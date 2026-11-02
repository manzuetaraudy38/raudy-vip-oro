from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Raudy VIP ORO</title>
<style>
body { background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:15px; }
.box-euro { border:2px solid #FFD700; border-radius:15px; padding:15px; text-align:center; margin-bottom:15px; background:#1a1a1a; }
.box-oro { background:#ff0000; border-radius:15px; padding:15px; text-align:center; margin-bottom:15px; font-weight:bold; font-size:18px; }
.btn-yellow { background:#FFD700; color:black; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:19px; margin-bottom:12px; display:block; text-decoration:none; }
.btn-blue { background:#0a84ff; color:white; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:12px; display:block; text-decoration:none; }
.btn-green { background:#25D366; color:white; border-radius:15px; padding:18px; text-align:center; font-weight:bold; font-size:18px; margin-bottom:20px; display:block; text-decoration:none; }
.disclaimer { background:#111; border:1px solid #333; border-radius:10px; padding:12px; font-size:11px; color:#888; line-height:1.4; margin-bottom:15px; }
.footer { text-align:center; font-size:11px; color:#555; line-height:1.6; padding-bottom:20px; }
</style>
</head>
<body>

<div class="box-euro">
<div style="font-size:22px; font-weight:bold;">EURO (EURUSD)</div>
<div style="font-size:36px; color:#00ff00; font-weight:bold;">1.1130</div>
<div style="font-size:14px; margin-top:5px;">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div>
</div>

<div class="box-oro">
🔴 ORO: VENTA 88% - ESPERANDO<br>$3900 | Actual: $3943.30
</div>

<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">
💳 PAGAR VIP $20 AHORA -<br>PAYPAL
</a>

<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">
💎 PAGAR VIP $100 TODO EL MES
</a>

<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20SENAL%20VIP" class="btn-green">
📱 WHATSAPP 0767574050 -<br>CONFIRMAR PAGO
</a>

<div class="disclaimer">
⚠️ <b>AVISO LEGAL - DISCLAIMER:</b><br>
Este contenido es solo con fines EDUCATIVOS e INFORMATIVOS. No constituye asesoría financiera, de inversión o recomendación de compra/venta según FINMA Suiza.<br><br>
El trading de ORO (XAUUSD) y FOREX (EURUSD) implica ALTO RIESGO y puede resultar en pérdida total del capital. Resultados pasados no garantizan resultados futuros.<br><br>
Raudy VIP comparte su análisis personal. Cada usuario opera bajo su propia responsabilidad y riesgo. Consulta con un asesor financiero licenciado antes de invertir. Al pagar el acceso VIP aceptas estos términos.
</div>

<div class="footer">
App Oficial: raudy-vip-oro.onrender.com<br>
Alarmas activas: $3890, $3900, $3980, $3990<br>
Contacto: Ginebra, Suiza - 0767574050<br>
© 2026 Raudy VIP - Todos los derechos reservados
</div>

</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
