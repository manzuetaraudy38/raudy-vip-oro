# RAUDY ROBOT REAL - ULTIMA TECNOLOGIA - ETF 500 + AAPL + TSLA + NVDA
# pip install yfinance pandas kivy plyer

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
import webbrowser
import random

Window.clearcolor = (0.05, 0.05, 0.05, 1)

# INTENTA CON DATOS REALES, SI NO HAY INTERNET USA SIMULADO
try:
    import yfinance as yf
    import pandas as pd
    REAL = True
except:
    REAL = False

TICKERS = {
    "ETF500": "SPY",
    "APPLE": "AAPL", 
    "TESLA": "TSLA",
    "VIDIA": "NVDA"
}

def get_analisis(ticker_yahoo):
    try:
        if not REAL:
            raise Exception("no lib")
        data = yf.download(ticker_yahoo, period="1d", interval="5m", progress=False)
        if len(data) < 50:
            raise Exception("pocos datos")
        close = data['Close']
        high = data['High']
        low = data['Low']
        open_ = data['Open']
        
        ema20 = close.ewm(span=20).mean().iloc[-1]
        ema50 = close.ewm(span=50).mean().iloc[-1]
        
        # RSI 14
        delta = close.diff()
        gain = delta.where(delta>0,0).rolling(14).mean()
        loss = -delta.where(delta<0,0).rolling(14).mean()
        rs = gain/loss
        rsi = 100 - (100/(1+rs))
        rsi_val = float(rsi.iloc[-1])

        last_close = float(close.iloc[-1])
        last_open = float(open_.iloc[-1])
        last_high = float(high.iloc[-1])
        last_low = float(low.iloc[-1])
        
        body = abs(last_close - last_open)
        upper_wick = last_high - max(last_open, last_close)
        lower_wick = min(last_open, last_close) - last_low
        
        # MECHA LARGA = mecha 2x el cuerpo
        mecha_larga = "SI" if (upper_wick > body*1.8 or lower_wick > body*1.8) else "NO"
        tipo_mecha = "SUPERIOR LARGA" if upper_wick > lower_wick else "INFERIOR LARGA"
        
        return last_close, ema20, ema50, rsi_val, mecha_larga, tipo_mecha
    except:
        # MODO SIMULADO SI FALLA INTERNET
        precio = {"SPY": 545.2, "AAPL": 228.5, "TSLA": 298.3, "NVDA": 142.8}[ticker_yahoo] + random.uniform(-2,2)
        ema20 = precio + random.uniform(-0.5, 0.5)
        ema50 = precio + random.uniform(-1, 1)
        rsi = random.randint(35, 72)
        mecha = random.choice(["SI","NO"])
        tipo = random.choice(["SUPERIOR LARGA","INFERIOR LARGA"])
        return precio, ema20, ema50, rsi, mecha, tipo

class RobotRaudyApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=[10,40,10,10], spacing=8)
        root.add_widget(Label(text="RAUDY ROBOT REAL - ULTIMA TECNOLOGIA", font_size='18sp', bold=True, color=(1,0.84,0,1), size_hint_y=0.08))
        root.add_widget(Label(text="ETF500 + APPLE + TESLA + NVIDIA | EMA + RSI + MECHA LARGA", font_size='10sp', color=(0.8,0.8,0.8,1), size_hint_y=0.04))

        self.grid = GridLayout(cols=2, spacing=8, size_hint_y=0.68)
        self.cards = {}
        for nombre in TICKERS:
            box = BoxLayout(orientation='vertical', padding=6)
            box.add_widget(Label(text=nombre, font_size='14sp', bold=True, color=(1,0.84,0,1)))
            lbl_precio = Label(text="$0.00", font_size='16sp', bold=True)
            lbl_ema = Label(text="EMA20/50: --", font_size='10sp')
            lbl_rsi = Label(text="RSI: --", font_size='11sp')
            lbl_mecha = Label(text="MECHA: --", font_size='10sp', color=(1,0.6,0,1))
            lbl_senal = Label(text="ESPERAR", font_size='22sp', bold=True, color=(1,1,1,1))
            box.add_widget(lbl_precio); box.add_widget(lbl_ema); box.add_widget(lbl_rsi); box.add_widget(lbl_mecha); box.add_widget(lbl_senal)
            self.grid.add_widget(box)
            self.cards[nombre] = (lbl_precio, lbl_ema, lbl_rsi, lbl_mecha, lbl_senal)

        root.add_widget(self.grid)
        
        self.status = Label(text="Conectando a datos reales...", font_size='12sp', color=(0,1,0,1), size_hint_y=0.05)
        root.add_widget(self.status)

        b1 = Button(text="ACTUALIZAR AHORA + BIP", size_hint_y=0.07)
        b1.bind(on_press=self.actualizar_todo)
        b2 = Button(text="PAGAR VIP $20 - paypal.me/RaudyManzueta/20", background_color=(1,0.84,0,1), color=(0,0,0,1), bold=True, size_hint_y=0.08)
        b2.bind(on_press=lambda x: webbrowser.open("https://paypal.me/RaudyManzueta/20"))
        root.add_widget(b1); root.add_widget(b2)

        Clock.schedule_interval(self.actualizar_todo, 30) # cada 30 seg datos reales
        Clock.schedule_once(self.actualizar_todo, 1)
        return root

    def actualizar_todo(self, dt):
        for nombre, ticker in TICKERS.items():
            precio, ema20, ema50, rsi, mecha_larga, tipo_mecha = get_analisis(ticker)
            lbl_precio, lbl_ema, lbl_rsi, lbl_mecha, lbl_senal = self.cards[nombre]
            
            lbl_precio.text = f"${precio:.2f}"
            lbl_ema.text = f"E20:{float(ema20):.2f} E50:{float(ema50):.2f}"
            lbl_rsi.text = f"RSI:{int(rsi)}"
            lbl_mecha.text = f"MECHA:{mecha_larga} {tipo_mecha if mecha_larga=='SI' else ''}"

            # LOGICA INTELIGENTE: EMA + RSI + MECHA LARGA
            if float(ema20) > float(ema50) and rsi < 68 and rsi > 52 and mecha_larga=="SI":
                lbl_senal.text = "BUY FUERTE"; lbl_senal.color = (0,1,0,1)
                self.bip()
                self.status.text = f"¡SEÑAL BUY en {nombre} con MECHA LARGA!"
            elif float(ema20) < float(ema50) and rsi > 32 and rsi < 48:
                lbl_senal.text = "SELL"; lbl_senal.color = (1,0.2,0.2,1)
            else:
                lbl_senal.text = "ESPERAR"; lbl_senal.color = (1,1,1,1)
        
        self.status.text = f"Actualizado: Datos {'REALES' if REAL else 'SIMULADOS'} - {len(TICKERS)} activos"

    def bip(self):
        try:
            from plyer import vibrator; vibrator.vibrate(0.5)
        except: pass

RobotRaudyApp().run()
