from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import random

precio=4058.24
hist=[precio]*50

class VelasApp(App):
 def build(self):
  self.root=BoxLayout(orientation='vertical',padding=5)
  self.titulo=Label(text="XAUUSD M5",font_size=40,bold=True,size_hint=(1,0.08))
  self.vela=Label(text="VELA",font_size=160,size_hint=(1,0.32))
  self.precio=Label(text="$4058",font_size=100,bold=True,color=(0,1,0,1),size_hint=(1,0.15))
  self.ema=Label(text="EMA 4050",font_size=55,bold=True,color=(0.3,0.7,1,1),size_hint=(1,0.13))
  self.rsi=Label(text="RSI 60",font_size=65,bold=True,color=(1,1,0,1),size_hint=(1,0.13))
  self.senal=Label(text="COMPRAR 90%",font_size=70,bold=True,color=(0,1,0,1),size_hint=(1,0.19))
  self.root.add_widget(self.titulo)
  self.root.add_widget(self.vela)
  self.root.add_widget(self.precio)
  self.root.add_widget(self.ema)
  self.root.add_widget(self.rsi)
  self.root.add_widget(self.senal)
  Clock.schedule_interval(self.actualizar,0.5)
  return self.root

 def actualizar(self,dt):
  global precio
  viejo=precio
  precio=precio+random.uniform(-2,2)
  hist.append(precio)
  hist.pop(0)
  e20=sum(hist[-20:])/20
  e50=sum(hist[-50:])/50
  rsi=50+random.uniform(-15,15)
  if precio>viejo:
   self.vela.text="VERDE"
   self.vela.color=(0,1,0,1)
   self.precio.color=(0,1,0,1)
   self.senal.color=(0,1,0,1)
   self.senal.text="COMPRAR 90%"
  else:
   self.vela.text="ROJA"
   self.vela.color=(1,0,0,1)
   self.precio.color=(1,0,0,1)
   self.senal.color=(1,0,0,1)
   self.senal.text="VENDER 88%"
  self.precio.text="$"+str(round(precio,2))
  self.ema.text="EMA20 "+str(round(e20,1))+" 50 "+str(round(e50,1))
  self.rsi.text="RSI "+str(round(rsi,1))

VelasApp().run()
