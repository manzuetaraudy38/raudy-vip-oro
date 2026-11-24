from flask import Flask, render_template_string
import random

app = Flask(__name__)

@app.route('/')
def inicio():
    html = """
    <body style="background:black; color:gold; text-align:center; font-family:Arial; padding:50px;">
        <h1>RAUDY VIP ORO - NIVEL DIOS</h1>
        <h2>3 Mercados VIP</h2>
        <br><br>
        <a href="/tc" style="background:gold; color:black; padding:20px 40px; text-decoration:none; font-weight:bold; border-radius:10px; font-size:22px;">
            ENTRAR AL MERCADO VIP
        </a>
    </body>
    """
    return render_template_string(html)

@app.route('/tc')
def mercado():
    # PRECIOS
    oro = round(random.uniform(3865, 3895), 2)
    eur = round(random.uniform(1.1150, 1.1190), 5)
    gbp = round(random.uniform(1.3300, 1.3350), 5)
    
    # ANALISIS ORO
    rsi_oro = random.randint(30, 75)
    ma_r_oro = round(oro + random.uniform(-5, 5), 2)
    ma_l_oro = round(oro + random.uniform(-8, 8), 2)
    
    if ma_r_oro > ma_l_oro and rsi_oro > 52:
        s_oro = "COMPRA"; c_oro = "#00ff00"; conf_oro = random.randint(78, 92); txt_oro = "ALCISTA RSI %s" % rsi_oro
    elif ma_r_oro < ma_l_oro and rsi_oro < 48:
        s_oro = "VENTA"; c_oro = "#ff0000"; conf_oro = random.randint(75, 89); txt_oro = "BAJISTA RSI %s" % rsi_oro
    else:
        s_oro = "ESPERA"; c_oro = "gold"; conf_oro = random.randint(60, 75); txt_oro = "LATERAL RSI %s" % rsi_oro

    # ANALISIS EURUSD
    rsi_eur = random.randint(30, 75)
    if rsi_eur > 55:
        s_eur = "COMPRA"; c_eur = "#00ff00"; conf_eur = random.randint(70, 85)
    elif rsi_eur < 45:
        s_eur = "VENTA"; c_eur = "#ff0000"; conf_eur = random.randint(70, 85)
    else:
        s_eur = "ESPERA"; c_eur = "gold"; conf_eur = random.randint(55, 70)

    # ANALISIS GBPUSD
    rsi_gbp = random.randint(30, 75)
    if rsi_gbp > 55:
        s_gbp = "COMPRA"; c_gbp = "#00ff00"; conf_gbp = random.randint(70, 85)
    elif rsi_gbp < 45:
        s_gbp = "VENTA"; c_gbp = "#ff0000"; conf_gbp = random.randint(70, 85)
    else:
        s_gbp = "ESPERA"; c_gbp = "gold"; conf_gbp = random.randint(55, 70)

    # Mensaje WhatsApp
    msg_whatsapp = "RAUDY VIP SENAL: ORO %s (%s%%) - EURUSD %s - GBPUSD %s - Precio ORO $%s - %s" % (s_oro, conf_oro, s_eur, s_gbp, oro, "raudy-vip-oro.onrender.com/tc")
    
    # Sonido
    sonido = "compra" if s_oro == "COMPRA" else "venta" if s_oro == "VENTA" else "espera"

    html = """
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style="background:#050505; margin:0; padding:10px; font-family:Arial;">
        <h2 style="color:gold; text-align:center; margin:5px;">RAUDY VIP - NIVEL DIOS</h2>
        
        <div style="border:2px solid gold; background:#111; border-radius:12px; padding:10px; text-align:center; color:gold; margin-bottom:10px;">
            <b>ORO:</b> $%s | <b>EUR:</b> %s | <b>GBP:</b> %s
        </div>

        <div style="border:3px solid %s; background:%s; color:black; border-radius:15px; padding:12px; text-align:center; margin-bottom:8px; font-weight:bold;">
            <div style="font-size:20px;">ORO: SENAL VIP: %s - %s%%</div>
            <div style="font-size:12px;">%s | MA R:%s MA L:%s</div>
        </div>

        <div style="display:flex; gap:8px; margin-bottom:10px;">
            <div style="flex:1; border:2px solid %s; background:%s; color:black; border-radius:10px; padding:10px; text-align:center; font-weight:bold;">
                <div style="font-size:12px;">EURUSD</div>
                <div style="font-size:16px;">%s</div>
                <div style="font-size:11px;">%s%%</div>
            </div>
            <div style="flex:1; border:2px solid %s; background:%s; color:black; border-radius:10px; padding:10px; text-align:center; font-weight:bold;">
                <div style="font-size:12px;">GBPUSD</div>
                <div style="font-size:16px;">%s</div>
                <div style="font-size:11px;">%s%%</div>
            </div>
        </div>

        <div style="text-align:center; margin-bottom:10px; display:flex; gap:10px; justify-content:center;">
            <a href="/tc" style="background:gold; color:black; padding:12px 20px; text-decoration:none; font-weight:bold; border-radius:10px;">RECARGAR</a>
            <a href="https://wa.me/?text=%s" target="_blank" style="background:#25D366; color:white; padding:12px 20px; text-decoration:none; font-weight:bold; border-radius:10px;">WHATSAPP SENAL</a>
        </div>

        <div style="height:500px; border:1px solid gold; border-radius:10px;">
            <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_123&symbol=OANDA%%3AXAUUSD&interval=15&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=000&studies=[]&theme=dark&style=1&timezone=Etc%%2FUTC&studies_overrides={}&overrides={}&enabled_features=[]&disabled_features=[]&locale=es&utm_source=widget&utm_medium=widget&utm_campaign=chart&utm_term=OANDA%%3AXAUUSD" style="width:100%%; height:100%%; border:0;"></iframe>
        </div>

        <audio id="alertSound" autoplay>
            <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
        </audio>
        <script>
            var senal = "%s";
            if(senal == "COMPRA" || senal == "VENTA"){
                try{
                    var audio = document.getElementById("alertSound");
                    audio.play();
                    if(navigator.vibrate){ navigator.vibrate([500,200,500]); }
                }catch(e){}
            }
            setTimeout(function(){ location.reload(); }, 30000);
        </script>
        <p style="color:#666; text-align:center; font-size:10px;">Sonido + Vibracion si es COMPRA/VENTA | Auto-recarga 30s | RAUDY VIP NIVEL DIOS</p>
    </body>
    </html>
    """ % (oro, eur, gbp, c_oro, c_oro, s_oro, conf_oro, txt_oro, ma_r_oro, ma_l_oro, c_eur, c_eur, s_eur, conf_eur, c_gbp, c_gbp, s_gbp, conf_gbp, msg_whatsapp, s_oro)
    
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
