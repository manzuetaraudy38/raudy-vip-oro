import os, requests
from flask import Flask
app = Flask(__name__)

SYMBOL = 'PAXGUSDT'
TIMEFRAMES = ['1m','5m','15m','1h','4h']

def get_velas(tf, limit=250):
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={tf}&limit={limit}"
    d = requests.get(url, timeout=10).json()
    return [float(x[4]) for x in d]  # closes

def ema(data, span):
    k = 2/(span+1)
    e = data[0]
    out = []
    for v in data:
        e = v*k + e*(1-k)
        out.append(e)
    return out[-1]

def rsi(data, n=14):
    gains=[]; losses=[]
    for i in range(1, len(data)):
        diff = data[i]-data[i-1]
        gains.append(max(diff,0)); losses.append(max(-diff,0))
    ag = sum(gains[-n:])/n; al = sum(losses[-n:])/n
    if al==0: return 100
    rs = ag/al
    return 100-(100/(1+rs))

def analizar():
    datos={}
    for tf in TIMEFRAMES:
        try:
            c = get_velas(tf)
            e50 = ema(c,50); e200 = ema(c,200); r = rsi(c)
            precio = c[-1]
            senal="NEUTRO ⏳"
            if precio > e50 > e200 and 50 < r < 70: senal="SUBE 🟢"
            elif precio < e50 < e200 and 30 < r < 50: senal="BAJA 🔴"
            datos[tf]={"precio":round(precio,2),"rsi":round(r,1),"senal":senal}
        except:
            datos[tf]={"precio":0,"rsi":0,"senal":"ERROR"}
    return datos

@app.route('/')
def inicio():
    d = analizar()
    if d['4h']['senal']=="SUBE 🟢" and d['1h']['senal']=="SUBE 🟢" and d['15m']['senal']=="SUBE 🟢":
        aviso="🚀 JEFE VA A SUBIR! ENTRA AHORA JEFE"; color="#00ff00"
    elif d['4h']['senal']=="BAJA 🔴" and d['1h']['senal']=="BAJA 🔴" and d['15m']['senal']=="BAJA 🔴":
        aviso="📉 JEFE VA A BAJAR! CUIDADO JEFE - NO ENTRES"; color="#ff4444"
    else:
        aviso="⏳ ESPERANDO JEFE... NO HAY ACUERDO"; color="#FFD700"
    filas="".join([f"<tr><td><b>{tf}</b></td><td>${d[tf]['precio']}</td><td>{d[tf]['rsi']}</td><td>{d[tf]['senal']}</td></tr>" for tf in TIMEFRAMES])
    return f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
    body{{background:#0a0a0a;color:#fff;font-family:Arial;text-align:center;padding:15px}}
    .card{{background:#111;border:2px solid #FFD700;border-radius:20px;padding:20px;max-width:480px;margin:auto}}
    h1{{color:#FFD700;margin:0}} .aviso{{background:{color};color:#000;padding:14px;border-radius:12px;font-weight:bold;font-size:18px;margin:15px 0}}
    table{{width:100%}} td,th{{padding:10px;border-bottom:1px solid #333}} th{{color:#FFD700}}
    button{{background:#FFD700;border:none;padding:12px 25px;border-radius:10px;font-weight:bold;margin-top:15px}}
    </style></head><body><div class="card"><p style="color:#00ff00;font-weight:bold">● LIVE</p><h1>👑 RAUDY ORO</h1><p>JEFE - EMA 50 + EMA 200 + RSI</p><div class="aviso">{aviso}</div><table><tr><th>TF</th><th>PRECIO</th><th>RSI</th><th>SEÑAL</th></tr>{filas}</table><button onclick="location.reload()">🔄 ACTUALIZAR</button></div></body></html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
