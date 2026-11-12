from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "RAUDY VIP ORO - Robot DEMO funcionando"

if __name__ == "__main__":
    app.run()
