from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RAUDY VIP PRECIO REAL</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center}
h1{color:#FFD700}
.box{border:3px solid #FFD700;border-radius:20px;padding:15px;margin:10px;display:inline-block;width:280px}
.vela{width:50px;height:110px;margin:10px auto;border-radius:10px;background:#333;border:2px solid #fff}
.verde{background:#00FF00;box-shadow:0 0 30px #00FF00}
.roja{background:#FF0000;box-shadow:0 0 30px #FF0000}
button{background:#FFD700;border:none;padding:15px 25px;font-size:18px;border-radius:10px;font-weight:bold}
.precio{font-size:32px;color:#FFD700;font-weight:bold}
#final{font-size:30px;font-weight:bold;padding:20px;border-radius:20px;margin:15px}
.real{color:#00FFFF;font-size:14px}
</style>
</head>
<body>
<h1>👑 RAUDY VIP ROBOT PRO</h1>
<h3 style='color:#00FF00'>● EN VIVO - PRECIO REAL DEL MERCADO - XAU/USD</h3>
<p>Precio Real Oro: <span class='precio' id='precio'>Cargando...</span></p>
<p class='real' id='hora'>Precio real del mercado mundial</p>
<div id='final'>Esperando...</div>
<div class='box'>
<h2>5 MINUTO</h2>
<div class='vela' id='vela5'></div>
<h2 id='t5'>...</h2>
<p id='d5'>...</p>
</div>
<div class='box'>
<h2>15 MINUTO</h2>
<div class='vela' id='vela15'></div>
<h2 id='t15'>...</h2>
<p id='d15'>...</p>
</div>
<div class='box'>
<h2>1 HORA</h2>
<div class='vela' id='vela1h'></div>
<h2 id='t1h'>...</h2>
<p id='d1h'>...</p>
</div>
<div class='box' style
