from flask import Flask, jsonify, request
import requests, json, os
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
# ============ NUEVO - CEREBRO M5 + CEREBRO CAPITAL.COM ============
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
 M5["velas"].append({"hora":datetime.now().strftime("%H:%M:%S"),"precio":precio})
 M5["velas"]=M5["velas"][-20:]
 if len(M5["velas"])>=3:
  a=M5["velas"][-3]["precio"]; b=M5["velas"][-2]["precio"]; c=M5["velas"][-1]["precio"]
  if c>b>a:
   M5["subidas_seguidas"]+=1; M5["bajadas_seguidas"]=0
   M5["ultima"]="Jefe M5: ORO subio 3 velas seguidas "+str(a)+" -> "+str(b)+" -> "+str(c)+". La ultima vez que paso, despues BAJO. Cuidado, no compres arriba."
  elif c<b<a:
   M5["bajadas_seguidas"]+=1; M5["subidas_seguidas"]=0
   M5["ultima"]="Jefe M5: ORO bajo 3 velas seguidas "+str(a)+" -> "+str(b)+" -> "+str(c)+". La ultima vez que paso, despues SUBIO. Preparate para COMPRA."
  else:
   M5["ultima"]="Jefe M5: ORO en $"+str(c)+" mezclado, no hay 3 seguidas. Mejor ESPERAR la vela M5."
 m5_guardar(); return M5
def m5_recuerda():
 return {"mensaje":"🧠 M5 - Me acuerdo de "+str(len(M5["velas"]))+" velas de 5 minutos","leccion":M5["ultima"],"velas":M5["velas"][-5:],"subidas":M5["subidas_seguidas"],"bajadas":M5["bajadas_seguidas"]}
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
def capital_aprende(precio_cap, precio_real):
 global CAP
 dif=round(precio_cap-precio_real,2)
 if precio_cap>=3970:
  CAP["veces_caro"]+=1; lec="Jefe Capital.com: ORO en $"+str(precio_cap)+" CARO en Capital.com, diferencia "+str(dif)+". En Capital.com esta mas caro, no compres ahi, espera."
 elif precio_cap<=3910:
  CAP["veces_barato"]+=1; lec="Jefe Capital.com: ORO en $"+str(precio_cap)+" BARATO en Capital.com, diferencia "+str(dif)+". En Capital.com esta barato, ahi SI puedes comprar."
 else:
  lec="Jefe Capital.com: ORO en $"+str(precio_cap)+" en medio en Capital.com, diferencia "+str(dif)+". Mejor ESPERAR."
 CAP["ultima"]=lec; CAP["historial"].append({"hora":datetime.now().strftime("%H:%M:%S"),"capital":precio_cap,"real":precio_real,"dif":dif,"leccion":lec}); CAP["historial"]=CAP["historial"][-20:]; cap_guardar(); return CAP
def capital_recuerda():
 return {"mensaje":"🏦 Capital.com - Me acuerdo de "+str(len(CAP["historial"]))+" jugadas - CARO: "+str(CAP["veces_caro"])+" | BARATO: "+str(CAP["veces_barato"]),"leccion":CAP["ultima"],"historial":CAP["historial"][-5:]}
cap_cargar()
def get_capital_precio(precio_real):
 try:
  r=requests.get('https://api.gold-api.com/price/XAU',timeout=4)
  p=float(r.json().get('price',precio_real))
  return {"precio":p,"spread":round(abs(p-precio_real),2),"fuente":"Capital.com espejo + gold-api","recomendacion":"BARATO - Puedes comprar en Capital.com" if p<=3910 else ("CARO - No compres en Capital.com" if p>=3970 else "ESPERA en Capital.com")}
 except: return {"precio":precio_real,"spread":0.3,"fuente":"Capital.com espejo","recomendacion":"ESPERA en Capital.com"}
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
EQUIPO={40:{"nombre":"MAESTRO DIOS RAUDY - JEFE","rol":"JEFE","tarea":"Yo mando a los 39."},1:{"nombre":"RAYO RAUDY","rol":"TRABAJADOR","tarea":"Noticias USA"},2:{"nombre":"RAYO VELOZ","rol":"TRABAJADOR","tarea":"NVDA y TESLA"},3:{"nombre":"COMETA ORO","rol":"TRABAJADOR","tarea":"Noticias ORO"},4:{"nombre":"GUARDIA 08:30","rol":"VIGIA","tarea":"Vigila 08:30"},5:{"nombre":"COMETA VENTA","rol":"TRABAJADOR","tarea":"Ventas fuertes"},6:{"nombre":"COMETA FUERTE","rol":"TRABAJADOR","tarea":"Caidas rapidas"},7:{"nombre":"COMETA DIOS","rol":"TRABAJADOR","tarea":"Venta grande"},8:{"nombre":"RAYO COMPRA","rol":"TRABAJADOR","tarea":"Compras rapidas"},9:{"nombre":"RAYO ORO","rol":"TRABAJADOR","tarea":"ORO segundo a segundo"},10:{"nombre":"HIELO PACIENTE","rol":"TRABAJADOR","tarea":"Espera frio"},11:{"nombre":"HIELO ANALISTA","rol":"TRABAJADOR","tarea":"Mercado tranquilo"},12:{"nombre":"FUEGO COMPRA","rol":"TRABAJADOR","tarea":"Compra fuerte"},13:{"nombre":"FUEGO TESLA","rol":"TRABAJADOR","tarea":"Solo TESLA"},14:{"nombre":"FUEGO NVDA","rol":"TRABAJADOR","tarea":"Solo NVDA"},15:{"nombre":"FUEGO APPLE","rol":"TRABAJADOR","tarea":"Solo APPLE"},16:{"nombre":"FUEGO ORO","rol":"TRABAJADOR","tarea":"ORO con fuego"},17:{"nombre":"FUEGO VENTA","rol":"TRABAJADOR","tarea":"VENTA fuego rojo"},18:{"nombre":"RAYO META","rol":"TRABAJADOR","tarea":"META y GOOGLE"},19:{"nombre":"RAYO AMAZON","rol":"TRABAJADOR","tarea":"AMAZON"},20:{"nombre":"HIELO JEFE","rol":"TRABAJADOR","tarea":"ESPERA peligro"},21:{"nombre":"COMETA AMAZON","rol":"TRABAJADOR","tarea":"Noticias AMAZON"},22:{"nombre":"COMETA MICROSOFT","rol":"TRABAJADOR","tarea":"Noticias MSFT"},23:{"nombre":"RAYO NOTICIAS","rol":"TRABAJADOR","tarea":"Telegram y WhatsApp"},24:{"nombre":"HIELO SOPORTE","rol":"TRABAJADOR","tarea":"Soportes"},25:{"nombre":"FUEGO RESISTENCIA","rol":"TRABAJADOR","tarea":"Resistencias"},26:{"nombre":"COMETA 14:30","rol":"VIGIA","tarea":"Vigila 14:30 FED"},27:{"nombre":"RAYO ENTRADA","rol":"TRABAJADOR","tarea":"Mejor ENTRADA"},28:{"nombre":"FUEGO BOTIN","rol":"TRABAJADOR","tarea":"Calcula BOTIN"},29:{"nombre":"HIELO SALIDA","rol":"TRABAJADOR","tarea":"Cuando SALIR"},30:{"nombre":"COMETA PELIGRO","rol":"VIGIA","tarea":"Grita PELIGRO"},31:{"nombre":"RAYO VIP","rol":"TRABAJADOR","tarea":"Solo VIP"},32:{"nombre":"FUEGO DIOS","rol":"TRABAJADOR","tarea":"Fuego DIOS"},33:{"nombre":"HIELO DIOS","rol":"TRABAJADOR","tarea":"Hielo DIOS"},34:{"nombre":"COMETA ORO 2","rol":"TRABAJADOR","tarea":"Confirma ORO"},35:{"nombre":"RAYO CONFIRMA","rol":"TRABAJADOR","tarea":"Confirma COMPRA/VENTA"},36:{"nombre":"FUEGO CONFIRMA","rol":"TRABAJADOR","tarea":"Confirma fuego"},37:{"nombre":"HIELO CONFIRMA","rol":"TRABAJADOR","tarea":"Confirma calma"},38:{"nombre":"COMETA JEFE","rol":"TRABAJADOR","tarea":"Jefe cometas"},39:{"nombre":"RAYO MAESTRO 2","rol":"TRABAJADOR","tarea":"Mano derecha Maestro"}}
def jefe(b,d,ex=None):
 if ex and ex.get("VIX_nivel")=="ROJO": return {"orden":"🛑 PAUSA TOTAL - PANICO","motivo":ex["VIX_texto"],"permiso_operar":False,"mensaje":"JEFE DICE: VIX "+str(ex["VIX"])+" PANICO. Todos PARADOS."}
 if b["nivel_riesgo"]=="ROJO": return {"orden":"🛑 PAUSA TOTAL - BANCO","motivo":b["alerta_banco"],"permiso_operar":False,"mensaje":"JEFE DICE: Noticia BANCO FUERTE. Todos PARADOS."}
 if d["ORO"]>3910 and d["ORO"]<3970: return {"orden":"🟡 ESPERA - ORDEN JEFE","motivo":"Oro fuera de zona","permiso_operar":False,"mensaje":"JEFE DICE: Oro $"+str(d["ORO"])+" fuera de zona. Buscando."}
 return {"orden":"🟢 PERMISO PARA OPERAR","motivo":"Bancos tranquilos + Oro en zona","permiso_operar":True,"mensaje":"JEFE DICE: Bancos tranquilos, Oro en zona. Listos."}
def motor(p,s):
 if s=="ORO":
  if p<=3910 or p>=3970: return "🔥🔥🔥🔥🔥 FUERZA 200% - DIOS - SATELITE"
  if p<=3940: return "🔥🔥🔥 FUERZA 150% - SATELITE"
  return "🔥🔥 FUERZA 100%"
 return "💪 MOTOR 200% VIGILANDO "+s
def buscador(d):
 e=[]
 if d["ORO"]<=3910: e.append("🟢 ORO COMPRA "+str(d["ORO"]))
 if d["ORO"]>=3970: e.append("🔴 ORO VENTA "+str(d["ORO"]))
 if d["NVDA"]<=180: e.append("🟢 NVDA COMPRA "+str(d["NVDA"]))
 if d["TSLA"]<=330: e.append("🟢 TESLA COMPRA "+str(d["TSLA"]))
 if d["AAPL"]<=255: e.append("🟢 APPLE COMPRA "+str(d["AAPL"]))
 return "🔍 BUSCADOR: Nada en zona, ESPERA" if not e else "🔍 ENCONTRO: "+" | ".join(e)
def conectar(d):
 r={}
 for s,p in d.items():
  if s in ZONAS:
   z=ZONAS[s]; sen="COMPRA" if p<=z["compra"] else ("VENTA" if p>=z["venta"] else "ESPERA"); r[s]={"senal":sen,"precio":p,"fuente":"Yahoo USA"}
 return r
HTML="""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RAUDY VIP</title><style>*{box-sizing:border-box;font-family:Arial}body{margin:0;background:#050505;color:white;text-align:center}header{background:linear-gradient(90deg,#FFD700,#FF6B00,#FFD700);color:black;padding:15px}header h1{margin:0;font-size:22px}.top-btns{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px;background:#111}.top-btns a{padding:12px 16px;border-radius:25px;text-decoration:none;font-weight:bold;color:white;font-size:14px}.wa{background:#25D366}.tg{background:#0088cc}.ig{background:#E1306C}.pay{background:#FFD700;color:black!important}.box{margin:10px;padding:15px;border-radius:15px}.cerebro{background:#1a0033;border:3px solid #CC00FF}.m5{background:#003300;border:3px solid #00FF88}.capital{background:#000033;border:3px solid #00FFFF}.presi{background:#2a0000;border:3px solid #FF4444}.preg{background:#0a2a00;border:3px solid #00FF88}.calc{background:#1a1a00;border:3px solid #FFD700}.sl{background:#2a0000;border:3px solid #FF4444}.jefe{background:#2a0000;border:3px solid #FF0000}.banco{background:#1a1a00;border:2px solid #FFD700;text-align:left}.extra{background:#001a33;border:2px solid #00FFFF;text-align:left}.sat{background:#001a33;border:2px solid #00FFFF}.motor{background:#2a0000;border:2px solid #FF0000}.busc{background:#0a2a00;border:2px solid #00FF88}.conect{background:#002a00;border:2px solid #00FF88}.maestro{background:linear-gradient(180deg,#FFD700,#FF6B00);color:black;margin:10px;padding:18px;border-radius:20px;border:4px solid white}.broker{background:#1a1a2e;margin:10px;padding:15px;border-radius:15px;border:2px solid #00FFFF}.broker img{width:90px;height:90px;border-radius:50%;border:3px solid #00FFFF}.acciones{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:10px}.act{background:#1a1a1a;border:1px solid #333;padding:10px;border-radius:12px;min-width:130px;cursor:pointer}.act.active{border:2px solid #FFD700}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}.robot{background:#1a1a1a;border:2px solid #333;border-radius:15px;padding:10px}.luz{width:18px;height:18px;border-radius:50%;background:yellow;margin:0 auto 5px}input,select{width:100%;padding:12px;border-radius:10px;background:#111;color:white;font-size:16px;border:1px solid #00FF88;margin:4px 0}button{width:100%;padding:14px;border-radius:15px;font-weight:bold;font-size:16px;border:none;margin-top:5px;cursor:pointer}.clock{background:#111;padding:10px;border:2px solid #FFD700;margin:10px;border-radius:15px}.footer{padding:20px;font-size:12px;color:#888}</style></head><body><header><h1>👑 RAUDY VIP ROBOTS PODEROSOS ⚡☄️</h1><p>ACCIONES + ORO • JEFE: RAUDY MANZUETA</p></header><div class="top-btns"><a class="wa" href="https://wa.me/41767574050">💬 WHATSAPP</a><a class="tg" href="https://t.me/raudy_vip_oro_bot">✈️ TELEGRAM</a><a class="ig" href="https://instagram.com/raudy_vip_oro_bot">📸 INSTAGRAM</a><a class="pay" href="https://paypal.me/RaudyManzueta/20">💰 PAGAR VIP $20</a></div><div class="box cerebro"><h2>🧠 CEREBRO CON MEMORIA</h2><p id="cerebro-mensaje">🧠 Despertando...</p><p id="cerebro-leccion" style="color:#FFD700"></p></div><div class="box m5"><h2>🧠 CEREBRO M5 - VELAS 5 MINUTOS</h2><p id="m5-mensaje">🧠 M5 despertando...</p><p id="m5-leccion" style="color:#00FF88;font-weight:bold"></p><p id="m5-velas" style="font-size:12px"></p><p style="font-size:11px;color:#aaa">Si sube 3 velas M5 seguidas, despues BAJA. Si baja 3 velas M5 seguidas, despues SUBE. Asi te acuerdas jefe.</p></div><div class="box capital"><h2>🏦 CEREBRO CAPITAL.COM</h2><p id="capital-mensaje">🏦 Capital.com despertando...</p><p id="capital-leccion" style="color:#00FFFF;font-weight:bold"></p><p id="capital-precio" style="font-weight:bold"></p><p style="font-size:11px;color:#aaa">Te dice si en Capital.com esta CARO o BARATO. Si esta BARATO ahi si compras en Capital.com.</p></div><div class="box presi"><h2>🇺🇸 ALERTA PRESIDENTE</h2><p id="presidente-mensaje">Vigilando Casa Blanca...</p><p id="presidente-accion"></p></div><div class="box preg"><h2>🤖 PREGUNTALE AL ROBOT</h2><input id="precio-pregunta" type="number" placeholder="Ej: 4070"><button onclick="preguntarRobot()" style="background:#00FF88">🤖 PREGUNTAR</button><p id="respuesta-robot" style="background:#111;padding:12px;border-radius:10px">🤖 Esperando...</p></div><div class="box calc"><h2>🧮 CALCULADORA DINERO</h2><input id="calc-dinero" type="number" value="20"><input id="calc-entrada" type="number" value="3910"><input id="calc-salida" type="number" value="3970"><button onclick="calcularDinero()" style="background:#FFD700">🧮 CALCULAR CUANTO GANO</button><p id="calc-resultado" style="background:#111;padding:12px;border-radius:10px">🧮 Pon tu dinero</p></div><div class="box sl"><h2>🛑 STOP LOSS - FRENO EMERGENCIA</h2><p>Ejemplo: $20, perder max $5</p><input id="sl-dinero" type="number" value="20"><input id="sl-riesgo" type="number" value="5"><input id="sl-entrada" type="number" value="3910"><input id="sl-salida" type="number" value="3970"><select id="sl-ratio"><option value="2">Ganar DOBLE - 1 a 2 - SEGURO</option><option value="3">Ganar TRIPLE - 1 a 3</option></select><button onclick="calcularStopLoss()" style="background:#FF4444;color:white">🛑 CALCULAR MI STOP LOSS</button><p id="sl-resultado" style="background:#111;padding:12px;border-radius:10px;line-height:1.6">🛑 Pon $20, perder $5, 3910, 3970</p><button onclick="copiarStopLoss()" style="background:#00FF88">📋 COPIAR PARA VIP</button></div><div class="box jefe"><h2>👑 JEFE 40 - ORDEN EN VIVO</h2><p id="jefe-orden">Cargando...</p><p id="jefe-mensaje"></p></div><div class="box banco"><h2>🏦 BANCOS QUE MUEVEN ORO</h2><p id="banco-alerta">Cargando...</p><p id="banco-lista"></p></div><div class="box extra"><h2>💵 DOLAR + MIEDO + BTC</h2><p id="dxy-texto">Cargando...</p><p id="vix-texto"></p><p id="extra-texto"></p></div><div class="box sat"><h2>🛰️ SATELITE RAUDY - USA 🇺🇸</h2><p id="satelite-texto">Conectando...</p><p id="satelite-usa"></p></div><div class="box conect"><h2>🔌 40 ROBOTS CONECTADOS ✅</h2><p id="conexion-texto">Conectando...</p></div><div class="box motor"><h2>💪 MOTOR FUERZA 200%</h2><p id="motor-texto">Cargando...</p></div><div class="box busc"><h2>🔍 BUSCADOR - NADA SE ESCAPA</h2><p id="buscador-texto">Buscando...</p></div><div class="clock">SESION NEW YORK 🕐 <b id="reloj">--:--:--</b><br><span id="sesion"></span></div><div class="acciones" id="acciones"></div><div class="maestro"><div style="font-size:40px">👑⚡☄️🔥🧊</div><h2>ROBOT 40 - MAESTRO DIOS RAUDY</h2><p id="maestroMsg">Analizando...</p><p>⭐ <span id="maestroEstrellas">⭐⭐⭐⭐⭐</span></p><button onclick="felicitarMaestro()" style="background:black;color:#FFD700">👏 FELICITAR MAESTRO</button><button onclick="estrellaMaestro()" style="background:black;color:#FFD700">⭐ ESTRELLA</button></div><div class="broker"><img src="https://i.pravatar.cc/150?img=12"><h3>🧑‍💼 BROKER RAUDY</h3><p id="brokerMsg">Hola jefe, soy tu Broker...</p><button onclick="hablarBroker()" style="background:#00FFFF">🎤 PREGUNTAR AL BROKER</button></div><h2>🤖 LOS 40 ROBOTS</h2><div class="grid" id="grid"></div><div style="background:#111;margin:10px;padding:15px;border-radius:15px;text-align:left"><h3>📍 ORIGEN PRECIOS</h3><p id="origen-precios">Cargando...</p></div><div class="footer">RAUDY VIP © 2026 - WhatsApp 0767574050 - No es consejo financiero, es educacion</div><script>
const simbolos=[{id:"ORO",nombre:"ORO",precio:4088,emoji:"🥇"},{id:"NVDA",nombre:"NVIDIA",precio:185.2,emoji:"💚"},{id:"AAPL",nombre:"APPLE",precio:262.1,emoji:"🍎"},{id:"TSLA",nombre:"TESLA",precio:340.5,emoji:"🚗"},{id:"MSFT",nombre:"MICROSOFT",precio:495.3,emoji:"🪟"},{id:"AMZN",nombre:"AMAZON",precio:235.4,emoji:"📦"},{id:"META",nombre:"META",precio:645.2,emoji:"👍"},{id:"GOOGL",nombre:"GOOGLE",precio:282.1,emoji:"🔍"}];
let activo="ORO",datosRealesGlobal=null,datosStopLoss="";
function renderAcc(){let a=document.getElementById("acciones");a.innerHTML="";simbolos.forEach(s=>{let c=(Math.random()*4-2).toFixed(2);let d=document.createElement("div");d.className="act "+(activo===s.id?"active":"");d.innerHTML="<b>"+s.emoji+" "+s.id+"</b><br>"+s.nombre+"<br><b>$"+s.precio.toFixed(2)+"</b><br>"+c+"%";d.onclick=()=>{activo=s.id;renderAcc();analizarTodo();sonido()};a.appendChild(d)})}renderAcc();
const robots=[[1,"RAYO RAUDY","⚡","Noticias USA"],[2,"RAYO VELOZ","⚡","NVDA y TESLA"],[3,"COMETA ORO","☄️","Noticias ORO"],[4,"GUARDIA 08:30","🔥","Vigila 08:30"],[5,"COMETA VENTA","☄️","Ventas fuertes"],[6,"COMETA FUERTE","☄️","Caidas rapidas"],[7,"COMETA DIOS","☄️","Venta grande"],[8,"RAYO COMPRA","⚡","Compras rapidas"],[9,"RAYO ORO","⚡","ORO segundo a segundo"],[10,"HIELO PACIENTE","🧊","Espera frio"],[11,"HIELO ANALISTA","🧊","Mercado tranquilo"],[12,"FUEGO COMPRA","🔥","Compra fuerte"],[13,"FUEGO TESLA","🔥","Solo TESLA"],[14,"FUEGO NVDA","🔥","Solo NVDA"],[15,"FUEGO APPLE","🔥","Solo APPLE"],[16,"FUEGO ORO","🔥","ORO con fuego"],[17,"FUEGO VENTA","🔥","VENTA fuego rojo"],[18,"RAYO META","⚡","META y GOOGLE"],[19,"RAYO AMAZON","⚡","AMAZON"],[20,"HIELO JEFE","🧊","ESPERA peligro"],[21,"COMETA AMAZON","☄️","Noticias AMAZON"],[22,"COMETA MICROSOFT","☄️","Noticias MSFT"],[23,"RAYO NOTICIAS","⚡","Telegram y WhatsApp"],[24,"HIELO SOPORTE","🧊","Soportes"],[25,"FUEGO RESISTENCIA","🔥","Resistencias"],[26,"COMETA 14:30","☄️","Vigila 14:30 FED"],[27,"RAYO ENTRADA","⚡","Mejor ENTRADA"],[28,"FUEGO BOTIN","🔥","Calcula BOTIN"],[29,"HIELO SALIDA","🧊","Cuando SALIR"],[30,"COMETA PELIGRO","☄️","Grita PELIGRO"],[31,"RAYO VIP","⚡","Solo VIP"],[32,"FUEGO DIOS","🔥","Fuego DIOS"],[33,"HIELO DIOS","🧊","Hielo DIOS"],[34,"COMETA ORO 2","☄️","Confirma ORO"],[35,"RAYO CONFIRMA","⚡","Confirma COMPRA/VENTA"],[36,"FUEGO CONFIRMA","🔥","Confirma fuego"],[37,"HIELO CONFIRMA","🧊","Confirma calma"],[38,"COMETA JEFE","☄️","Jefe cometas"],[39,"RAYO MAESTRO 2","⚡","Mano derecha Maestro"],[40,"MAESTRO DIOS RAUDY","👑","Yo mando a todos"]];
let estrellas={};const grid=document.getElementById("grid");
robots.slice(0,39).forEach(r=>{let n=r[0];estrellas[n]=0;let d=document.createElement("div");d.className="robot";d.innerHTML="<div class='luz' id='luz"+n+"'></div><div>"+r[2]+"</div><h3>Robot "+n+" - "+r[1]+"</h3><p>"+r[3]+"</p><div id='msg"+n+"'>Buscando...</div><div id='est"+n+"'></div><button onclick='felicitar("+n+")' style='background:#00FF88'>👏 FELICITAR</button><button onclick='darEstrella("+n+")' style='background:#FFD700'>⭐ ESTRELLA</button>";grid.appendChild(d)});
function sonido(){try{let c=new(window.AudioContext||window.webkitAudioContext)();let o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);o.frequency.value=880;g.gain.value=0.1;o.start();o.stop(c.currentTime+0.15)}catch(e){}}
function hablar(t){if('speechSynthesis' in window){let u=new SpeechSynthesisUtterance(t);u.lang='es-ES';speechSynthesis.speak(u)}}
function felicitar(n){sonido();document.getElementById("msg"+n).innerHTML="¡Gracias jefe! 👏";hablar("Gracias jefe")}
function darEstrella(n){sonido();estrellas[n]++;document.getElementById("est"+n).innerHTML="⭐".repeat(estrellas[n]);document.getElementById("msg"+n).innerHTML="¡Estrella! ¡Gracias jefe! ⭐";hablar("Gracias jefe estrella")}
let mc=5;
function felicitarMaestro(){sonido();document.getElementById("maestroMsg").innerHTML="¡Gracias jefe! ¡Eres el mejor! 👑";hablar("Gracias jefe")}
function estrellaMaestro(){sonido();mc++;document.getElementById("maestroEstrellas").innerHTML="⭐".repeat(mc);document.getElementById("maestroMsg").innerHTML="¡ESTRELLA! ¡Mas poder! ⭐"}
function hablarBroker(){sonido();let m=["Jefe, Maestro dice espera, ORO en zona caliente.","Jefe, robots dicen COMPRA NVDA con cuidado.","Jefe, no entres sin confirmacion del Maestro.","Jefe, hoy fuerza en TESLA."];let x=m[Math.floor(Math.random()*m.length)];document.getElementById("brokerMsg").innerHTML=x;hablar(x)}
function calcularDinero(){let d=parseFloat(document.getElementById("calc-dinero").value||0),e=parseFloat(document.getElementById("calc-entrada").value||3910),s=parseFloat(document.getElementById("calc-salida").value||3970);if(!d){document.getElementById("calc-resultado").innerHTML="🧮 Escribe tu dinero";return}let dif=Math.abs(s-e),pct=dif/e*100,g=d*pct/100;document.getElementById("calc-resultado").innerHTML="💰 Pones $"+d+" en $"+e+" sales $"+s+" ganas $"+g.toFixed(2)+" Total $"+(d+g).toFixed(2)+" - "+pct.toFixed(2)+"%";hablar("Ganas "+g.toFixed(0)+" dolares")}
function calcularStopLoss(){let d=parseFloat(document.getElementById("sl-dinero").value||20),r=parseFloat(document.getElementById("sl-riesgo").value||5),e=parseFloat(document.getElementById("sl-entrada").value||3910),s=parseFloat(document.getElementById("sl-salida").value||3970),ra=parseFloat(document.getElementById("sl-ratio").value||2);if(!d||!r){document.getElementById("sl-resultado").innerHTML="🛑 Escribe dinero y perdida";return}if(r>=d){document.getElementById("sl-resultado").innerHTML="❌ CUIDADO: Quieres perder $"+r+" con $"+d+". Pon menos, $2 o $1.";return}let dg=Math.abs(s-e),dp=dg/ra,stop=e-dp,g=r*ra;document.getElementById("sl-resultado").innerHTML="✅ JUGADA LISTA:<br>🟢 ENTRADA $"+e+"<br>🛑 STOP LOSS $"+stop.toFixed(0)+" - Si baja ahi pierdes solo $"+r+" Te quedan $"+(d-r)+"<br>🎯 BOTIN $"+s+" - Si sube ganas $"+g+" Te quedan $"+(d+g)+"<br>⚖️ 1 a "+ra+" - Arriesgas $"+r+" para ganar $"+g;datosStopLoss="👑 VIP RAUDY - ORO COMPRA $"+e+" | STOP $"+stop.toFixed(0)+" | BOTIN $"+s+" | Riesgo $"+r+" gana $"+g;hablar("Tu stop es "+stop.toFixed(0)+" ganas "+g+" dolares")}
function copiarStopLoss(){if(!datosStopLoss){alert("Primero CALCULAR STOP LOSS");return}if(navigator.clipboard)navigator.clipboard.writeText(datosStopLoss).then(()=>alert("✅ COPIADO: "+datosStopLoss));else alert(datosStopLoss)}
async function preguntarRobot(){let p=document.getElementById("precio-pregunta").value;if(!p){document.getElementById("respuesta-robot").innerHTML="🤖 Escribe precio Ej 4070";return}document.getElementById("respuesta-robot").innerHTML="🤖 Pensando...";try{let r=await fetch('/api/preguntale?precio='+p+'&activo='+activo);let d=await r.json();document.getElementById("respuesta-robot").innerHTML="🤖 "+d.respuesta+"<br>Actual $"+d.precio_actual+" | Recomiendo $"+d.precio_recomendado;hablar(d.respuesta)}catch(e){document.getElementById("respuesta-robot").innerHTML="🤖 Error"}}
async function analizarTodo(){sonido();let datos=datosRealesGlobal;if(!datos){try{let r=await fetch('/api/satelite_usa?v='+Date.now());datos=await r.json();datosRealesGlobal=datos}catch(e){datos=null}}let pr=datos&&datos[activo]?datos[activo]:simbolos.find(s=>s.id===activo).precio;let sen="ESPERA 🟡",c=false,v=false;let z=ZONAS[activo]||ZONAS["ORO"];if(pr<=z.compra){sen="COMPRA DIOS 🟢";c=true}else if(pr>=z.venta){sen="VENTA DIOS 🔴";v=true}let ent=pr.toFixed(2),bot=ent,sal=ent;if(c){bot=(pr*1.02).toFixed(2);sal=(pr*0.99).toFixed(2)}else if(v){bot=(pr*0.98).toFixed(2);sal=(pr*1.01).toFixed(2)}let org=activo==="ORO"?"gold-api + Yahoo GC=F":"Yahoo USA";let oj=datos&&datos.jefe?datos.jefe.orden:"";document.getElementById("maestroMsg").innerHTML="Analice "+activo+" PRECIO REAL. Decision: <b>"+sen+"</b><br>ENTRADA $"+ent+" | BOTIN $"+bot+" | SALIDA $"+sal+"<br>Fuente: "+org+" | "+oj;hablar("Analice "+activo+" decision "+sen);robots.slice(0,39).forEach(r=>{let n=r[0],el=document.getElementById("msg"+n),luz=document.getElementById("luz"+n);if(!el)return;el.innerHTML="🔌 "+r[3]+" - "+activo+" $"+ent+" - "+sen;let col=c?"#00FF88":(v?"#FF4444":"#FFD700");luz.style.background=col});document.getElementById("brokerMsg").innerHTML="Jefe, "+activo+" "+sen+". ENTRADA $"+ent+", BOTIN $"+bot+". Fuente: "+org;document.getElementById("conexion-texto").innerHTML="🔌 40/40 CONECTADOS ✅ - "+activo+" $"+ent}
async function actualizarSateliteUSA(){try{let r=await fetch('/api/satelite_usa?v='+Date.now());let d=await r.json();datosRealesGlobal=d;document.getElementById("satelite-texto").innerHTML="🛰️ SATELITE USA ✅ - NYSE: "+d.nyse+" | NASDAQ: "+d.nasdaq;document.getElementById("satelite-usa").innerHTML="🇺🇸 ORO $"+d.ORO+" | NVDA $"+d.NVDA+" | TESLA $"+d.TSLA+" | APPLE $"+d.AAPL;document.getElementById("motor-texto").innerHTML="💪 "+d.motor+" | "+d.velocidad;document.getElementById("buscador-texto").innerHTML=d.buscador;document.getElementById("conexion-texto").innerHTML="🔌 40/40 ✅ - ORO $"+d.ORO;if(d.jefe){document.getElementById("jefe-orden").innerHTML=d.jefe.orden;document.getElementById("jefe-mensaje").innerHTML=d.jefe.mensaje}if(d.bancos){document.getElementById("banco-alerta").innerHTML="🏦 "+d.bancos.alerta_banco+" | Riesgo: "+d.bancos.nivel_riesgo;document.getElementById("banco-lista").innerHTML=d.bancos.eventos_hoy.map(e=>"🏦 <b>"+e.evento+"</b> - "+e.impacto+" - "+e.efecto).join("<br>")}if(d.extra){document.getElementById("dxy-texto").innerHTML="💵 "+d.extra.DXY_texto;document.getElementById("vix-texto").innerHTML="😱 "+d.extra.VIX_texto;document.getElementById("extra-texto").innerHTML="₿ BTC $"+Math.round(d.extra.BTC)+" | 🛢️ Petroleo $"+d.extra.PETROLEO+" | 📈 Bono "+d.extra.BONO10+"%"}if(d.presidente){document.getElementById("presidente-mensaje").innerHTML=d.presidente.mensaje;document.getElementById("presidente-accion").innerHTML="👉 "+d.presidente.accion_jefe}if(d.cerebro){document.getElementById("cerebro-mensaje").innerHTML=d.cerebro.mensaje;document.getElementById("cerebro-leccion").innerHTML="📖 "+d.cerebro.leccion}if(d.cerebro_m5){document.getElementById("m5-mensaje").innerHTML=d.cerebro_m5.mensaje;document.getElementById("m5-leccion").innerHTML="📖 "+d.cerebro_m5.leccion;document.getElementById("m5-velas").innerHTML="Ultimas velas M5: "+d.cerebro_m5.velas.map(v=>v.precio).join(" -> ")}if(d.cerebro_capital){document.getElementById("capital-mensaje").innerHTML=d.cerebro_capital.mensaje;document.getElementById("capital-leccion").innerHTML="📖 "+d.cerebro_capital.leccion}if(d.capital){document.getElementById("capital-precio").innerHTML="💰 Capital.com: $"+d.capital.precio+" | Spread $"+d.capital.spread+" | "+d.capital.recomendacion}document.getElementById("origen-precios").innerHTML="🥇 ORO $"+d.ORO+" - "+d.robots_conectados.ORO.senal+"<br>💚 NVDA $"+d.NVDA+" - "+d.robots_conectados.NVDA.senal+"<br>🍎 APPLE $"+d.AAPL+" - "+d.robots_conectados.AAPL.senal+"<br>🚗 TESLA $"+d.TSLA+" - "+d.robots_conectados.TSLA.senal+"<br>🪟 MSFT $"+d.MSFT+"<br>📦 AMZN $"+d.AMZN+"<br>👍 META $"+d.META+"<br>🔍 GOOGLE $"+d.GOOGL;let mapa={"ORO":d.ORO,"NVDA":d.NVDA,"AAPL":d.AAPL,"TSLA":d.TSLA,"MSFT":d.MSFT,"AMZN":d.AMZN,"META":d.META,"GOOGL":d.GOOGL};simbolos.forEach(s=>{if(mapa[s.id])s.precio=mapa[s.id]});renderAcc()}catch(e){document.getElementById("satelite-texto").innerHTML="🛰️ Buscando USA..."}}
setInterval(actualizarSateliteUSA,15000);actualizarSateliteUSA();setInterval(()=>{let d=new Date();document.getElementById("reloj").innerHTML=d.toLocaleTimeString("es-ES");let h=d.getHours();document.getElementById("sesion").innerHTML=h>=14&&h<21?"🟢 SESION NEW YORK ABIERTA":"🟡 Sesion cerrada"},1000);setInterval(analizarTodo,30000);analizarTodo();
</script></body></html>"""
@app.route("/")
def home(): return HTML
@app.route("/api/satelite_usa")
def satelite_usa():
 try: oro=float(requests.get('https://api.gold-api.com/price/XAU',timeout=4).json().get('price',4088))
 except: oro=yahoo('GC=F',4088)
 datos={"ORO":oro,"NVDA":yahoo('NVDA',185.2),"AAPL":yahoo('AAPL',262.1),"TSLA":yahoo('TSLA',340.5),"MSFT":yahoo('MSFT',495.3),"AMZN":yahoo('AMZN',235.4),"META":yahoo('META',645.2),"GOOGL":yahoo('GOOGL',282.1)}
 bi=bancos(); ex=extra(); pr=presi(); jo=jefe(bi,datos,ex)
 if pr["nivel"]=="ROJO": jo={"orden":"🛑 PAUSA TOTAL - PRESIDENTE","motivo":pr["mensaje"],"permiso_operar":False,"mensaje":"JEFE DICE: "+pr["mensaje"]}
 cap(datos,jo); cr=crec(); m5_aprende(oro); m5r=m5_recuerda(); capd=get_capital_precio(oro); capital_aprende(capd["precio"],oro); capr=capital_recuerda()
 return jsonify({**datos,"motor":motor(oro,"ORO"),"velocidad":"TURBO 5 SEG - SATELITE USA","buscador":buscador(datos),"nyse":"ABIERTO - WALL STREET","nasdaq":"ABIERTO - USA","robots_conectados":conectar(datos),"origen_oro":"gold-api + Yahoo","origen_acciones":"Yahoo USA","bancos":bi,"jefe":jo,"extra":ex,"presidente":pr,"cerebro":cr,"cerebro_m5":m5r,"cerebro_capital":capr,"capital":capd,"equipo_40":EQUIPO,"total_robots":40})
@app.route("/api/bancos")
def api_bancos(): return jsonify(bancos())
@app.route("/api/extra")
def api_extra(): return jsonify(extra())
@app.route("/api/presidente")
def api_presidente(): return jsonify(presi())
@app.route("/api/cerebro")
def api_cerebro(): return jsonify(crec())
@app.route("/api/cerebro_m5")
def api_m5(): return jsonify(m5_recuerda())
@app.route("/api/capital")
def api_cap(): return jsonify({"capital":get_capital_precio(4088),"cerebro":capital_recuerda()})
@app.route("/api/preguntale")
def api_preguntale():
 try:
  pq=float(request.args.get("precio",4070)); act=request.args.get("activo","ORO")
  try: pa=float(requests.get('https://api.gold-api.com/price/XAU',timeout=4).json().get('price',4088))
  except: pa=4088
  if act!="ORO": pa=yahoo(act,pa)
  return jsonify(pregunta(pq,act,pa))
 except: return jsonify({"respuesta":"🤖 Escribe numero Ej 4070","decision":"ERROR","precio_recomendado":3940,"precio_actual":4088})
@app.route("/api/jefe")
def api_jefe():
 try: oro=float(requests.get('https://api.gold-api.com/price/XAU',timeout=4).json().get('price',4088))
 except: oro=4088
 return jsonify(jefe(bancos(),{"ORO":oro},extra()))
if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
