//+------------------------------------------------------------------+
//|                                     RAUDY BANK V5 - ESTILO BANCO |
//|  M1 + M5 + M15 + H1 + H4 - Como operan los bancos               |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK"
#property version   "5.00"
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01;
input double NivelCompra = 3910;  // Zona de liquidez donde el banco compra
input double NivelVenta = 3970;   // Zona de liquidez donde el banco vende
input double RiesgoDolar = 1.0;   // Banco: arriesga poco
input double GananciaDolar = 3.0; // Banco: gana 3x lo que arriesga
input int MaxOperacionesDia = 1;

int h_M1, h_M5, h_M15, h_H1, h_H4;
datetime diaActual = 0;
double ganadoHoy = 0;

int OnInit()
{
   h_M1 = iMA(_Symbol, PERIOD_M1, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M5 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M15 = iMA(_Symbol, PERIOD_M15, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_H1 = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_H4 = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_EMA, PRICE_CLOSE);
   return(INIT_SUCCEEDED);
}

bool TendenciaAlcista()
{
   double m1[], m5[], m15[], h1[], h4[];
   double precio = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   CopyBuffer(h_M1,0,0,1,m1); CopyBuffer(h_M5,0,0,1,m5);
   CopyBuffer(h_M15,0,0,1,m15); CopyBuffer(h_H1,0,0,1,h1); CopyBuffer(h_H4,0,0,1,h4);
   // Banco: Todas las velas tienen que estar de acuerdo para comprar
   return(precio > m1[0] && precio > m5[0] && precio > m15[0] && precio > h1[0] && precio > h4[0]);
}

bool TendenciaBajista()
{
   double m1[], m5[], m15[], h1[], h4[];
   double precio = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   CopyBuffer(h_M1,0,0,1,m1); CopyBuffer(h_M5,0,0,1,m5);
   CopyBuffer(h_M15,0,0,1,m15); CopyBuffer(h_H1,0,0,1,h1); CopyBuffer(h_H4,0,0,1,h4);
   return(precio < m1[0] && precio < m5[0] && precio < m15[0] && precio < h1[0] && precio < h4[0]);
}

void OnTick()
{
   if(PositionsTotal() > 0) return;

   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double distTP = GananciaDolar / (Lote * 100.0);
   double distSL = RiesgoDolar / (Lote * 100.0);

   // ESTILO BANCO: Solo compra en 3910 si TODAS las velas dicen SUBE
   if(bid <= NivelCompra && TendenciaAlcista())
      trade.Buy(Lote, _Symbol, ask, bid - distSL, bid + distTP, "RAUDY BANK COMPRA");

   // ESTILO BANCO: Solo vende en 3970 si TODAS las velas dicen BAJA
   if(bid >= NivelVenta && TendenciaBajista())
      trade.Sell(Lote, _Symbol, bid, bid + distSL, bid - distTP, "RAUDY BANK VENTA");
}
