from flask import Flask, session, request, redirect, jsonify
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "RAUDY-ORO-PRO-2026-GINEBRA-RAUDY20"

# === CONFIGURACION ===
CLAVE_ADMIN = "RAUDY-ADMIN-100"  # TU CODIGO JEFE - NUNCA VENCE
CLAVE_CLIENTE = "RAUDY20"  # CODIGO CLIENTES - VENCE 30 DIAS
FECHA_VENCE = datetime(2026, 12, 3, 23, 59, 59)

def dias_restantes():
    delta = FECHA_VENCE - datetime.now()
    return max(0, delta.days)

def esta_logueado():
    vip = session.get("vip")
    if vip == CLAVE_ADMIN:
        return True
    if vip == CLAVE_CLIENTE and datetime.now() <= FECHA_VENCE:
        return True
    return False

def codigo_vigente():
    return True  # Siempre deja entrar al login, el control esta en esta_logueado

def get_price_yahoo(symbol, fallback):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        j = r.json()
        price = j['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except:
        return fallback

@app.route('/login', methods=['GET','POST'])
def login():
    error = ""
    if request.method == 'POST':
        clave = request.form.get("clave","").strip().upper()
        if clave == CLAVE_ADMIN or clave == CLAVE_CLIENTE:
            # Si es cliente, verifica fecha
            if clave == CLAVE_CLIENTE and datetime.now() > FECHA_VENCE:
                error = "⛔ CODIGO VENCIDO - PAGA DE NUEVO"
            else:
                session["vip"] = clave
                return redirect("/")
        else:
            error = "❌ CLAVE INCORRECTA - PAGA VIP PARA OBTENERLA"

    # Si cliente intenta entrar vencido
    vencido_msg = ""
    if datetime.now() > FECHA_VENCE:
        vencido_msg = f'<div style="background:red;color:white;padding:10px;border-radius:10px;font-weight:bold;margin-bottom:12px">⛔ RAUDY20 VENCIO EL {FECHA_VENCE.strftime("%d/%m/%Y")} - RENUEVA TU VIP</div>'

    return f'''
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY VIP</title>
<style>
body{{background:#0a0a0a;color:white;font-family:Arial;margin:0;padding:15px;text-align:center}}
.box{{border:2px solid #FFD700;border-radius:20px;padding:25px;background:#1a1a1a;max-width:400px;margin:40px auto}}
input{{width:90%;padding:18px;border-radius:12px;border:2px solid #FFD700;background:#0a0a0a;color:#FFD700;font-size:22px;text-align:center;font-weight:bold;margin:15px 0}}
.btn{{background:#FFD700;color:black;border-radius:15px;padding:18px;font-weight:bold;font-size:18px;width:100%;border:none;cursor:pointer}}
.btn-yellow{{background:#FFD700;color:black;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-blue{{background:#0a84ff;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:10px;display:block;text-decoration:none}}
.btn-green{{background:#25D366;color:white;border-radius:15px;padding:16px;text-align:center;font-weight:bold;font-size:17px;margin-bottom:12px;display:block;text-decoration:none}}
.warn{{border:1px solid #ff4444;background:#1a0a0a;border-radius:12px;padding:12px;font-size:10px;color:#ffaaaa;text-align:left;margin-top:15px;line-height:1.4}}
</style></head><body>
<div class="box">
<h1 style="color:#FFD700;">🔒 RAUDY ORO PRO VIP</h1>
{vencido_msg}
<p>App cerrada con candado - Solo VIP</p>
<form method="POST">
<input name="clave" placeholder="ESCRIBE TU CLAVE VIP" required>
<div style="color:#ff4444;font-weight:bold;margin:10px;">{error}</div>
<button class="btn">🔓 ENTRAR</button>
</form>
<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050</a>
<div class="warn"><b>⚠️ ADVERTENCIA DE RIESGO:</b> Solo educativo. No es consejo financiero. Trading Oro, Forex, Tesla, Apple es ALTO RIESGO. Puedes perder tu dinero.</div>
</div></body></html>'''

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
    return {"oro": oro, "gbp": get_price_yahoo('GBPUSD=X', 1.3412), "eur": get_price_yahoo('EURUSD=X', 1.1197), "tesla": get_price_yahoo('TSLA', 245.80), "apple": get_price_yahoo('AAPL', 185.30)}

@app.route('/')
def home():
    if not esta_logueado():
        return redirect("/login")
    vip = session.get("vip")
    dias = dias_restantes()
    tipo = "ADMIN JEFE" if vip == CLAVE_ADMIN else f"VIP - VENCE EN {dias} DIAS"
    return f'''
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY ORO PRO</title>
<script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
<style>
body {{ background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:10px; }}
.header {{ text-align:center; padding:15px; border:2px solid #FFD700; border-radius:15px; background:#1a1a1a; margin-bottom:12px; }}
.header h1 {{ margin:0; color:#FFD700; font-size:26px; }}
.box {{ border:2px solid #FFD700; border-radius:15px; padding:12px; text-align:center; margin-bottom:14px; background:#1a1a1a; }}
.precio {{ font-size:32px; color:#00ff00; font-weight:bold; }}
.zonas {{ font-size:11px; margin-top:6px; line-height:1.4; }}
.estado {{ border-radius:10px; padding:8px; font-weight:bold; font-size:13px; margin-top:8px; }}
.chart {{ width:100%; height:180px; margin-top:10px; border-radius:10px; background:#0f0f0f; }}
.btn-yellow {{ background:#FFD700; color:black; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }}
.btn-blue {{ background:#0a84ff; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }}
.btn-green {{ background:#25D366; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:12px; display:block; text-decoration:none; }}
.footer {{ text-align:center; font-size:10px; color:#666; padding:10px; }}
.warn-main {{ border:2px solid #ff4444; background:#1a0a0a; border-radius:15px; padding:12px; font-size:10px; color:#ffaaaa; line-height:1.4; text-align:left; margin-bottom:14px; }}
</style></head><body>
<div class="header">
<h1>🔥 RAUDY ORO PRO 🔥</h1>
<div style="font-size:11px; color:#00ff00;" id="hora">VIVO - {tipo}</div>
<div style="margin-top:5px;"><a href="/logout" style="color:#ff4444; font-size:11px; text-decoration:none;">SALIR</a></div>
</div>
<div class="warn-main"><b>⚠️ ADVERTENCIA DE RIESGO - SOLO EDUCATIVO - NO ES CONSEJO FINANCIERO</b><br>Trading Oro, Forex, Tesla, Apple es ALTO RIESGO. Puedes perder todo tu capital.</div>
<div class="box"><div style="font-weight:bold;">🟡 ORO (XAUUSD) - EN VIVO</div><div class="precio" id="oro">$3951.70</div><div class="zonas"><span style="color:#00ff00;">COMPRA BUENA: $3900 - $3890 | $3865</span><br><span style="color:#ff4444;">VENTA BUENA: $3980 - $3990 | $4020</span></div><div class="estado" id="estado-oro" style="background:#ff0000;">🔴 VENTA 88% - ESPERANDO $3900</div><div class="chart" id="chart-oro"></div></div>
<div class="box"><div style="font-weight:bold;">💷 GBPUSD - LIBRA</div><div class="precio" id="gbp">1.3412</div><div class="zonas"><span style="color:#00ff00;">COMPRA: 1.2620 - 1.2580</span> | <span style="color:#ff4444;">VENTA: 1.2750 - 1.2820</span></div><div class="estado" id="estado-gbp" style="background:#333;">ESPERANDO</div><div class="chart" id="chart-gbp"></div></div>
<div class="box"><div style="font-weight:bold;">💶 EURO (EURUSD)</div><div class="precio" id="eur">1.1197</div><div class="zonas">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div><div class="chart" id="chart-eur"></div></div>
<div class="box"><div style="font-weight:bold;">🚗 TESLA (TSLA)</div><div class="precio" id="tesla">$245.80</div><div class="zonas"><span style="color:#00ff00;">COMPRA: $240 - $235 - $228</span><br><span style="color:#ff4444;">VENTA: $275 - $285 - $295</span></div><div class="estado" id="estado-tesla" style="background:#333;">ESPERANDO</div><div class="chart" id="chart-tesla"></div></div>
<div class="box"><div style="font-weight:bold;">🍎 APPLE (AAPL)</div><div class="precio" id="apple">$185.30</div><div class="zonas"><span style="color:#00ff00;">COMPRA: $172 - $168 - $165</span><br><span style="color:#ff4444;">VENTA: $195 - $200 - $205</span></div><div class="estado" id="estado-apple" style="background:#333;">ESPERANDO</div><div class="chart" id="chart-apple"></div></div>
<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA - PAYPAL</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 PAGAR VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050 - CONFIRMAR PAGO</a>
<div class="footer">App: RAUDY ORO PRO | raudy-vip-oro.onrender.com<br>© 2026 Ginebra Suiza - Velas en vivo - Solo Educativo</div>
<script>
function makeCandleChart(elemId){{ const chart = LightweightCharts.createChart(document.getElementById(elemId), {{ layout: {{ background: {{ color: '#0f0f0f' }}, textColor: '#888' }}, grid: {{ vertLines: {{ color: '#222' }}, horzLines: {{ color: '#222' }} }}, width: document.getElementById(elemId).clientWidth, height: 180, timeScale: {{ timeVisible: true, secondsVisible: true }} }}); const series = chart.addCandlestickSeries({{ upColor: '#00ff00', downColor: '#ff4444', borderVisible: false, wickUpColor: '#00ff00', wickDownColor: '#ff4444' }}); return {{ chart, series, data: [] }}; }}
let charts = {{ oro: makeCandleChart('chart-oro'), gbp: makeCandleChart('chart-gbp'), eur: makeCandleChart('chart-eur'), tesla: makeCandleChart('chart-tesla'), apple: makeCandleChart('chart-apple') }};
function addCandle(cObj, price){{ let now = Math.floor(Date.now() / 1000); let last = cObj.data[cObj.data.length - 1]; if(!last || (now - last.time) >= 15){{ let candle = {{ time: now, open: last ? last.close : price, high: price, low: price, close: price }}; cObj.data.push(candle); if(cObj.data.length > 60) cObj.data.shift(); }} else {{ last.high = Math.max(last.high, price); last.low = Math.min(last.low, price); last.close = price; }} cObj.series.setData(cObj.data); }}
async function actualizar(){{ try{{ let r = await fetch('/api/precios?v=' + Date.now()); if(r.status==401){{ window.location='/login'; return; }} let d = await r.json(); document.getElementById('oro').innerText = '$' + d.oro.toFixed(2); document.getElementById('gbp').innerText = d.gbp.toFixed(4); document.getElementById('eur').innerText = d.eur.toFixed(4); document.getElementById('tesla').innerText = '$' + d.tesla.toFixed(2); document.getElementById('apple').innerText = '$' + d.apple.toFixed(2); addCandle(charts.oro, d.oro); addCandle(charts.gbp, d.gbp); addCandle(charts.eur, d.eur); addCandle(charts.tesla, d.tesla); addCandle(charts.apple, d.apple); let eo = document.getElementById('estado-oro'); if(d.oro > 3940){{ eo.innerHTML = '🔴 VENTA 88% - ESPERANDO $3900'; eo.style.background = '#ff0000'; }} else if(d.oro <= 3905 && d.oro >= 3885){{ eo.innerHTML = '🟢 COMPRA BUENA $3900'; eo.style.background = '#00aa00'; }} else {{ eo.innerHTML = '🟡 En zona ' + d.oro.toFixed(2); eo.style.background = '#FFA500'; }} }}catch(e){{}} }}
setInterval(actualizar, 5000); actualizar();
</script></body></html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
