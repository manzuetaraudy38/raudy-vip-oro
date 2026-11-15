//+------------------------------------------------------------------+
//|                                     RAUDY ORO BOT V3 - DE VERDAD |
//+------------------------------------------------------------------+
#property copyright "RAUDY"
#property version   "3.00"
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01;
input double NivelCompra = 3910;
input double NivelVenta = 3970;
input double MetaDiaria = 5.0;   // Si gana $5 hoy, se para
input double MaxPerdidaDiaria = 2.0; // Si pierde $2 hoy, se para

double ganadoHoy = 0;
datetime diaActual = 0;

void OnTick()
{
   MqlDateTime dt;
   TimeToStruct(TimeCurrent(), dt);
   datetime hoy = StringToTime((string)dt.year+"."+(string)dt.mon+"."+(string)dt.day);
   if(hoy != diaActual){ diaActual = hoy; ganadoHoy = 0; }

   // Si ya gano su meta o ya perdio su maximo, NO opera mas hoy
   if(ganadoHoy >= MetaDiaria) return;
   if(ganadoHoy <= -MaxPerdidaDiaria) return;
   if(PositionsTotal() > 0) return;

   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   double distTP = MetaDiaria / (Lote * 100.0);
   double distSL = MaxPerdidaDiaria / (Lote * 100.0);

   if(bid <= NivelCompra)
      trade.Buy(Lote, _Symbol, ask, bid - distSL, bid + distTP, "RAUDY V3 COMPRA");

   if(bid >= NivelVenta)
      trade.Sell(Lote, _Symbol, bid, bid + distSL, bid - distTP, "RAUDY V3 VENTA");
}
