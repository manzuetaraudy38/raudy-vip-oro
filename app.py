# app.py - RAUDY VIP 1000
import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# LLAVES - NUNCA SE ESCRIBEN AQUÍ, SOLO EN RENDER
BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")
USAR_TESTNET = os.getenv("USAR_TESTNET", "True") == "True"

# TUS ACTIVOS
ACTIVOS = ["ORO", "EUR/USD", "GBP/USD", "USD/CHF", "TESLA", "APPLE", "META", "SP500"]

# CEREBRO 1000 ROBOTS - VOTACIÓN
def cerebro_1000(precio, tp, sl):
    votos_compra = 0
    votos_venta = 0
    # Aquí votan 1000 mini-robots
    # Ejemplo simple: si precio cerca de SL, votan venta. Si cerca de TP, votan compra
    for i in range(1000):
        if precio < tp:
            votos_compra += 1
        else:
            votos_venta += 1
    if votos_compra > 700:
        return "COMPRAR"
    if votos_venta > 700:
        return "VENDER"
    return "ESPERA"

HTML = """
<h1>RAUDY VIP 1000 👑</h1>
<p>Precio Oro: <b id="precio">3980</b></p>
<label>TP: <input id="tp" value="4000"></label><br>
<label>SL: <input id="sl" value="3950"></label><br><br>
<button onclick="operar('COMPRAR')" style="background:green;color:white;padding:15px;">COMPRAR</button>
<button onclick="operar('VENDER')" style="background:red;color:white;padding:15px;">VENDER</button>
<br><br>
<a href="https://t.me/TU_TELEGRAM"><button>TELEGRAM</button></a>
<a href="https://wa.me/TU_WHATSAPP"><button>WHATSAPP</button></a>
<br><br>
<a href="https://payhip.com/TU_LINK_DE_PAGO"><button>PAGAR PARA USAR MI ROBOT - $29/mes</button></a>
<script>
function hablar(texto){
  let voz = new SpeechSynthesisUtterance(texto);
  voz.lang = 'es-DO';
  speechSynthesis.speak(voz);
}
function operar(tipo){
  let precio = document.getElementById('precio').innerText;
  hablar('Jefe, esta en ' + precio + ', voy a ' + tipo);
  fetch('/operar', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({tipo:tipo})});
}
setInterval(()=>{
  let precio = 3970 + Math.floor(Math.random()*20);
  document.getElementById('precio').innerText = precio;
  if(precio <= 3970){ hablar('Jefe, esta en ' + precio + ', bajo'); }
  if(precio >= 3980){ hablar('Jefe, esta en ' + precio + ', subio'); }
}, 10000);
</script>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/operar", methods=["POST"])
def operar():
    data = request.get_json()
    decision = cerebro_1000(3980, 4000, 3950)
    return jsonify({"ok": True, "decision": decision, "pedido": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
