from flask import Flask
import os
app = Flask(__name__)

HTML = open("index.html").read() if os.path.exists("index.html") else "<h1>RAUDY VIP ORO</h1>"

@app.route("/")
def home():
    return """<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>RAUDY VIP ORO - DOBLE ROBOT</title><style>body{background:#000;color:#fff;font-family:Arial;text-align:center}h1{color:#FFD700;font-size:32px}.box{border:2px solid #FFD700;border-radius:20px;padding:20px;margin:15px;display:inline-block;width:300px}button{background:#FFD700;border:none;padding:15px 25px;font-size:18px;border-radius:10px;font-weight:bold;margin:5px}</style></head><body><h1>👑 RAUDY VIP ORO</h1><h2 style='color:#00FF00'>● EN VIVO - DOBLE ROBOT</h2><div class='box'><div style='font-size:50px'>🤖</div><h2>ROBOT 1 - ORO</h2><p id='r1'>Pulsa GENERAR</p><button onclick="document.getElementById('r1').innerHTML='🟢 COMPRA - ORO SUBE '+Math.floor(Math.random()*100)+'%'">GENERAR R1</button></div><div class='box' style='border-color:#00FF00'><div style='font-size:50px'>🤖</div><h2>ROBOT 2 - VERDE</h2><p id='r2'>Pulsa GENERAR</p><button onclick="document.getElementById('r2').innerHTML='🟢 COMPRA - VERDE SUBE '+Math.floor(Math.random()*100)+'%'">GENERAR R2</button></div><p>Tienda Raudy VIP prendida!</p></body></html>"""

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
