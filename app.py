from flask import Flask, session, request, redirect, jsonify
import requests

app = Flask(__name__)
app.secret_key = "RAUDY-ORO-PRO-2026-GINEBRA-RAUDY20"

# LA BUENA - SOLO UNA CLAVE
CLAVE_BUENA = "RAUDY20"

def get_price_yahoo(symbol, fallback):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        j = r.json()
        price = j['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except:
        return fallback

def esta_logueado():
    return session.get("vip") == CLAVE_BUENA

@app.route('/login', methods=['GET','POST'])
def login():
    error = ""
    if request.method == 'POST':
        clave = request.form.get("clave","").strip().upper()
        if clave == CLAVE_BUENA:
            session["vip"] = CLAVE_BUENA
            return redirect("/")
        error = "❌ CLAVE MALA - LA BUENA ES RAUDY20"
    return f'''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY ORO PRO - VIP</title>
<style>
body{{background:#0a0a0a;color:white;font-family:Arial;margin:0;padding:15px;text-align:center}}
.box{{border:2px solid #FFD700;border-radius:20px;padding:25px;background:#1a1a1a;max-width:400px;margin:40px auto}}
input{{width:90%;padding:18px;border-radius:12px;border:2px solid #FFD700;background:#0a0a0a;color:#FFD700;font-size:22px;text-align:center;font-weight:bold;margin:15px 0}}
.btn{{background:#FFD700;color:black;border-radius:15px;padding:18px;font-weight:bold;font-size:18px;width:100%;border:none;cursor:pointer}}
.btn-yellow{{background:#FFD700;color:black;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-blue{{background:#0a84ff;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-green{{background:#25D366;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:12px;display:block;text-decoration:none}}
.warn{{border:1px solid #ff4444;background:#1a0a0a;border-radius:12px;padding:12px;font-size:10px;color:#ffaaaa;text-align:left;margin-top:15px;line-height:1.4}}
</style>
</head>
<body>
<div class="box">
<h1 style="color:#FFD700;">🔒 RAUDY ORO PRO VIP</h1>
<p>App cerrada con candado</p>
<p style="color:#00ff00;font-weight:bold;">CLAVE BUENA: RAUDY20</p>
<form method="POST">
<input name="clave" placeholder="ESCRIBE RAUDY20" required>
<div style="color:#ff4444;font-weight:bold;margin:10px;">{error}</div>
<button class="btn">🔓 ENTRAR CON RAUDY20</button>
</form>
<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050</a>
<div class="warn">
<b>⚠️ ADVERTENCIA DE RIESGO - AVISO LEGAL EDUCATIVO:</b><br>
Esta App RAUDY ORO PRO es SOLO CON FINES EDUCATIVOS. No es consejo financiero, no es asesoría de inversión. Trading de Oro, Forex, Tesla, Apple contiene ALTO RIESGO y puedes perder todo tu dinero. Resultados pasados no garantizan futuros. Opera bajo tu propio riesgo. Raudy Manzueta no es asesor financiero regulado.
</div>
</div>
</body>
</html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route('/api/precios')
def precios():
    if not esta_logueado():
        return jsonify({"error": "no autorizado"}), 401
    oro = 3951.50
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=4)
        oro = r.json().get('price', oro)
    except:
        oro = get_price_yahoo('GC=F', oro)
    return {
        "oro": oro,
        "gbp": get_price_yahoo('GBPUSD=X', 1.3412),
        "eur": get_price_yahoo('EURUSD=X', 1.1197),
        "tesla": get_price_yahoo('TSLA', 245.80),
        "apple": get_price_yahoo('AAPL', 185.30)
    }

@app.route('/')
def home():
    if not esta_logueado():
        return redirect("/login")
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY ORO PRO</title>
<script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
<style>
body { background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:10px; }
.header { text-align:center; padding:15px; border:2px solid #FFD700; border-radius:15px; background:#1a1a1a; margin-bottom:12px; }
.header h1 { margin:0; color:#FFD700; font-size:26px; }
.box { border:2px solid #FFD700; border-radius:15px; padding:12px; text-align:center; margin-bottom:14px; background:#1a1a1a; }
.precio { font-size:32px; color:#00ff00; font-weight:bold; }
.zonas { font-size:11px; margin-top:6px; line-height:1.4; }
.estado { border-radius:10px; padding:8px; font-weight:bold; font-size:13px; margin-top:8px; }
.chart { width:100%; height:180px; margin-top:10px; border-radius:10px; background:#0f0f0f; }
.btn-yellow { background:#FFD700; color:black; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }
.btn-blue { background:#0a84ff; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }
.btn-green { background:#25D366; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:12px; display:block; text-decoration:none; }
.footer { text-align:center; font-size:10px; color:#666; padding:10px; }
.warn-main { border:2px solid #ff4444; background:#1a0a0a; border-radius:15px; padding:12px; font-size:10px; color:#ffaaaa; line-height:1.4; text-align:left; margin-bottom:14px; }
.warn-title { color:#ff4444; font-weight:bold; font-size:11px; text-align:center; margin-bottom:6px; }
</style>
</head>
<body>

<div class="header">
<h1>🔥 RAUDY ORO PRO 🔥</h1>
<div style="font-size:11px; color:#aaa;">APP OFICIAL - VELAS JAPONESAS EN VIVO</div>
<div style="font-size:11px; color:#00ff00;" id="hora">VIVO - RAUDY ORO PRO - VIP ✅ RAUDY20</div>
<div style="margin-top:5px;"><a href="/logout" style="color:#ff4444; font-size:11px; text-decoration:none;">SALIR</a></div>
</div>

<div class="warn-main">
<div class="warn-title">⚠️ ADVERTENCIA DE RIESGO - SOLO EDUCATIVO - NO ES CONSEJO FINANCIERO</div>
<b>RAUDY ORO PRO NO ES CONSEJO FINANCIERO.</b> Contenido solo educativo e informativo. Trading Oro (XAUUSD), Divisas (GBPUSD, EURUSD), Acciones (TSLA, AAPL) implica ALTO RIESGO de pérdida total. Puedes perder todo tu capital. No garantizamos ganancias. No somos asesores regulados. Opera bajo tu propia responsabilidad. Consulta con profesional autorizado.
</div>

<div class="box">
<div style="font-weight:bold;">🟡 ORO (XAUUSD) - EN VIVO</div>
<div class="precio" id="oro">$3951.70</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA BUENA: $3900 - $3890 | $3865</span><br><span style="color:#ff4444;">VENTA BUENA: $3980 - $3990 | $4020</span></div>
<div class="estado" id="estado-oro" style="background:#ff0000;">🔴 VENTA 88% - ESPERANDO $3900</div>
<div class="chart" id="chart-oro"></div>
</div>

<div class="box">
<div style="font-weight:bold;">💷 GBPUSD - LIBRA</div>
<div class="precio" id="gbp">1.3412</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA: 1.2620 - 1.2580</span> | <span style="color:#ff4444;">VENTA: 1.2750 - 1.2820</span></div>
<div class="estado" id="estado-gbp" style="background:#333;">ESPERANDO</div>
<div class="chart" id="chart-gbp"></div>
</div>

<div class="box">
<div style="font-weight:bold;">💶 EURO (EURUSD)</div>
<div class="precio" id="eur">1.1197</div>
<div class="zonas">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div>
<div class="chart" id="chart-eur"></div>
</div>

<div class="box">
<div style="font-weight:bold;">🚗 TESLA (TSLA)</div>
<div class="precio" id="tesla">$245.80</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA: $240 - $235 - $228</span><br><span style="color:#ff4444;">VENTA: $275 - $285 - $295</span></div>
<div class="estado" id="estado-tesla" style="background:#333;">ESPERANDO</div>
<div class="chart" id="chart-tesla"></div>
</div>

<div class="box">
<div style="font-weight:bold;">🍎 APPLE (AAPL)</div>
<div class="precio" id="apple">$185.30</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA: $172 - $168 - $165</span><br><span style="color:#ff4444;">VENTA: $195 - $200 - $205</span></div>
<div class="estado" id="estado-apple" style="background:#333;">ESPERANDO</div>
<div class="chart" id="chart-apple"></div>
</div>

<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA - PAYPAL</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050 - CONFIRMAR PAGO</a>

<div class="footer">App: RAUDY ORO PRO | raudy-vip-oro.onrender.com<br>© 2026 Ginebra Suiza - Velas en vivo - CLAVE RAUDY20 - Solo Educativo</div>

<script>
function makeCandleChart(elemId){
  const chart = LightweightCharts.createChart(document.getElementById(elemId), {
    layout: { background: { color: '#0f0f0f' }, textColor: '#888' },
    grid
