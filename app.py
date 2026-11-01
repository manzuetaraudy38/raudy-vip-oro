@app.route('/tc')
def tc():
    oro=round(random.uniform(3875.50,3895.80),2)
    eur=round(random.uniform(1.10123,1.13145),5)
    gbp=round(random.uniform(1.31123,1.35145),5)
    senal=random.choice(["VENTA","COMPRA"])
    porc=random.randint(76,89)
    color_senal="#ff1a1a" if senal=="VENTA" else "#00ff66"
    hora=datetime.now().strftime("%H:%M:%S")
    mensaje=f"RAUDY VIP ORO {senal} {porc}% ORO ${oro} - PAGA VIP CHF 20: {PAYPAL_LINK}"
    wsp=f"https://wa.me/?text={quote(mensaje)}"
    return render_template_string(f"""
    <!DOCTYPE html>
    <html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>SEÑAL VIP</title>
    <style>
        body{{background:black;color:white;font-family:Arial;margin:0;padding:15px;text-align:center}}
        .top{{border:2px solid gold;border-radius:15px;padding:12px;color:gold;font-weight:bold;background:#111}}
        .senal-box{{background:{color_senal};color:black;border-radius:20px;padding:30px 15px;margin:20px 0;font-weight:bold}}
        .btn-paypal{{display:block;background:#0070BA;color:white;padding:22px;font-weight:bold;text-decoration:none;border-radius:15px;font-size:22px;margin:20px 0;border:3px solid white}}
        .btn-action{{background:gold;color:black;padding:14px 20px;font-weight:bold;text-decoration:none;border-radius:10px;margin:5px;display:inline-block}}
        .btn-wsp{{background:#25D366;color:white;padding:14px 20px;font-weight:bold;text-decoration:none;border-radius:10px;margin:5px;display:inline-block}}
    </style>
    </head>
    <body>
        <h1 style="color:gold;">RAUDY VIP ORO</h1>
        <div class="top">ORO ${oro} | EUR {eur} | GBP {gbp} | {hora}</div>
        <div class="senal-box">
            <div style="font-size:36px;">{senal}</div>
            <div style="font-size:48px;">{porc}%</div>
            <div style="font-size:16px;background:black;color:white;padding:8px;border-radius:20px;display:inline-block;margin-top:10px;">SEÑAL VIP ACTIVA</div>
        </div>
        <a href="{PAYPAL_LINK}" class="btn-paypal">💳 PAGAR VIP CHF 20 PAYPAL - DESBLOQUEAR</a>
        <p style="color:#00ff66;font-weight:bold;">PAGO SEGURO - ACCESO INMEDIATO 30 DIAS</p>
        <div><a href="/tc" class="btn-action">NUEVA SEÑAL</a><a href="{wsp}" target="_blank" class="btn-wsp">WHATSAPP</a></div>
        <div style="background:#111;border:2px solid gold;border-radius:15px;padding:15px;margin:20px 0;text-align:left;">
            <p style="color:gold;text-align:center;font-weight:bold;">DESBLOQUEA CON CHF 20</p>
            <p>🔒 Entrada exacta<br>🔒 Stop Loss y Take Profit<br>🔒 Grupo VIP<br>🔒 30 días ilimitado<br><br><span style="color:gold;">{PAYPAL_LINK}</span></p>
        </div>
        <a href="/" style="color:gray;">Inicio</a>
    </body></html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
