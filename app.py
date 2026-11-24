import requests, random, math, wave, struct, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from collections import deque

TARGET = 3890
last = 4030

# --- SONIDO ---
def crear_sonido():
    try:
        file = '/tmp/alarma.wav'
        if not os.path.exists(file):
            w = wave.open(file, 'w')
            w.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
            for i in range(88200): # 2 seg
                val = int(32767 * 0.7 * math.sin(2*math.pi*900*i/44100))
                w.writeframes(struct.pack('h', val))
            w.close()
        return file
    except:
        return None

SONIDO_FILE = crear_sonido()
sound = SoundLoader.load(SONIDO_FILE) if SONIDO_FILE else None

def get_price():
    global last
    try:
        r = requests.get("https://data-asg.goldprice.org/dbXRates/USD", timeout=3).json()
        last = float(r['items'][0]['xauPrice'])
        return last
    except:
        last += random.uniform(-4, 4)
        return last

def ema_calc(data, period):
    if len(data) < period:
        return sum(data)/len(data)
    k = 2/(period+1)
    ema = sum(data[:period])/period
    for p in data[period:]:
        ema = p*k + ema*(1-k)
    return ema

def notificar(titulo, mensaje):
    try:
        from plyer import notification
        notification.notify(title=titulo, message=mensaje, app_name='ORO RAUDY', timeout=10)
    except:
        pass
    try:
        from plyer import vibrator
        vibrator.vibrate(1.5)
    except:
        pass
    try:
        if sound:
            sound.play()
    except:
        pass

candles = deque(maxlen=30)
prices = deque(maxlen=60)
for i in range(25):
    o = 4030 + random.uniform(-3,3)
    c = o + random.uniform(-4,4)
    candles.append({'o':o, 'h':max(o,c)+2, 'l':min(o,c)-2, 'c':c})
    prices.append(c)

ema20_hist = deque(maxlen=30)
ema50_hist = deque(maxlen=30)

class CandleGraph(Widget):
    def update(self, candles_list, e20_list, e50_list):
        self.canvas.clear()
        if len(candles_list) < 2:
            return
        with self.canvas:
            all_vals = []
            for c in candles_list:
                all_vals.extend([c['h'], c['l']])
            all_vals.extend(e20_list)
            all_vals.extend(e50_list)
            min_p = min(all_vals)
            max_p = max(all_vals)
            diff = max_p - min_p
            if diff < 5:
                diff = 5
            w = self.width
            h = self.height
            candle_w = w / len(candles_list) * 0.6
            for i, c in enumerate(candles_list):
                x = self.x + (i / len(candles_list)) * w + 2
                h_y = self.y + ((c['h'] - min_p)/diff)*h
                l_y = self.y + ((c['l'] - min_p)/diff)*h
                o_y = self.y + ((c['o'] - min_p)/diff)*h
                cl_y = self.y + ((c['c'] - min_p)/diff)*h
                Color(0.6,0.6,0.6,1)
                Line(points=[x+candle_w/2, l_y, x+candle_w/2, h_y], width=1)
                if c['c'] >= c['o']:
                    Color(0,1,0,1)
                else:
                    Color(1,0,0,1)
                Rectangle(pos=(x, min(o_y, cl_y)), size=(candle_w, max(4, abs(cl_y - o_y))))
            if len(e20_list) > 1:
                Color(1,1,1,0.9)
                points = []
                for i, val in enumerate(e20_list):
                    x = self.x + (i / len(candles_list)) * w + candle_w/2 + 2
                    y = self.y + ((val - min_p)/diff)*h
                    points.extend([x,y])
                Line(points=points, width=1.5)
            if len(e50_list) > 1:
                Color(0,0.5,1,0.9)
                points = []
                for i, val in enumerate(e50_list):
                    x = self.x + (i / len(candles_list)) * w + candle_w/2 + 2
                    y = self.y + ((val - min_p)/diff)*h
                    points.extend([x,y])
                Line(points=points, width=1.5)

class RaudyApp(App):
    def build(self):
        self.box = BoxLayout(orientation='vertical', padding=10, spacing=5)
        self.l1 = Label(text='ORO $4030', font_size='40sp', bold=True, color=(1,0.84,0,1), size_hint=(1,0.15))
        self.graph = CandleGraph(size_hint=(1,0.5))
        self.l2 = Label(text='BLANCA 20 | AZUL 50', font_size='16sp', size_hint=(1,0.07))
        self.l3 = Label(text='SCORE 10% - ESPERA', font_size='28sp', bold=True, size_hint=(1,0.14))
        self.l4 = Label(text='FALTAN $140 para $3890', font_size='20sp', size_hint=(1,0.14))
        self.box.add_widget(self.l1)
        self.box.add_widget(self.graph)
        self.box.add_widget(self.l2)
        self.box.add_widget(self.l3)
        self.box.add_widget(self.l4)
        self.counter = 0
        self.notificado = False
        notificar('ROBOT RAUDY ACTIVO', 'Te avisare cuando ORO llegue a $3890')
        Clock.schedule_interval(self.update, 3)
        return self.box

    def update(self, dt):
        global candles
        p = get_price()
        prices.append(p)
        self.counter += 1
        if self.counter % 3 == 0:
            last_c = candles[-1]['c']
            candles.append({'o':last_c, 'h':max(last_c,p), 'l':min(last_c,p), 'c':p})
        else:
            c = candles[-1]
            candles[-1] = {'o':c['o'], 'h':max(c['h'],p), 'l':min(c['l'],p), 'c':p}
        e20 = ema_calc(list(prices), 20)
        e50 = ema_calc(list(prices), 50)
        ema20_hist.append(e20)
        ema50_hist.append(e50)
        faltan = p - TARGET
        score = 10
        if p < 3950: score = 40
        if p < 3920: score = 60
        if p < 3900: score = 80
        if p <= TARGET and e20 > e50: score = 95
        
        self.l1.text = f'ORO ${p:.0f}'
        self.l2.text = f'BLANCA 20 ${e20:.0f} | AZUL 50 ${e50:.0f}'
        self.l4.text = f'FALTAN ${faltan:.0f} para ${TARGET}'
        self.graph.update(list(candles), list(ema20_hist), list(ema50_hist))
        
        if score >= 80:
            self.l3.text = f'SCORE {score}% - BUY AHORA!!'
            self.l3.color = (0,1,0,1)
            if not self.notificado:
                notificar('¡¡¡ COMPRA ORO AHORA !!!', f'ORO llego a ${p:.0f} - TARGET ${TARGET}')
                self.notificado = True
        elif score >= 50:
            self.l3.text = f'SCORE {score}% - CERCA'
            self.l3.color = (1,1,0,1)
            self.notificado = False
        else:
            self.l3.text = f'SCORE {score}% - ESPERA'
            self.l3.color = (1,1,1,1)
            self.notificado = False

RaudyApp().run()
