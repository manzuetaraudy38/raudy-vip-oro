from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def home():
    return """<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>RAUDY VIP ORO REAL</title><style>body{background:#000;color:#fff;font-family:Arial;text-align:center}h1{color:#FFD700}.box{border:3px solid #FFD700;border-radius:20px;padding:20px;margin:15px;display:inline-block;width:300px;vertical-align:top}.vela{width:60px;height:140px;margin:15px auto;border-radius:10px;background:#333;border:2px solid #fff}.verde{background:#00FF00;box-shadow:0 0 40px #00FF00}.roja{background:#FF0000;box-shadow:0 0 40px #FF0000}button{background:#FFD700;border:none;padding:15px 25px;font-size:18px;border-radius:10px;font-weight:bold}h2{font-size:22px}.precio{font-size:26px;color:#FFD700;font-weight:bold}</style></head><body><h1>👑 RAUDY VIP ORO</h1><h3 style='color:#00FF00'>● EN VIVO - VELA REAL ORO</h3><p>Precio Oro PAXG: <span class='precio' id='precio'>Cargando...</span></p><p id='hora'>...</p><div class='box'><div style='font-size:50px'>🤖</div><h2>ROBOT 1</h2><div class='vela' id='vela1'></div><h2 id='
