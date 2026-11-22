import os, requests
from flask import Flask
app = Flask(__name__)

# TU CONFIGURACION JEFE - IGUAL QUE TU CODIGO
SYMBOL = 'BTCUSDT'  # Si quieres ORO jefe, cambialo a PAXGUSDT
TIMEFRAMES = ['1m','5m','15m','1h','4h']
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN','TU_TOKEN_DE_TELEGRAM')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID','TU_CHAT_ID')

def get_velas(tf, limit=250):
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={tf}&limit={limit}"
    d = requests.get(url, timeout=10).json()
    return [float(x[4]) for x in d]

def ema(data, span):
    k = 2/(span+1); e = data[0]
    for v in data: e = v*k + e*(1-k)
    return e

def rsi(data, n=14):
    gains=[]; losses=[]
    for i in range(1,len(data)):
        diff=data[i]-data[i-1]
        gains.append(max(diff,0)); losses.append(max(-diff,0))
    ag=sum(gains[-n:])/n; al=sum(losses[-n:])/n
    if al==0: return 100
    return 100-(100/(1+ag/al))

def analizar():
    senales={}; datos={}
    for tf in TIMEFRAMES:
        try:
            c=get_velas(tf)
            e50=ema(c,50); e200=ema(c,200); r=rsi(c); precio=c[-1]
            senal="NEUTRO ⏳"
            if precio > e50 > e200 and 50 < r < 70: senal="SUBE 🟢"
            elif precio < e50 < e200 and 30 < r < 50: senal="BAJA 🔴"
            senales[tf]=senal
            datos[tf]={"precio":round(precio,2),"ema50":round(e50,2),"ema200":round(e200,2),"rsi":round(r,1),"senal":senal}
        except:
            senales[tf]="ERROR"; datos[tf]={"precio":0,"ema50":0,"ema200":0,"rsi":0,"senal":"ERROR"}
    return senales, datos

def enviar_telegram(mensaje):
    if TELEGRAM_TOKEN.startswith('TU_'): return
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={'chat_id':TELEGRAM_CHAT_ID,'text':mensaje}, timeout=10)
    except: pass

@app.route('/')
def inicio():
    senales, d = analizar()
    if senales.get('4h')=="SUBE 🟢" and senales.get('1h')=="SUBE 🟢" and senales.get('15m')=="SUBE 🟢":
        aviso="🚀 JEFE VA A SUBIR! ENTRA AHORA JEFE"; color="#00ff00"
        enviar_telegram(f"🚀 JEFE VA A SUBIR! {SYMBOL}\n4H: SUBE\n1H: SUBE\n15m: SUBE")
    elif senales.get('4h')=="BAJA 🔴" and senales.get('1h')=="BAJA 🔴" and senales.get('15m')=="BAJA 🔴":
        aviso="📉 JEFE VA A BAJAR! CUIDADO JEFE - NO ENTRES"; color="#ff4444"
        enviar_telegram(f"📉 JEFE VA A BAJAR! {SYMBOL}\n4H: BAJA\n1H: BAJA\n15m: BAJA")
    else:
        aviso="⏳ ESPERANDO JEFE... NO HAY ACUERDO"; color="#FFD700"
    filas="".join([f"<tr><td><b>{tf}</b></td><td>${d[tf]['precio']}</td><td>{d[tf]['ema50']}</td><td>{d[tf]['ema200']}</td><td>{d[tf]['rsi']}</td><td>{d[tf]['senal']}</td></tr>" for tf in TIMEFRAMES])
    return f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
    body{{background:#0a0a0a;color:#fff;font-family:Arial;text-align:center;padding:15px}}
    .card{{background:#111;border:2px solid #FFD700;border-radius:20px;padding:20px;max-width:520px;margin:auto}}
    h1{{color:#FFD700;margin:0}} .aviso{{background:{color};color:#000;padding:14px;border-radius:12px;font-weight:bold;font-size:18px;margin:15px 0}}
    table{{width:100%;font-size:13px}} td,th{{padding:8px;border-bottom:1px solid #333}} th{{color:#FFD700}}
    button{{background:#FFD700;border:none;padding:12px 25px;border-radius:10px;font-weight:bold;margin-top:15px}}
    </style></head><body><div class="card"><p style="color:#00ff00;font-weight:bold">● LIVE</p><h1>👑 ROBOT JEFE</h1><p>EMA 50 + EMA 200 + RSI - {SYMBOL}</p><div class="aviso">{aviso}</div><table><tr><th>TF</th><th>PRECIO</th><th>EMA50</th><th>EMA200</th><th>RSI</th><th>SEÑAL</th></tr>{filas}</table><button onclick="location.reload()">🔄 ACTUALIZAR</button><p style="color:#888;font-size:12px">1m 5m 15m 1h 4h - JEFE TE AVISA</p></div></body></html>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
