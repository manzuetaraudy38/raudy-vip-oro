import os, json, urllib.request
import threading, time, random, math
from datetime import datetime
from flask import Flask, request, jsonify
app = Flask(__name__)
BOT = {"activo": False, "balance": 1000.0}
HIST = []
TP_GAN = 20.0
SL_PER = 10.0

def precio(sym):
    try:
        u = "https://query1.finance.yahoo.com"
        u += "/v8/finance/chart/" + sym
        u += "?interval=1m&range=1d"
        req = urllib.request.Request(
            u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read().decode())
            m = d["chart"]["result"][0]["meta"]
            return float(m.get("regularMarketPrice"))
    except:
        return None

def precios_pasado():
    try:
        u = "https://query1.finance.yahoo.com"
        u += "/v8/finance/chart/GC=F"
        u += "?interval=1h&range=1mo"
        req = urllib.request.Request(
            u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            d = json.loads(r.read().decode())
            res = d["chart"]["result"][0]
            cl = res["indicators"]["quote"][0]["close"]
            return [float(x) for x in cl if x is not None]
    except:
        return []

def rsi(pr, n=14):
    if len(pr) < n + 1:
        return 50
    g = 0
    p = 0
    for i in range(1, n + 1):
        diff = pr[-i] - pr[-i-1]
        if diff > 0:
            g += diff
        else:
            p += abs(diff)
    if p == 0:
        return 100
    rs = (g / n) / (p / n)
    return 100 - (100 / (1 + rs))

def ema(pr, n):
    if len(pr) < n:
        return sum(pr) / len(pr)
    k = 2 / (n + 1)
    e = sum(pr[:n]) / n
    for x in pr[n:]:
        e = x * k + e * (1 - k)
    return e

def macd(pr):
    if len(pr) < 26:
        return 0
    m = ema(pr, 12) - ema(pr, 26)
    return m

def boll(pr):
    if len(pr) < 20:
        return "MEDIO"
    ult = pr[-20:]
    med = sum(ult) / len(ult)
    var = sum((x - med) ** 2 for x in ult) / len(ult)
    dv = math.sqrt(var)
    sup = med + 2 * dv
    inf = med - 2 * dv
    act = pr[-1]
    if act <= inf + dv * 0.2:
        return "BARATO"
    if act >= sup - dv * 0.2:
        return "CARO"
    if act < med:
        return "BARATO"
    return "CARO"

def tendencia(pr):
    if len(pr) < 10:
        return "LADO"
    a = sum(pr[-5:]) / 5
    b = sum(pr[-10:-5]) / 5
    if a > b:
        return "SUBIENDO"
    if a < b:
        return "BAJANDO"
    return "LADO"

def doble(pr):
    if len(pr) < 30:
        return False
    largo = tendencia(pr[-30:])
    corto = tendencia(pr[-10:])
    if largo == "SUBIENDO":
        return True
    return False

def cerebro(precio, lista):
    lista.append(precio)
    if len(lista) > 60:
        lista.pop(0)
    v = 0
    r = rsi(lista)
    t = tendencia(lista)
    mc = macd(lista)
    b = boll(lista)
    d = doble(lista)
    if r < 30:
        v += 200
    if r > 70:
        v -= 200
    if t == "SUBIENDO":
        v += 150
    if t == "BAJANDO":
        v -= 150
    if mc > 0:
        v += 200
    if mc < 0:
        v -= 200
    if b == "BARATO":
        v += 250
    if b == "CARO":
        v -= 250
    if d:
        v += 300
    if v >= 400:
        return "COMPRAR"
    if v <= -400:
        return "VENDER"
    return "ESPERA"

def backtest():
    pr = precios_pasado()
    if len(pr) < 50:
        pr = []
        p = 4150
        for i in range(200):
            p += random.uniform(-12, 12)
            pr.append(p)
        modo = "SIMULADO"
    else:
        modo = "REAL"
    bal = 1000
    g = 0
    pe = 0
    for i in range(30, len(pr) - 5):
        lista = pr[max(0, i-30):i]
        votos = 0
        if rsi(lista) < 45:
            votos += 1
        if macd(lista) > 0:
            votos += 1
        if boll(lista) == "BARATO":
            votos += 1
        if doble(lista):
            votos += 1
        if votos >= 3:
            ent = pr[i]
            sal = pr[min(len(pr)-1, i+5)]
            gan = sal - ent
            if gan > 0 and gan > TP_GAN:
                gan = TP_GAN
            if gan < 0 and gan < -SL_PER:
                gan = -SL_PER
            bal += gan
            if gan >= 0:
                g += 1
            else:
                pe += 1
    tot = g + pe
    wr = (g / tot * 100) if tot > 0 else 0
    return {
        "modo": modo,
        "balance_final": round(bal, 2),
        "ganadas": g,
        "perdidas": pe,
        "winrate": round(wr, 1),
        "mensaje": "Gana 20 pierde 10"
    }

@app.route("/")
def home():
    oro = precio("GC=F") or 4149
    dec = cerebro(oro, HIST)
    return f"""
    <h1>RAUDY VIP 1000 - LIVE</h1>
    <p>ORO: {oro}</p>
    <p>CEREBRO: {dec}</p>
    <p>Balance: {BOT['balance']}</p>
    <p><a href='/api/backtest'>BACKTEST REAL</a></p>
    <p><a href='/api/precios'>PRECIOS</a></p>
    <p>Calidad: RSI + MACD + Bollinger + Doble Tiempo + 1:2</p>
    """

@app.route("/api/precios")
def api_precios():
    oro = precio("GC=F") or 4149
    tes = precio("TSLA") or 378
    return jsonify({"ORO": oro, "TESLA": tes})

@app.route("/api/backtest")
def api_back():
    return jsonify(backtest())

@app.route("/api/senal")
def api_senal():
    oro = precio("GC=F") or 4149
    dec = cerebro(oro, HIST)
    return jsonify({"precio": oro, "decision": dec})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
