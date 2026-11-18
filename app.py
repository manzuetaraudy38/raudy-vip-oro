//+------------------------------------------------------------------+
//|                              RAUDY BANK V7 - WINDOWS LIVE       |
//|  CALCULADOR EN VIVO + ESTILO BANCO - Precio directo              |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK"
#property version   "7.00"
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01;
input double NivelCompra = 3700;  // JEFE: Cambia segun precio vivo
input double NivelVenta = 3760;   // JEFE: Cambia segun precio vivo
input double RiesgoDolar = 10.0;  // Arriesgas 10
input double GananciaDolar = 30.0; // Ganas 30 - 3x
input int MaxOperacionesDia = 1;

int h_M1, h_M5, h_M15, h_H1, h_H4;
datetime diaActual = 0;
int operacionesHoy = 0;

// --- TABLERO EN VIVO ---
void CrearTexto(string nombre, int y, int tamano, color col)
{
   if(ObjectFind(0, nombre) < 0)
      ObjectCreate(0, nombre, OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(0, nombre, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(0, nombre, OBJPROP_XDISTANCE, 15);
   ObjectSetInteger(0, nombre, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, nombre, OBJPROP_FONTSIZE, tamano);
   ObjectSetInteger(0, nombre, OBJPROP_COLOR, col);
   ObjectSetString(0, nombre, OBJPROP_FONT, "Arial Bold");
}

void MostrarCalculador(double bid, double ask, double distSL, double distTP)
{
   CrearTexto("RB_TITULO", 15, 16, clrGold);
   ObjectSetString(0, "RB_TITULO", OBJPROP_TEXT, "👑 RAUDY BANK V7 - EN VIVO");

   CrearTexto("RB_PRECIO", 45, 18, clrWhite);
   ObjectSetString(0, "RB_PRECIO", OBJPROP_TEXT, "PRECIO EN VIVO: " + DoubleToString(bid, 2) + "  |  VENTA: " + DoubleToString(ask, 2));

   CrearTexto("RB_NIVELES", 75, 12, clrYellow);
   ObjectSetString(0, "RB_NIVELES", OBJPROP_TEXT, "COMPRA EN: " + DoubleToString(NivelCompra,2) + "  |  VENTA EN: " + DoubleToString(NivelVenta,2));

   double faltaCompra = bid - NivelCompra;
   double faltaVenta = NivelVenta - bid;

   CrearTexto("RB_DIST", 100, 12, clrLightGreen);
   ObjectSetString(0, "RB_DIST", OBJPROP_TEXT, "Faltan " + DoubleToString(faltaCompra,1) + " para COMPRA | Faltan " + DoubleToString(faltaVenta,1) + " para VENTA");

   CrearTexto("RB_CALC", 125, 12, clrAqua);
   ObjectSetString(0, "RB_CALC", OBJPROP_TEXT, "SI ENTRAS: SL=" + DoubleToString(bid-distSL,2) + " (-" + DoubleToString(RiesgoDolar,0) + "$)  TP=" + DoubleToString(bid+distTP,2) + " (+" + DoubleToString(GananciaDolar,0) + "$)");

   CrearTexto("RB_DIA", 150, 12, clrOrange);
   ObjectSetString(0, "RB_DIA", OBJPROP_TEXT, "OPERACIONES HOY: " + IntegerToString(operacionesHoy) + "/" + IntegerToString(MaxOperacionesDia) + " | LOTE: " + DoubleToString(Lote,2));

   // Tambien abajo en la esquina
   Comment("RAUDY BANK LIVE\nPrecio: ", DoubleToString(bid,2), "\nCompra: ", NivelCompra, " | Venta: ", NivelVenta);
}

int OnInit()
{
   h_M1 = iMA(_Symbol, PERIOD_M1, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M5 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M15 = iMA(_Symbol, PERIOD_M15, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_H1 = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_H4 = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_EMA, PRICE_CLOSE);
   trade.SetExpertMagicNumber(20261118);
   ChartSetInteger(0, CHART_COLOR_BACKGROUND, clrBlack);
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   ObjectsDeleteAll(0, "RB_");
   Comment("");
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
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   if(tickValue <= 0 || tickSize <= 0) return;
   double valorPorPunto = (Lote * tickValue) / tickSize;
   if(valorPorPunto <= 0) return;
   double distSL = RiesgoDolar / valorPorPunto;
   double distTP = GananciaDolar / valorPorPunto;

   // --- MOSTRAR CALCULADOR EN VIVO SIEMPRE ---
   MostrarCalculador(bid, ask, distSL, distTP);

   if(PositionsTotal() > 0) return;
   MqlDateTime t; TimeToStruct(TimeCurrent(), t);
   datetime hoy = StructToTime(t) - (t.hour*3600 + t.min*60 + t.sec);
   if(hoy != diaActual) { diaActual = hoy; operacionesHoy = 0; }
   if(operacionesHoy >= MaxOperacionesDia) return;

   if(bid <= NivelCompra && TendenciaAlcista())
   {
      if(trade.Buy(Lote, _Symbol, ask, ask - distSL, ask + distTP, "RAUDY BANK COMPRA"))
         operacionesHoy++;
   }
   if(bid >= NivelVenta && TendenciaBajista())
   {
      if(trade.Sell(Lote, _Symbol, bid, bid + distSL, bid - distTP, "RAUDY BANK VENTA"))
         operacionesHoy++;
   }
}
