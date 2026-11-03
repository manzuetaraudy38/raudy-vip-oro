from flask import Flask
import requests

app = Flask(__name__)

def get_price_yahoo(symbol, fallback):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=5)
        j = r.json()
        price = j['chart']['result'][0]['meta']['regularMarketPrice']
        return float(price)
    except:
        return fallback

@app.route('/api/precios')
def precios():
    oro = 3951.50
    try:
        r = requests.get('https://api.gold-api.com/price/XAU', timeout=4)
        oro = r.json().get('price', oro)
    except:
        oro = get_price_yahoo('GC=F', oro)
    return {
        "oro": oro,
        "gbp": get_price_yahoo('GBPUSD=X', 1.2695),
        "eur": get_price_yahoo('EURUSD=X', 1.1134),
        "tesla": get_price_yahoo('TSLA', 245.80),
        "apple": get_price_yahoo('AAPL', 185.30)
    }

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAUDY ORO PRO</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { background:#0a0a0a; color:white; font-family: Arial; margin:0; padding:10px; }
.header { text-align:center; padding:15px; border:2px solid #FFD700; border-radius:15px; background:#1a1a1a; margin-bottom:12px; }
.header h1 { margin:0; color:#FFD700; font-size:26px; letter-spacing:1px; }
.box { border:2px solid #FFD700; border-radius:15px; padding:12px; text-align:center; margin-bottom:14px; background:#1a1a1a; }
.precio { font-size:32px; color:#00ff00; font-weight:bold; }
.zonas { font-size:11px; margin-top:6px; line-height:1.4; }
.estado { border-radius:10px; padding:8px; font-weight:bold; font-size:13px; margin-top:8px; }
canvas { background:#0f0f0f; border-radius:10px; margin-top:10px; width:100% !important; height:140px !important; }
.btn-yellow { background:#FFD700; color:black; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }
.btn-blue { background:#0a84ff; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:10px; display:block; text-decoration:none; }
.btn-green { background:#25D366; color:white; border-radius:15px; padding:16px; text-align:center; font-weight:bold; font-size:17px; margin-bottom:12px; display:block; text-decoration:none; }
.footer { text-align:center; font-size:10px; color:#666; padding:10px; }
</style>
</head>
<body>

<div class="header">
<h1>🔥 RAUDY ORO PRO 🔥</h1>
<div style="font-size:11px; color:#aaa;">APP OFICIAL CON GRAFICO EN VIVO</div>
<div style="font-size:11px; color:#00ff00;" id="hora">Actualizado: --:--:-- VIVO</div>
</div>

<div class="box">
<div style="font-weight:bold;">🟡 ORO (XAUUSD) - EN VIVO</div>
<div class="precio" id="oro">$3951.50</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA BUENA: $3900 - $3890 | $3865</span><br><span style="color:#ff4444;">VENTA BUENA: $3980 - $3990 | $4020</span></div>
<div class="estado" id="estado-oro" style="background:#ff0000;">🔴 VENTA 88% - ESPERANDO $3900</div>
<canvas id="chart-oro"></canvas>
</div>

<div class="box">
<div style="font-weight:bold;">💷 GBPUSD - LIBRA</div>
<div class="precio" id="gbp">1.2695</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA: 1.2620 - 1.2580</span> | <span style="color:#ff4444;">VENTA: 1.2750 - 1.2820</span></div>
<div class="estado" id="estado-gbp" style="background:#333;">ESPERANDO</div>
<canvas id="chart-gbp"></canvas>
</div>

<div class="box">
<div style="font-weight:bold;">💶 EURO (EURUSD)</div>
<div class="precio" id="eur">1.1134</div>
<div class="zonas">COMPRA: 1.109 - 1.108 | VENTA: 1.115 - 1.118</div>
<canvas id="chart-eur"></canvas>
</div>

<div class="box">
<div style="font-weight:bold;">🚗 TESLA (TSLA)</div>
<div class="precio" id="tesla">$245.80</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA: $240 - $235 - $228</span><br><span style="color:#ff4444;">VENTA: $275 - $285 - $295</span></div>
<div class="estado" id="estado-tesla" style="background:#333;">ESPERANDO</div>
<canvas id="chart-tesla"></canvas>
</div>

<div class="box">
<div style="font-weight:bold;">🍎 APPLE (AAPL)</div>
<div class="precio" id="apple">$185.30</div>
<div class="zonas"><span style="color:#00ff00;">COMPRA: $172 - $168 - $165</span><br><span style="color:#ff4444;">VENTA: $195 - $200 - $205</span></div>
<div class="estado" id="estado-apple" style="background:#333;">ESPERANDO</div>
<canvas id="chart-apple"></canvas>
</div>

<a href="https://www.paypal.me/RaudyManzueta/20" class="btn-yellow">💳 PAGAR VIP $20 AHORA</a>
<a href="https://www.paypal.me/RaudyManzueta/100" class="btn-blue">💎 VIP $100 TODO EL MES</a>
<a href="https://wa.me/41767574050?text=Hola%20Raudy%20quiero%20VIP%20RAUDY%20ORO%20PRO" class="btn-green">📱 WHATSAPP 0767574050</a>

<div class="footer">RAUDY ORO PRO | raudy-vip-oro.onrender.com<br>© 2026 Ginebra Suiza - Grafico en vivo cada 5 seg</div>

<script>
let hist = {oro:[], gbp:[], eur:[], tesla:[], apple:[]};
let labels = [];
let charts = {};

function crearChart(id, color){
  let ctx = document.getElementById(id).getContext('2d');
  return new Chart(ctx, {
    type: 'line',
    data: { labels: labels, datasets: [{ data: [], borderColor: color, backgroundColor: color+'33', borderWidth: 2, fill: true, tension: 0.4, pointRadius:0 }] },
    options: { responsive:true, plugins:{legend:{display:false}}, scales:{ x:{display:false}, y:{grid:{color:'#222'}, ticks:{color:'#888', font:{size:10}}}} }
  });
}

charts.oro = crearChart('chart-oro', '#FFD700');
charts.gbp = crearChart('chart-gbp', '#00ff00');
charts.eur = crearChart('chart-eur', '#0a84ff');
charts.tesla = crearChart('chart-tesla', '#ff4444');
charts.apple = crearChart('chart-apple', '#ffffff');

async function actualizarTodo(){
  try{
    let r = await fetch('/api/precios?v='+Date.now());
    let d = await r.json();
    let hora = new Date().toLocaleTimeString();
    document.getElementById('oro').innerText = '$' + d.oro.toFixed(2);
    document.getElementById('gbp').innerText = d.gbp.toFixed(4);
    document.getElementById('eur').innerText = d.eur.toFixed(4);
    document.getElementById('tesla').innerText = '$' + d.tesla.toFixed(2);
    document.getElementById('apple').innerText = '$' + d.apple.toFixed(2);
    document.getElementById('hora').innerText = 'Actualizado: ' + hora + ' VIVO - RAUDY ORO PRO';

    labels.push(hora);
    if(labels.length > 20){ labels.shift(); }
    
    function pushHist(key, val, chart){
      hist[key].push(val);
      if(hist[key].length > 20) hist[key].shift();
      chart.data.labels = labels;
      chart.data.datasets[0].data = hist[key];
      chart.update();
    }
    pushHist('oro', d.oro, charts.oro);
    pushHist('gbp', d.gbp, charts.gbp);
    pushHist('eur', d.eur, charts.eur);
    pushHist('tesla', d.tesla, charts.tesla);
    pushHist('apple', d.apple, charts.apple);

    let estOro = document.getElementById('estado-oro');
    if(d.oro > 3940){ estOro.innerHTML='🔴 VENTA 88% - ESPERANDO $3900'; estOro.style.background='#ff0000'; }
    else if(d.oro <= 3905 && d.oro >= 3885){ estOro.innerHTML='🟢 COMPRA BUENA $3900 - $'+d.oro.toFixed(2); estOro.style.background='#00aa00'; }
    else { estOro.innerHTML='🟡 En zona '+d.oro.toFixed(2); estOro.style.background='#FFA500'; }

    let estGbp = document.getElementById('estado-gbp');
    if(d.gbp <= 1.2620){ estGbp.innerHTML='🟢 GBP COMPRA BUENA'; estGbp.style.background='#00aa00'; }
    else if(d.gbp >= 1.2750){ estGbp.innerHTML='🔴 GBP VENTA BUENA'; estGbp.style.background='#ff0000'; }
    else { estGbp.innerHTML='🟡 GBP En zona '+d.gbp.toFixed(4); estGbp.style.background='#333'; }

    let estTesla = document.getElementById('estado-tesla');
    if(d.tesla <= 240){ estTesla.innerHTML='🟢 TESLA COMPRA $'+d.tesla.toFixed(2); estTesla.style.background='#00aa00'; }
    else if(d.tesla >= 275){ estTesla.innerHTML='🔴 TESLA VENTA $'+d.tesla.toFixed(2); estTesla.style.background='#ff0000'; }
    else { estTesla.innerHTML='🟡 TESLA '+d.tesla.toFixed(2); estTesla.style.background='#FFA500'; }

    let estApple = document.getElementById('estado-apple');
    if(d.apple <= 172){ estApple.innerHTML='🟢 APPLE COMPRA $'+d.apple.toFixed(2); estApple.style.background='#00aa00'; }
    else if(d.apple >= 195){ estApple.innerHTML='🔴 APPLE VENTA $'+d.apple.toFixed(2); estApple.style.background='#ff0000'; }
    else { estApple.innerHTML='🟡 APPLE '+d.apple.toFixed(2); estApple.style.background='#FFA500'; }

  }catch(e){ console.log(e); }
}
setInterval(actualizarTodo, 5000);
actualizarTodo();
</script>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
