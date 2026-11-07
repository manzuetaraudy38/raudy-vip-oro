from flask import Flask, jsonify, request
import requests, json, os, re
from datetime import datetime
app = Flask(__name__)
F="cerebro_memoria.json"
C={"historial":[],"veces_compra":0,"veces_venta":0,"veces_espera":0,"ultima_leccion":"Todavia no aprendi nada jefe."}
def cg():
 global C
 try:
  if os.path.exists(F): C=json.load(open(F))
 except: pass
def cs():
 try: json.dump(C,open(F,"w"))
 except: pass
def cap(d,o):
 global C
 oro=d.get("ORO",4088); orden=o.get("orden","")
 if "COMPRA" in orden or oro<=3910: dec="COMPRA"; C["veces_compra"]+=1
 elif "VENTA" in orden or oro>=3970: dec="VENTA"; C["veces_venta"]+=1
 else: dec="ESPERA"; C["veces_espera"]+=1
 lec="Jefe, ORO en $"+str(oro)+". Me acuerdo de la ultima vez." if oro>3910 and oro<3970 else ("Jefe, ORO bajo a $"+str(oro)+". Despues SUBIO." if oro<=3910 else "Jefe, ORO subio a $"+str(oro)+". Despues BAJO.")
 C["ultima_leccion"]=lec; C["historial"].append({"hora":datetime.now().strftime("%H:%M:%S"),"oro":oro,"decision":dec,"leccion":lec}); C["historial"]=C["historial"][-20:]; cs(); return C
def crec():
 t=C["veces_compra"]+C["veces_venta"]+C["veces_espera"]
 if t==0: return {"mensaje":"🧠 Cerebro empezando jefe.","total":0,"leccion":C["ultima_leccion"]}
 return {"mensaje":"🧠 Me acuerdo de "+str(t)+" jugadas - COMPRA: "+str(C["veces_compra"])+" | VENTA: "+str(C["veces_venta"])+" | ESPERA: "+str(C["veces_espera"]),"total":t,"leccion":C["ultima_leccion"],"historial":C["historial"][-5:]}
cg()
FM5="cerebro_m5.json"
M5={"velas":[],"ultima":"Todavia no vi velas M5 jefe.","subidas_seguidas":0,"bajadas_seguidas":0}
def m5_cargar():
 global M5
 try:
  if os.path.exists(FM5): M5=json.load(open(FM5))
 except: pass
def m5_guardar():
 try: json.dump(M5,open(FM5,"w"))
 except: pass
def m5_aprende(precio):
 global M5
 M5["velas"].append({"hora":datetime.now().strftime("%H:%M:%S"),"precio":precio}); M5["velas"]=M5["velas"][-20:]
 if len(M5["velas"])>=3:
  a=M5["velas"][-3]["precio"]; b=M5["velas"][-2]["precio"]; c=M5["velas"][-1]["precio"]
  if c>b>a: M5["subidas_seguidas"]+=1; M5["bajadas_seguidas"]=0; M5["ultima"]="Jefe M5: ORO subio 3 velas seguidas "+str(a)+" -> "+str(b)+" -> "+str(c)+". Despues BAJO la ultima vez. No compres arriba."
  elif c<b<a: M5["bajadas_seguidas"]+=1; M5["subidas_seguidas"]=0; M5["ultima"]="Jefe M5: ORO bajo 3 velas seguidas "+str(a)+" -> "+str(b)+" -> "+str(c)+". Despues SUBIO la ultima vez. Preparate COMPRA."
  else: M5["ultima"]="Jefe M5: ORO en $"+str(c)+" mezclado. ESPERAR vela M5."
 m5_guardar(); return M5
def m5_recuerda(): return {"mensaje":"🧠 M5 - Me acuerdo de "+str(len(M5["velas"]))+" velas de 5 minutos","leccion":M5["ultima"],"velas":M5["velas"][-5:],"subidas":M5["subidas_seguidas"],"bajadas":M5["bajadas_seguidas"]}
m5_cargar()
FCAP="cerebro_capital.json"
CAP={"historial":[],"ultima":"Todavia no vi Capital.com jefe.","veces_caro":0,"veces_barato":0}
def cap_cargar():
 global CAP
 try:
  if os.path.exists(FCAP): CAP=json.load(open(FCAP))
 except: pass
def cap_guardar():
 try: json.dump(CAP,open(FCAP,"w"))
 except: pass
def capital_aprende(pc,pr):
 global CAP
 dif=round(pc-pr,2)
 if pc>=3970: CAP["veces_caro"]+=1; lec="Jefe Capital.com: ORO $"+str(pc)+" CARO, dif "+str(dif)+". No compres ahi."
 elif pc<=3910: CAP["veces_barato"]+=1; lec="Jefe Capital.com: ORO $"+str(pc)+" BARATO, dif "+str(dif)+". Ahi SI compras."
 else: lec="Jefe Capital.com: ORO $"+str(pc)+" en medio, dif "+str(dif)+". ESPERAR."
 CAP["ultima"]=lec; CAP["historial"].append({"hora":datetime.now().strftime("%H:%M:%S"),"capital":pc,"real":pr,"dif":dif,"leccion":lec}); CAP["historial"]=CAP["historial"][-20:]; cap_guardar(); return CAP
def capital_recuerda(): return {"mensaje":"🏦 Capital.com - Me acuerdo de "+str(len(CAP["historial"]))+" jugadas - CARO: "+str(CAP["veces_caro"])+" | BARATO: "+str(CAP["veces_barato"]),"leccion":CAP["ultima"],"historial":CAP["historial"][-5:]}
cap_cargar()
def get_capital_precio(pr):
 try:
  r=requests.get('https://api.gold-api.com/price/XAU',timeout=4); p=float(r.json().get('price',pr)); return {"precio":p,"spread":round(abs(p-pr),2),"fuente":"Capital.com espejo","recomendacion":"BARATO - Puedes comprar en Capital.com" if p<=3910 else ("CARO - No compres en Capital.com" if p>=3970 else "ESPERA en Capital.com")}
 except: return {"precio":pr,"spread":0.3,"fuente":"Capital.com espejo","recomendacion":"ESPERA en Capital.com"}
# ===== NUEVO - CEREBRO TRADING 212 =====
FT212="cerebro_t212.json"
T212={"historial":[],"ultima":"Todavia no vi Trading 212 jefe.","veces_caro":0,"veces_barato":0,"veces_espera":0}
def t212_cargar():
 global T212
 try:
  if os.path.exists(FT212): T212=json.load(open(FT212))
 except: pass
def t212_guardar():
 try: json.dump(T212,open(FT212,"w"))
 except: pass
def t212_aprende(pc,pr):
 global T212
 dif=round(pc-pr,2)
 if pc>=3970: T212["veces_caro"]+=1; lec="Jefe Trading 212: ORO $"+str(pc)+" CARO en Trading 212, dif "+str(dif)+". No compres en Trading 212, espera que baje a 3910."
 elif pc<=3910: T212["veces_barato"]+=1; lec="Jefe Trading 212: ORO $"+str(pc)+" BARATO en Trading 212, dif "+str(dif)+". En Trading 212 SI puedes comprar, esta en tu zona."
 else: T212["veces_espera"]+=1; lec="Jefe Trading 212: ORO $"+str(pc)+" en medio en Trading 212, dif "+str(dif)+". En Trading 212 mejor ESPERAR."
 T212["ultima"]=lec; T212["historial"].append({"hora":datetime.now().strftime("%H:%M:%S"),"t212":pc,"real":pr,"dif":dif,"leccion":lec}); T212["historial"]=T212["historial"][-20:]; t212_guardar(); return T212
def t212_recuerda(): return {"mensaje":"🟢 Trading 212 - Me acuerdo de "+str(len(T212["historial"]))+" jugadas - CARO: "+str(T212["veces_caro"])+" | BARATO: "+str(T212["veces_barato"])+" | ESPERA: "+str(T212["veces_espera"]),"leccion":T212["ultima"],"historial":T212["historial"][-5:]}
t212_cargar()
def get_t212_precio(pr):
 try:
  r=requests.get('https://query1.finance.yahoo.com/v8/finance/chart/GC=F',headers={'User-Agent':'Mozilla/5.0'},timeout=5); p=float(r.json()['chart']['result'][0]['meta']['regularMarketPrice']); return {"precio":p,"spread":round(abs(p-pr),2),"fuente":"Trading 212 espejo + Yahoo GC=F","recomendacion":"BARATO - Puedes comprar en Trading 212" if p<=3910 else ("CARO - No compres en Trading 212" if p>=3970 else "ESPERA en Trading 212")}
 except: return {"precio":pr,"spread":0.4,"fuente":"Trading 212 espejo","recomendacion":"ESPERA en Trading 212"}
# ===== CHAT LIBRE - LE ESCRIBES AL ROBOT COMO WHATSAPP =====
def chat_robot(mensaje, precio_actual=4088, precio_cap=4088, precio_t212=4088):
 m=mensaje.lower()
 nums=re.findall(r'\d+\.?\d*', mensaje)
 precio_q=float(nums[0]) if nums else 0
 m5l=M5["ultima"]; capl=CAP["ultima"]; t212l=T212["ultima"]
 if "hola" in m or "buenas" in m: return "Hola jefe 👑 Soy tu robot. Dime: ¿quieres comprar ORO a que precio? Ej: Quiero comprar a 3910. O dime: Tengo $20, cuanto gano?"
 if "trading 212" in m or "212" in m: return "🟢 Trading 212 jefe: ORO en $"+str(precio_t212)+". "+t212l+" | Capital.com en $"+str(precio_cap)+"."
 if "capital" in m: return "🏦 Capital.com jefe: ORO en $"+str(precio_cap)+". "+capl
 if "m5" in m or "5 minutos" in m: return "🧠 M5 jefe: "+m5l
 if "cuanto gano" in m or "gano" in m or "tengo $" in m or "tengo 20" in m:
  dinero=float(nums[0]) if nums else 20
  g=dinero*60/3910
  return "Jefe, si pones $"+str(dinero)+" en 3910 y sales en 3970, ganas $"+str(round(g,2))+" - Te quedan $"+str(round(dinero+g,2))+". Pon STOP en 3880 para perder max $"+str(round(dinero*0.25,2))+"."
 if "stop" in m: return "🛑 STOP LOSS jefe: Si entras en 3910, pon STOP en 3880. Si entras en 3970 venta, pon STOP en 4000. Asi no pierdes mucho. Usa la calculadora de STOP LOSS arriba."
 if "compro" in m or "comprar" in m or "compra" in m:
  if precio_q==0: return "Jefe, dime a que precio quieres comprar. Ej: Quiero comprar a 3910"
  if precio_q<=3910+30: return "✅ SI JEFE, COMPRA YA a $"+str(precio_q)+" esta BARATO. ORO ahora $"+str(precio_actual)+". En Trading 212 $"+str(precio_t212)+" y Capital.com $"+str(precio_cap)+". Pon STOP en "+str(int(precio_q-30))+"."
  if precio_q>=3970: return "❌ NO JEFE, a $"+str(precio_q)+" esta CARO. Espera a 3910. ORO ahora $"+str(precio_actual)+"."
  return "🟡 JEFE ESPERA. Quieres $"+str(precio_q)+" pero mejor espera a 3910. ORO ahora $"+str(precio_actual)+". M5 dice: "+m5l
 if "vendo" in m or "venta" in m or "vender" in m: return "Jefe, VENTA en 3970. Si ORO llega a 3970, vende. Pon STOP en 4000. Ahora esta en $"+str(precio_actual)+"."
 if "espero" in m or "esperar" in m or "hoy" in m: return "Jefe, hoy ORO en $"+str(precio_actual)+". Si esta entre 3910 y 3970, ESPERA. Si baja a 3910 COMPRA. Si sube a 3970 VENTA. M5: "+m5l
 if "ayuda" in m or "que hago" in m: return "Jefe, dime: 1) Quiero comprar a 3910 2) Tengo $20 cuanto gano 3) Trading 212 o Capital.com 4) Stop Loss. Yo te contesto."
 return "Jefe, te entendi: "+mensaje+". ORO ahora $"+str(precio_actual)+" | Trading 212 $"+str(precio_t212)+" | Capital.com $"+str(precio_cap)+". Dime: ¿Quieres comprar a que precio? Ej: Quiero comprar a 3910"
EV=[{"evento":"FED - Tasa USA","impacto":"ALTO","hora":"14:00 NY","efecto":"Si sube tasa, ORO BAJA"},{"evento":"NFP - Empleo USA","impacto":"ALTO","hora":"08:30 NY","efecto":"Si empleo fuerte, ORO BAJA"},{"evento":"CPI - Inflacion USA","impacto":"ALTO","hora":"08:30 NY","efecto":"Si inflacion alta, ORO SUBE"},{"evento":"BCE - Europa","impacto":"ALTO","hora":"08:15 NY","efecto":"Mueve EUR y ORO"},{"evento":"FOMC - Powell","impacto":"ALTO","hora":"14:30 NY","efecto":"Cada palabra mueve ORO $20-$50"},{"evento":"PIB USA","impacto":"ALTO","hora":"08:30 NY","efecto":"Mueve todo el mercado"}]
def bancos():
 b={"fed_tasa":"5.25% - FED","bce_tasa":"2.15% - BCE","fuente":"ForexFactory + FED + BCE","eventos_hoy":EV,"alerta_banco":"SIN NOTICIA FUERTE AHORA","nivel_riesgo":"VERDE"}
 try:
  r=requests.get('https://api.tradingeconomics.com/calendar?c=guest:guest&f=json&d1=today&d2=today',timeout=4)
  if r.status_code==200:
   d=r.json(); er=[]
   for e in d[:8]: er.append({"evento":e.get('Event','Evento'),"impacto":e.get('Importance','MEDIO'),"hora":e.get('Date','')[:16],"efecto":e.get('Country','USA')+" - "+e.get('Category','')})
   if er:
    b["eventos_hoy"]=er
    for ev in er:
     if str(ev.get("impacto")).upper() in ["HIGH","3","ALTO"]: b["alerta_banco"]="⚠️ ALERTA BANCO: "+ev["evento"]; b["nivel_riesgo"]="ROJO"; break
 except: pass
 return b
def yahoo(s,fb):
 try:
  r=requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{s}',headers={'User-Agent':'Mozilla/5.0'},timeout=5); return float(r.json()['chart']['result'][0]['meta']['regularMarketPrice'])
 except: return fb
def extra():
 dxy=yahoo('DX-Y.NYB',99.5); vix=yahoo('^VIX',15.2); btc=yahoo('BTC-USD',105000); pet=yahoo('CL=F',61.5); bono=yahoo('^TNX',4.1)
 vt="😱 PANICO TOTAL - VIX "+str(round(vix,2))+" - PAUSA" if vix>=30 else ("⚠️ MIEDO ALTO - VIX "+str(round(vix,2)) if vix>=20 else "😎 TRANQUILO - VIX "+str(round(vix,2)))
 vn="ROJO" if vix>=30 else ("AMARILLO" if vix>=20 else "VERDE")
 dt="💵 DOLAR FUERTE "+str(round(dxy,2))+" - ORO BAJA" if dxy>=101 else ("💵 DOLAR DEBIL "+str(round(dxy,2))+" - ORO SUBE" if dxy<=98 else "💵 DOLAR NEUTRAL "+str(round(dxy,2)))
 return {"DXY":dxy,"DXY_texto":dt,"DXY_para_oro":"BAJISTA" if dxy>=101 else ("ALCISTA" if dxy<=98 else "NEUTRAL"),"VIX":vix,"VIX_texto":vt,"VIX_nivel":vn,"BTC":btc,"PETROLEO":pet,"BONO10":bono,"fuente":"Yahoo Finance USA","resumen_jefe":dt+" | "+vt}
EP=[{"evento":"Presidente USA - Habla Economia","impacto":"ALTO","efecto":"Si habla aranceles, ORO SUBE"},{"evento":"Casa Blanca - Arancel","impacto":"ALTO","efecto":"Arancel nuevo = ORO $30-$80"},{"evento":"Presidente - Reunion FED","impacto":"ALTO","efecto":"Si presiona FED, ORO SUBE"},{"evento":"Elecciones","impacto":"ALTO","efecto":"Incertidumbre = ORO SUBE"}]
def presi():
 a={"nivel":"VERDE","mensaje":"🟢 SIN CAMBIO PRESIDENCIAL","accion_jefe":"Puedes operar normal","eventos":EP,"fuente":"whitehouse.gov"}
 try:
  r=requests.get('https://api.tradingeconomics.com/calendar?c=guest:guest&f=json&d1=today&d2=today',timeout=4)
  if r.status_code==200:
   for e in r.json():
    t=(str(e.get('Event',''))+" "+str(e.get('Category',''))).lower()
    if any(p in t for p in ["president","white house","election","tariff","government","treasury","speech"]): a["nivel"]="ROJO"; a["mensaje"]="🚨 ALERTA PRESIDENTE: "+e.get('Event','Cambio')+" - PAUSA 1 HORA"; a["accion_jefe"]="NO COMPRES AHORA"; break
 except: pass
 return a
ZONAS={"ORO":{"compra":3910,"venta":3970,"soporte":3940},"NVDA":{"compra":180,"venta":195,"soporte":180},"AAPL":{"compra":255,"venta":270,"soporte":255},"TSLA":{"compra":330,"venta":355,"soporte":330},"MSFT":{"compra":490,"venta":505,"soporte":490},"AMZN":{"compra":230,"venta":245,"soporte":230},"META":{"compra":640,"venta":660,"soporte":640},"GOOGL":{"compra":280,"venta":292,"soporte":280}}
def pregunta(pq,act="ORO",pa=4088):
 pq=float(pq); z=ZONAS.get(act,ZONAS["ORO"]); pr=presi(); mem=crec(); ex=" | 🧠 "+mem["leccion"]
 if pr["nivel"]=="ROJO": return {"respuesta":"🛑 NO COMPRES - "+pr["mensaje"]+ex,"decision":"ESPERA-PRESIDENTE","precio_recomendado":z["soporte"],"precio_actual":pa}
 if pq>z["venta"] and pq>pa: return {"respuesta":"❌ NO JEFE, "+act+" a $"+str(pq)+" esta CARO. Ahora $"+str(pa)+" va a BAJAR a $"+str(z["soporte"])+ex,"decision":"NO-COMPRAR","precio_recomendado":z["soporte"],"precio_actual":pa}
 if pq<=z["compra"]+30: return {"respuesta":"✅ SI JEFE, COMPRA YA "+act+" a $"+str(pq)+" BARATO"+ex,"decision":"SI-COMPRAR","precio_recomendado":pq,"precio_actual":pa}
 return {"respuesta":"🟡 ESPERA. Quieres $"+str(pq)+" pero esta en $"+str(pa)+". Espera a $"+str(z["soporte"])+ex,"decision":"ESPERA","precio_recomendado":z["soporte"],"precio_actual":pa}
EQUIPO={40:{"nombre":"MAESTRO DIOS RAUDY - JEFE","rol":"JEFE","tarea":"Yo mando a los 39."},1:{"nombre":"RAYO RAUDY","rol":"TRABAJADOR","tarea":"Noticias USA"},2:{"nombre":"RAYO VELOZ","rol":"TRABAJADOR","tarea":"NVDA y TESLA"},3:{"nombre":"COMETA ORO","rol":"TRABAJADOR","tarea":"Noticias ORO"},4:{"nombre":"GUARDIA 08:30","rol":"VIGIA","tarea":"Vigila 
