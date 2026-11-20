# JEFE BOT - 12 ROBOTS - RENDER OK
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "JEFE OK - 12 ROBOTS - 6 COMPRA 6 VENTA - H4 MANDA"

@app.route("/compra")
def compra():
    return "COMPRA JEFE - COMPRA"

@app.route("/venta")
def venta():
    return "VENTA JEFE - VENTA"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
