//+------------------------------------------------------------------+
//|            RAUDY BANK V10 - 2027 IA - SOLO PARA XM MT5          |
//|  ALINEADO CON XM - GOLD# - LOTE 0.01 - ALARMA 4 PUNTOS           |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK V10 - SOLO XM"
#property version   "10.00"
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01; // JEFE: XM - NO lo subas. 0.01 = seguro
input double RiesgoDolar = 10.0;   // JEFE: Pierdes max 10
input double GananciaDolar = 30.0;  // JEFE: Ganas 30 = 3x
input int MaxOperacionesDia = 1;
input int MinPuntosIA = 4;
input bool ModoIA = true;
input bool AlarmaActiva = true;
input bool SoloOperarSiEsGOLD = true; // JEFE: true = solo GOLD# de XM
input int HoraInicioXM = 8;  // JEFE: Hora XM - Empieza 08:00
input int HoraFinXM = 20;    // JEFE: Hora XM - Termina 20:00
input double NivelCompraFijo = 3700;
input double NivelVentaFijo = 3760;

int h_M1, h_M5, h_M15, h_H1, h_H4;
int h_RSI, h_ATR;
datetime diaActual = 0;
int operacionesHoy = 0;
bool alarmaHoyYaSono = false;

int OnInit()
{
   // --- JEFE: VERIFICA QUE ESTAS EN XM Y EN GOLD# ---
   string simbolo = _Symbol;
   if(SoloOperarSiEsGOLD && simbolo != "GOLD#" && simbolo != "GOLD" && simbolo != "XAUUSD" && simbolo != "XAUUSD#")
   {
      Alert("JEFE! ESTE ROBOT ES SOLO PARA GOLD# DE XM! Tu estas en: " + simbolo + " - Cambialo a GOLD#");
      Print("RAUDY V10 XM - Simbolo incorrecto: " + simbolo);
      return(INIT_FAILED);
   }

   // JEFE: XM - Activa el simbolo para que tenga datos
   SymbolSelect(_Symbol, true);

   h_M1 = iMA(_Symbol, PERIOD_M1, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M5 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M15 = iMA(_Symbol, PERIOD_M15, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_H1 = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_H4 = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_RSI = iRSI(_Symbol, PERIOD_M15, 14, PRICE_CLOSE);
   h_ATR = iATR(_Symbol, PERIOD_H1, 14);
   trade.SetExpertMagicNumber(20270101);
   // JEFE: XM usa Filling IOC a veces, lo dejamos en automatico
   trade.SetDeviationInPoints(30);
   Print("RAUDY V10 XM LISTO - Simbolo: " + _Symbol + " Digitos: " + IntegerToString((int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS)));
   return(INIT_SUCCEEDED);
}

void MostrarTablero(double bid, double ask, double compraIA, double ventaIA, double distSL, double distTP, int puntos, double rsi, double atr, double spread)
{
   string t1 = "👑 RAUDY BANK V10 - XM - GOLD#";
   string t2 = "XM PRECIO: " + DoubleToString(bid,2) + " | VENTA: " + DoubleToString(ask,2) + " | SPREAD: " + DoubleToString(spread,2);
   string t3 = "IA COMPRA EN: " + DoubleToString(compraIA,2) + " | IA VENTA EN: " + DoubleToString(ventaIA,2);
   string t4 = "SI ENTRAS: SL=" + DoubleToString(bid-distSL,2) + " (-" + DoubleToString(RiesgoDolar,0) + "$) TP=" + DoubleToString(bid+distTP,2) + " (+" + DoubleToString(GananciaDolar,0) + "$)";
   string t5 = "PUNTOS: " + IntegerToString(puntos) + "/5 | RSI: " + DoubleToString(rsi,1) + " | ATR: " + DoubleToString(atr,2) + " | HOY: " + IntegerToString(operacionesHoy) + "/" + IntegerToString(MaxOperacionesDia);
   string t6 = "";
   if(puntos >= 4) t6 = "🟢 ¡JEFE! ¡YA HAY 4 PUNTOS! ¡LISTO EN XM!";
   else t6 = "🟡 ESPERA JEFE - No hay 4 puntos - NO ENTRES";
   string t7 = "LOTE XM: " + DoubleToString(Lote,2) + " | SOLO GOLD# XM";
   Comment(t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5 + "\n" + t6 + "\n" + t7);
}

void OnTick()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   if(bid <= 0 || ask <= 0) return;

   // --- JEFE: DATOS XM ---
   int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   long stopLevel = SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double spread = (ask - bid) / point; // en puntos
   double spreadEnDolares = ask - bid;

   if(tickValue <= 0 || tickSize <= 0) return;

   // --- JEFE: PROTECCION XM - Si pones lote 1, lo bajo a 0.01 solo ---
   double loteSeguro = Lote;
   if(loteSeguro > 0.05) loteSeguro = 0.01; // JEFE: Nunca mas de 0.05 en XM
   if(loteSeguro < minLot) loteSeguro = minLot;
   if(loteSeguro > maxLot) loteSeguro = maxLot;
   // Ajustar al paso de XM
   loteSeguro = MathFloor(loteSeguro / lotStep) * lotStep;
   if(loteSeguro < minLot) loteSeguro = minLot;

   double valorPorPunto = (loteSeguro * tickValue) / tickSize;
   if(valorPorPunto <= 0) return;
   double distSL = RiesgoDolar / valorPorPunto;
   double distTP = GananciaDolar / valorPorPunto;

   // --- JEFE: XM - Si SL queda muy pegado, lo aleja al minimo de XM ---
   double distMinima = (stopLevel + 5) * point; // 5 puntos extra de seguridad
   if(distSL < distMinima) distSL = distMinima;
   if(distTP < distMinima) distTP = distMinima;

   // --- JEFE: HORA XM - No opera de noche ---
   MqlDateTime t; TimeToStruct(TimeCurrent(), t);
   datetime hoy = StructToTime(t) - (t.hour*3600 + t.min*60 + t.sec);
   static double NivelCompraIA = 0;
   static double NivelVentaIA = 0;
   if(hoy != diaActual || NivelCompraIA == 0)
   {
      diaActual = hoy;
      operacionesHoy = 0;
      alarmaHoyYaSono = false;
      if(ModoIA)
      {
         NivelCompraIA = MathRound(bid - 25);
         NivelVentaIA = MathRound(bid + 25);
      }
      else
      {
         NivelCompraIA = NivelCompraFijo;
         NivelVentaIA = NivelVentaFijo;
      }
   }
   bool enHorarioXM = (t.hour >= HoraInicioXM && t.hour < HoraFinXM);

   double m1[], m5[], m15[], h1[], h4[], rsiArr[], atrArr[];
   if(CopyBuffer(h_M1,0,0,1,m1)<=0) return;
   if(CopyBuffer(h_M5,0,0,1,m5)<=0) return;
   if(CopyBuffer(h_M15,0,0,1,m15)<=0) return;
   if(CopyBuffer(h_H1,0,0,1,h1)<=0) return;
   if(CopyBuffer(h_H4,0,0,1,h4)<=0) return;
   if(CopyBuffer(h_RSI,0,0,1,rsiArr)<=0) return;
   if(CopyBuffer(h_ATR,0,0,1,atrArr)<=0) return;

   bool alcista = (bid > m1[0] && bid > m5[0] && bid > m15[0] && bid > h1[0] && bid > h4[0]);
   bool bajista = (bid < m1[0] && bid < m5[0] && bid < m15[0] && bid < h1[0] && bid < h4[0]);

   int puntos = 0;
   if(alcista || bajista) puntos += 2;
   if(alcista && rsiArr[0] < 70) puntos += 1;
   if(bajista && rsiArr[0] > 30) puntos += 1;
   if(atrArr[0] > 5 && atrArr[0] < 30) puntos += 1;
   double distancia = MathAbs(bid - h1[0]);
   if(distancia > 10 && distancia < 80) puntos += 1;

   MostrarTablero(bid, ask, NivelCompraIA, NivelVentaIA, distSL, distTP, puntos, rsiArr[0], atrArr[0], spreadEnDolares);

   // --- 🔔 ALARMA XM ---
   if(AlarmaActiva && puntos >= MinPuntosIA && !alarmaHoyYaSono)
   {
      alarmaHoyYaSono = true;
      string dir = alcista ? "COMPRA" : "VENTA";
      Alert("👑 RAUDY V10 XM - JEFE! YA HAY " + IntegerToString(puntos) + " PUNTOS! " + dir + " GOLD# A " + DoubleToString(bid,2));
      PlaySound("alert.wav");
      SendNotification("RAUDY V10 XM - JEFE! Ya hay " + IntegerToString(puntos) + " puntos! " + dir + " GOLD# XM: " + DoubleToString(bid,2));
      Print("ALARMA XM JEFE - 4 PUNTOS - " + dir);
   }

   // --- REGLAS XM ---
   if(!enHorarioXM) return; // JEFE: De noche no entra
   if(PositionsTotal() > 0) return;
   if(operacionesHoy >= MaxOperacionesDia) return;

   if(puntos >= MinPuntosIA)
   {
      // JEFE: Normalizar precio a digitos XM
      if(alcista && MathAbs(bid - NivelCompraIA) <= 15)
      {
         double sl = NormalizeDouble(ask - distSL, digits);
         double tp = NormalizeDouble(ask + distTP, digits);
         double precio = NormalizeDouble(ask, digits);
         if(trade.Buy(loteSeguro, _Symbol, precio, sl, tp, "RAUDY V10 XM COMPRA"))
            operacionesHoy++;
      }
      if(bajista && MathAbs(bid - NivelVentaIA) <= 15)
      {
         double sl = NormalizeDouble(bid + distSL, digits);
         double tp = NormalizeDouble(bid - distTP, digits);
         double precio = NormalizeDouble(bid, digits);
         if(trade.Sell(loteSeguro, _Symbol, precio, sl, tp, "RAUDY V10 XM VENTA"))
            operacionesHoy++;
      }
   }
}
