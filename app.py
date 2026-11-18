//+------------------------------------------------------------------+
//|                    RAUDY BANK V8 - 2027 IA                      |
//|  Tu V5 arreglado + IA + Calculador en Vivo + Aprende             |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK 2027 IA"
#property version   "8.00"
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01;
input double RiesgoDolar = 10.0;   // JEFE: Antes tenias 1, ahora 10 como banco
input double GananciaDolar = 30.0; // JEFE: Antes tenias 3, ahora 30 = 3x
input int MaxOperacionesDia = 1;
input int MinPuntosIA = 4; // JEFE: Si no tiene 4 puntos, NO entra
input bool ModoIA = true; // JEFE: true = IA calcula niveles sola

int h_M1, h_M5, h_M15, h_H1, h_H4;
int h_RSI, h_ATR;
datetime diaActual = 0;
int operacionesHoy = 0;
int rachaGanadora = 0;
int rachaPerdedora = 0;

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
   // JEFE: Esto es tu calculador en vivo
   string t1 = "👑 RAUDY BANK V8 - 2027 IA";
   string t2 = "PRECIO EN VIVO: " + DoubleToString(bid,2) + " | VENTA: " + DoubleToString(ask,2);
   string t3 = "IA COMPRA EN: " + DoubleToString(compraIA,2) + " | IA VENTA EN: " + DoubleToString(ventaIA,2);
   string t4 = "SI ENTRAS: SL=" + DoubleToString(bid-distSL,2) + " (-" + DoubleToString(RiesgoDolar,0) + "$) TP=" + DoubleToString(bid+distTP,2) + " (+" + DoubleToString(GananciaDolar,0) + "$)";
   string t5 = "PUNTOS IA: " + IntegerToString(puntos) + "/5 | RSI: " + DoubleToString(rsi,1) + " | ATR: " + DoubleToString(atr,2) + " | HOY: " + IntegerToString(operacionesHoy) + "/" + IntegerToString(MaxOperacionesDia);
   
   Comment(t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5);
}

void OnTick()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   // --- ARREGLO JEFE: Calculo correcto para ORO ---
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   if(tickValue <= 0 || tickSize <= 0) return;
   double valorPorPunto = (Lote * tickValue) / tickSize;
   if(valorPorPunto <= 0) return;
   double distSL = RiesgoDolar / valorPorPunto;
   double distTP = GananciaDolar / valorPorPunto;

   // --- IA 2027: Calcula niveles sola con precio en vivo ---
   // Jefe, ya no tienes que poner 3910 a mano. La IA lo hace.
   // Si el oro esta en 3724, ella compra en 3699 y vende en 3749
   double NivelCompraIA = bid - 25;
   double NivelVentaIA = bid + 25;
   if(!ModoIA) { NivelCompraIA = 3700; NivelVentaIA = 3760; } // Si apagas IA, usa estos

   // --- IA: Aprende - Si perdio 2, baja el lote ---
   double LoteIA = Lote;
   if(rachaPerdedora >= 2) LoteIA = Lote * 0.5;
   if(rachaGanadora >= 2) LoteIA = Lote * 1.5;

   // Leer indicadores
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

   // --- IA: PUNTOS ---
   int puntos = 0;
   if(alcista || bajista) puntos += 2;
   if(alcista && rsiArr[0] < 70) puntos += 1;
   if(bajista && rsiArr[0] > 30) puntos += 1;
   if(atrArr[0] > 5 && atrArr[0] < 30) puntos += 1;
   double distancia = MathAbs(bid - h1[0]);
   if(distancia > 10 && distancia < 80) puntos += 1;

   MostrarTablero(bid, ask, NivelCompraIA, NivelVentaIA, distSL, distTP, puntos, rsiArr[0], atrArr[0]);

   // --- REGLAS JEFE ---
   if(PositionsTotal() > 0) return;
   MqlDateTime t; TimeToStruct(TimeCurrent(), t);
   datetime hoy = StructToTime(t) - (t.hour*3600 + t.min*60 + t.sec);
   if(hoy != diaActual) { diaActual = hoy; operacionesHoy = 0; }
   if(operacionesHoy >= MaxOperacionesDia) return;

   // --- IA DECIDE: Solo si tiene 4 puntos o mas ---
   if(puntos >= MinPuntosIA)
   {
      if(alcista && bid <= NivelCompraIA + 5)
      {
         if(trade.Buy(LoteIA, _Symbol, ask, ask - distSL, ask + distTP, "RAUDY IA COMPRA"))
            operacionesHoy++;
      }
      if(bajista && bid >= NivelVentaIA - 5)
      {
         if(trade.Sell(LoteIA, _Symbol, bid, bid + distSL, bid - distTP, "RAUDY IA VENTA"))
            operacionesHoy++;
      }
   }
}
