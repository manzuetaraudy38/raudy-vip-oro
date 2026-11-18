//+------------------------------------------------------------------+
//|                 RAUDY BANK V9 - 2027 IA + ALARMA                |
//|  LISTO PARA PEGAR - Solo copiar todo y pegar en MetaEditor       |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK 2027 IA + ALARMA"
#property version   "9.00"
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01;
input double RiesgoDolar = 10.0;   // JEFE: Arriesgas 10
input double GananciaDolar = 30.0;  // JEFE: Ganas 30 = 3x
input int MaxOperacionesDia = 1;
input int MinPuntosIA = 4; // JEFE: Si no tiene 4, NO entra
input bool ModoIA = true;
input bool AlarmaActiva = true; // JEFE: true = Suena cuando hay 4 verdes
input double NivelCompraFijo = 3700; // JEFE: Si apagas IA, usa este
input double NivelVentaFijo = 3760;  // JEFE: Si apagas IA, usa este

int h_M1, h_M5, h_M15, h_H1, h_H4;
int h_RSI, h_ATR;
datetime diaActual = 0;
int operacionesHoy = 0;
int rachaGanadora = 0;
int rachaPerdedora = 0;
bool alarmaHoyYaSono = false;
datetime ultimoAviso = 0;

int OnInit()
{
   h_M1 = iMA(_Symbol, PERIOD_M1, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M5 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M15 = iMA(_Symbol, PERIOD_M15, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_H1 = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_H4 = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_RSI = iRSI(_Symbol, PERIOD_M15, 14, PRICE_CLOSE);
   h_ATR = iATR(_Symbol, PERIOD_H1, 14);
   trade.SetExpertMagicNumber(20270101);
   return(INIT_SUCCEEDED);
}

void MostrarTablero(double bid, double ask, double compraIA, double ventaIA, double distSL, double distTP, int puntos, double rsi, double atr)
{
   string t1 = "👑 RAUDY BANK V9 - 2027 IA + ALARMA";
   string t2 = "PRECIO EN VIVO: " + DoubleToString(bid,2) + " | VENTA: " + DoubleToString(ask,2);
   string t3 = "IA COMPRA EN: " + DoubleToString(compraIA,2) + " | IA VENTA EN: " + DoubleToString(ventaIA,2);
   string t4 = "SI ENTRAS: SL=" + DoubleToString(bid-distSL,2) + " (-" + DoubleToString(RiesgoDolar,0) + "$) TP=" + DoubleToString(bid+distTP,2) + " (+" + DoubleToString(GananciaDolar,0) + "$)";
   string t5 = "PUNTOS IA: " + IntegerToString(puntos) + "/5 | RSI: " + DoubleToString(rsi,1) + " | ATR: " + DoubleToString(atr,2) + " | HOY: " + IntegerToString(operacionesHoy) + "/" + IntegerToString(MaxOperacionesDia);
   string t6 = "";
   if(puntos >= 4) t6 = "🟢 ¡JEFE! ¡YA HAY 4 PUNTOS! ¡LISTO PARA ENTRAR!";
   else t6 = "🟡 ESPERA JEFE - Todavia no hay 4 puntos - NO ENTRES";
   Comment(t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5 + "\n" + t6);
}

void OnTick()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   if(tickValue <= 0 || tickSize <= 0) return;
   double valorPorPunto = (Lote * tickValue) / tickSize;
   if(valorPorPunto <= 0) return;
   double distSL = RiesgoDolar / valorPorPunto;
   double distTP = GananciaDolar / valorPorPunto;

   // --- IA 2027: Niveles con precio en vivo, pero fijos por dia ---
   // JEFE: Para que no se mueva a cada segundo, lo calculamos una vez al dia
   static double NivelCompraIA = 0;
   static double NivelVentaIA = 0;
   MqlDateTime t; TimeToStruct(TimeCurrent(), t);
   datetime hoy = StructToTime(t) - (t.hour*3600 + t.min*60 + t.sec);
   if(hoy != diaActual || NivelCompraIA == 0)
   {
      diaActual = hoy;
      operacionesHoy = 0;
      alarmaHoyYaSono = false;
      if(ModoIA)
      {
         // JEFE: Si el oro esta en 3730, compra en 3705 y vende en 3755
         NivelCompraIA = MathRound(bid - 25);
         NivelVentaIA = MathRound(bid + 25);
      }
      else
      {
         NivelCompraIA = NivelCompraFijo;
         NivelVentaIA = NivelVentaFijo;
      }
   }

   double LoteIA = Lote;
   if(rachaPerdedora >= 2) LoteIA = Lote * 0.5;
   if(rachaGanadora >= 2) LoteIA = Lote * 1.5;

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

   MostrarTablero(bid, ask, NivelCompraIA, NivelVentaIA, distSL, distTP, puntos, rsiArr[0], atrArr[0]);

   // --- 🔔 ALARMA JEFE: Solo cuando hay 4 puntos ---
   if(AlarmaActiva && puntos >= MinPuntosIA && !alarmaHoyYaSono)
   {
      alarmaHoyYaSono = true;
      string dir = alcista ? "COMPRA" : "VENTA";
      Alert("👑 RAUDY BANK - JEFE! YA HAY " + IntegerToString(puntos) + " PUNTOS! SEÑAL " + dir + " EN ORO A " + DoubleToString(bid,2));
      PlaySound("alert.wav");
      SendNotification("RAUDY BANK V9 - JEFE! Ya hay " + IntegerToString(puntos) + " puntos! Señal " + dir + " Oro: " + DoubleToString(bid,2));
      Print("ALARMA JEFE - 4 PUNTOS - " + dir);
   }

   // --- REGLAS JEFE ---
   if(PositionsTotal() > 0) return;
   if(operacionesHoy >= MaxOperacionesDia) return;

   if(puntos >= MinPuntosIA)
   {
      // JEFE: Entra si esta CERCA del nivel, no lejos. 15 dolares de margen.
      if(alcista && MathAbs(bid - NivelCompraIA) <= 15)
      {
         if(trade.Buy(LoteIA, _Symbol, ask, ask - distSL, ask + distTP, "RAUDY IA COMPRA"))
            operacionesHoy++;
      }
      if(bajista && MathAbs(bid - NivelVentaIA) <= 15)
      {
         if(trade.Sell(LoteIA, _Symbol, bid, bid + distSL, bid - distTP, "RAUDY IA VENTA"))
            operacionesHoy++;
      }
   }
}
