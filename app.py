//+------------------------------------------------------------------+
//|                                     RAUDY BANK V6 - ESTILO BANCO |
//|  M1 + M5 + M15 + H1 + H4 - Como operan los bancos               |
//|  ARREGLADO POR JEFE - Solo 1 operacion al dia                    |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK"
#property version   "6.00"
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01;
input double NivelCompra = 3910;  // CAMBIA ESTO CADA SEMANA, JEFE
input double NivelVenta = 3970;   // CAMBIA ESTO CADA SEMANA, JEFE
input double RiesgoDolar = 10.0;  // Banco: arriesga 10, no 1
input double GananciaDolar = 30.0; // Banco: gana 3x lo que arriesga
input int MaxOperacionesDia = 1;

int h_M1, h_M5, h_M15, h_H1, h_H4;
datetime diaActual = 0;
int operacionesHoy = 0;

int OnInit()
{
   h_M1 = iMA(_Symbol, PERIOD_M1, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M5 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M15 = iMA(_Symbol, PERIOD_M15, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_H1 = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_H4 = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_EMA, PRICE_CLOSE);

   trade.SetExpertMagicNumber(20261118);
   return(INIT_SUCCEEDED);
}

bool TendenciaAlcista()
{
   double m1[], m5[], m15[], h1[], h4[];
   double precio = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   if(CopyBuffer(h_M1,0,0,1,m1)<=0) return false;
   if(CopyBuffer(h_M5,0,0,1,m5)<=0) return false;
   if(CopyBuffer(h_M15,0,0,1,m15)<=0) return false;
   if(CopyBuffer(h_H1,0,0,1,h1)<=0) return false;
   if(CopyBuffer(h_H4,0,0,1,h4)<=0) return false;
   // Banco: Todas tienen que decir SUBE
   return(precio > m1[0] && precio > m5[0] && precio > m15[0] && precio > h1[0] && precio > h4[0]);
}

bool TendenciaBajista()
{
   double m1[], m5[], m15[], h1[], h4[];
   double precio = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   if(CopyBuffer(h_M1,0,0,1,m1)<=0) return false;
   if(CopyBuffer(h_M5,0,0,1,m5)<=0) return false;
   if(CopyBuffer(h_M15,0,0,1,m15)<=0) return false;
   if(CopyBuffer(h_H1,0,0,1,h1)<=0) return false;
   if(CopyBuffer(h_H4,0,0,1,h4)<=0) return false;
   return(precio < m1[0] && precio < m5[0] && precio < m15[0] && precio < h1[0] && precio < h4[0]);
}

void OnTick()
{
   // REGLA JEFE: Si ya hay operacion abierta, no abrir otra
   if(PositionsTotal() > 0) return;

   // REGLA JEFE: Nuevo dia = contador en 0
   MqlDateTime t;
   TimeToStruct(TimeCurrent(), t);
   datetime hoy = StructToTime(t) - (t.hour*3600 + t.min*60 + t.sec);
   if(hoy != diaActual)
   {
      diaActual = hoy;
      operacionesHoy = 0;
   }

   // REGLA JEFE: Si ya hizo 1 hoy, no hace mas
   if(operacionesHoy >= MaxOperacionesDia) return;

   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   // Calculo correcto para ORO: 0.01 lote = 1 dolar por cada 1 dolar de movimiento
   double tickValue = Symbol
