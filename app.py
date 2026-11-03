from flask import Flask
import requests

app = Flask(__name__)

def get_price_yahoo(symbol, fallback):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
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
        "gbp": get_price_yahoo('GBPUSD=X', 1.3412),
        "eur": get_price_yahoo('EURUSD=X', 1.1197),
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
</style>
</head>
<body>

<div class="header">
<h1>🔥 RAUDY ORO PRO 🔥</h1>
<div style="font-size:11px; color:#aaa;">APP OFICIAL - VELAS JAPONESAS EN VIVO</div>
<div style="font-size:11px; color:#00ff00;" id="hora">VIVO - RAUDY ORO PRO</div>
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

<div class="footer">App: RAUDY ORO PRO | raudy-vip-oro.onrender.com<br>Alarmas: Oro $3900, GBP 1.2580, Tesla $235, Apple $168<br>© 2026 Ginebra Suiza - Velas en vivo</div>

<script>
function makeCandleChart(elemId){
  const chart = LightweightCharts.createChart(document.getElementById(elemId), {
    layout: { background: { color: '#0f0f0f' }, textColor: '#888' },
    grid: { vertLines: { color: '#222' }, horzLines: { color: '#222' } },
    width: document.getElementById(elemId).clientWidth,
    height: 180,
    timeScale: { timeVisible: true, secondsVisible: true }
  });
  const series = chart.addCandlestickSeries({ upColor: '#00ff00', downColor: '#ff4444', borderVisible: false, wickUpColor: '#00ff00', wickDownColor: '#ff4444' });
  return { chart, series, data: [] };
}

let charts = {
  oro: makeCandleChart('chart-oro'),
  gbp: makeCandleChart('chart-gbp'),
  eur: makeCandleChart('chart-eur'),
  tesla: makeCandleChart('chart-tesla'),
  apple: makeCandleChart('chart-apple')
};

function addCandle(cObj, price){
  let now = Math.floor(Date.now() / 1000);
  let last = cObj.data[cObj.data.length - 1];
  if(!last || (now - last.time) >= 15){
    let candle = { time: now, open: last ? last.close : price, high: price, low: price, close: price };
    cObj.data.push(candle);
    if(cObj.data.length > 60) cObj.data.shift();
  } else {
    last.high = Math.max(last.high, price);
    last.low = Math.min(last.low, price);
    last.close = price;
  }
  cObj.series.setData(cObj.data);
}

async function actualizar(){
  try{
    let r = await fetch('/api/precios?v=' + Date.now());
    let d = await r.json();
    let hora = new Date().toLocaleTimeString();
    document.getElementById('oro').innerText = '$' + d.oro.toFixed(2);
    document.getElementById('gbp').innerText = d.gbp.toFixed(4);
    document.getElementById('eur').innerText = d.eur.toFixed(4);
    document.getElementById('tesla').innerText = '$' + d.tesla.toFixed(2);
    document.getElementById('apple').innerText = '$' + d.apple.toFixed(2);
    document.getElementById('hora').innerText = 'Actualizado: ' + hora + ' VIVO - RAUDY ORO PRO VELAS';
    addCandle(charts.oro, d.oro);
    addCandle(charts.gbp, d.gbp);
    addCandle(charts.eur, d.eur);
    addCandle(charts.tesla, d.tesla);
    addCandle(charts.apple, d.apple);
    let eo = document.getElementById('estado-oro');
    if(d.oro > 3940){ eo.innerHTML = '🔴 VENTA 88% - ESPERANDO $3900'; eo.style.background = '#ff0000'; }
    else if(d.oro <= 3905 && d.oro >= 3885){ eo.innerHTML = '🟢 COMPRA BUENA $3900'; eo.style.background = '#00aa00'; }
    else { eo.innerHTML = '🟡 En zona ' + d.oro.toFixed(2); eo.style.background = '#FFA500'; }
  }catch(e){}
}
setInterval(actualizar, 5000);
actualizar();
</script>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
