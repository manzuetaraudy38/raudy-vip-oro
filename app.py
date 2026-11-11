from flask import Flask, request, jsonify
app = Flask(__name__)

PRODUCTOS = [
    {"id": 1, "nombre": "Jabón Aclarante VIP Oro", "precio": 350, "img": "🧼"},
    {"id": 2, "nombre": "Crema Facial Oro", "precio": 650, "img": "🧴"},
    {"id": 3, "nombre": "Crema Corporal VIP", "precio": 750, "img": "✨"},
    {"id": 4, "nombre": "Combo Completo VIP Oro", "precio": 1500, "img": "👑"},
]

# --- CEREBRO DEL ROBOT ---
def robot_responde(mensaje):
    m = mensaje.lower()
    if "hola" in m or "buenas" in m or "hey" in m:
        return "👑 ¡Hola! Soy el Robot de RAUDY VIP ORO. ¿Qué quieres comprar hoy? Tenemos Jabón 🧼, Crema Facial 🧴 y Combo 👑. Escribe: jabon, crema o precio"
    if "jabon" in m:
        return "🧼 Jabón Aclarante VIP Oro - RD$ 350. Te deja la piel suave y clara. ¿Lo quieres? Escribe: quiero jabon"
    if "crema" in m and "facial" in m or m == "crema":
        return "🧴 Crema Facial Oro - RD$ 650. Para brillo y suavidad en la cara. ¿La quieres? Escribe: quiero crema"
    if "corporal" in m:
        return "✨ Crema Corporal VIP - RD$ 750. Para todo el cuerpo, huele rico. Escribe: quiero corporal"
    if "combo" in m:
        return "👑 Combo Completo - RD$ 1500. Jabón + Crema Facial + Crema Corporal. ¡Te ahorras RD$ 250! Escribe: quiero combo"
    if "precio" in m or "cuanto" in m or "costo" in m:
        return "💰 PRECIOS: Jabón RD$350 | Crema Facial RD$650 | Crema Corporal RD$750 | Combo RD$1500. ¿Cuál quieres?"
    if "envio" in m or "enviar" in m or "delivery" in m:
        return "🚚 Hacemos envíos a todo el país. El envío se paga aparte según tu ciudad. ¿De dónde eres?"
    if "quiero" in m:
        return f"✅ ¡Perfecto! Para pedir {mensaje}, dale al botón verde de WhatsApp abajo y te lo aparto de una vez. ¡Solo quedan pocos!"
    if "gracias" in m:
        return "👑 ¡Gracias a ti! RAUDY VIP ORO siempre a tu orden. ¿Quieres ver otro producto?"
    return "🤖 Entendí. Te puedo ayudar con: jabon, crema, combo, precio, envio. ¿Qué quieres ver?"

@app.route("/robot", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("mensaje", "")
    return jsonify({"respuesta": robot_responde(msg)})

@app.route("/")
def tienda():
    tarjetas = ""
    for p in PRODUCTOS:
        tarjetas += f"""
        <div style="background:#1a1a1a; border:2px solid gold; border-radius:15px; padding:20px; width:280px; text-align:center;">
            <div style="font-size:60px;">{p['img']}</div>
            <h3 style="color:gold;">{p['nombre']}</h3>
            <h2 style="color:#00ff88;">RD$ {p['precio']}</h2>
            <button onclick="pedir('{p['nombre']}')" style="background:gold; color:black; padding:12px 25px; border:none; border-radius:10px; font-size:18px; font-weight:bold;">COMPRAR</button>
        </div>
        """
    return f"""
    <html><head><title>RAUDY VIP ORO - Robot Vendedor</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="background:black; font-family:Arial; margin:0; padding:20px; padding-bottom:120px;">
        <div style="text-align:center;">
            <h1 style="color:gold;">👑 RAUDY VIP ORO 👑</h1>
            <p style="color:white;">🤖 Robot Vendedor 24/7 - Te atiende solo</p>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:20px; justify-content:center;">{tarjetas}</div>

        <!-- ROBOT -->
        <div id="chat" style="position:fixed; bottom:10px; left:10px; right:10px; background:white; border-radius:15px; padding:10px; box-shadow:0 0 20px gold;">
            <div id="mensajes" style="height:120px; overflow-y:auto; font-size:14px; margin-bottom:10px;">
                <p><b>🤖 Robot:</b> ¡Hola! Soy el robot de RAUDY. Pregúntame por jabon, crema, combo o precio</p>
            </div>
            <div style="display:flex; gap:5px;">
                <input id="input" placeholder="Escribe: quiero jabon..." style="flex:1; padding:12px; border-radius:10px; border:1px solid #ccc;">
                <button onclick="enviar()" style="background:gold; padding:12px 20px; border:none; border-radius:10px; font-weight:bold;">ENVIAR</button>
            </div>
        </div>
        <script>
        function pedir(p){{ window.open("https://wa.me/18090000000?text=" + encodeURIComponent("Hola Raudy quiero comprar: " + p), "_blank"); }}
        async function enviar(){{
            var inp = document.getElementById("input");
            var txt = inp.value; if(!txt) return;
            var caja = document.getElementById("mensajes");
            caja.innerHTML += "<p><b>Tú:</b> " + txt + "</p>";
            inp.value = "";
            var r = await fetch("/robot", {{method:"POST", headers:{{"Content-Type":"application/json"}}, body: JSON.stringify({{mensaje: txt}})}});
            var d = await r.json();
            caja.innerHTML += "<p><b>🤖 Robot:</b> " + d.respuesta + "</p>";
            caja.scrollTop = caja.scrollHeight;
        }}
        </script>
    </body></html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
