//+------------------------------------------------------------------+
//| RAUDY VIP ORO - Robot DEMO - NO usar con dinero real            |
//| Regla: Compra si el precio esta sobre la media, vende si baja   |
//+------------------------------------------------------------------+
#property copyright "RAUDY VIP ORO DEMO"
#property version   "1.00"

input double Lote = 0.01;          // Lote chiquito, jefe. NO lo subas
input int PeriodoMedia = 50;       // Media movil de 50
input int StopLoss_Puntos = 200;    // Freno, jefe
input int TakeProfit_Puntos = 200;  // Para ganar, jefe
input long MagicNumber = 123456;

int handleMA;
double bufferMA[];
MqlTradeRequest request;
MqlTradeResult result;

//+------------------------------------------------------------------+
int OnInit()
{
   handleMA = iMA(_Symbol, PERIOD_M15, PeriodoMedia, 0, MODE_SMA, PRICE_CLOSE);
   if(handleMA == INVALID_HANDLE)
   {
      Print("Error creando la media");
      return(INIT_FAILED);
   }
   ArraySetAsSeries(bufferMA, true);
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
void OnTick()
{
   // Solo 1 trade abierto a la vez, jefe. No abre 10, jefe.
   if(PositionsTotal() > 0)
      return;

   if(CopyBuffer(handleMA, 0, 0, 2, bufferMA) < 2)
      return;

   double precioActual = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double precioVenta = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double media = bufferMA[0];
   double punto = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   int digitos = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);

   ZeroMemory(request);
   request.action = TRADE_ACTION_DEAL;
   request.symbol = _Symbol;
   request.volume = Lote;
   request.magic = MagicNumber;
   request.deviation = 10;

   // REGLA A, JEFE: Si precio esta ARRIBA de la media = COMPRA
   if(precioActual > media)
   {
      request.type = ORDER_TYPE_BUY;
      request.price = precioActual;
      request.sl = NormalizeDouble(precioActual - StopLoss_Puntos * punto * 10, digitos);
      request.tp = NormalizeDouble(precioActual + TakeProfit_Puntos * punto * 10, digitos);
      request.comment = "RAUDY COMPRA DEMO";
      if(!OrderSend(request, result))
         Print("Error compra: ", result.retcode);
   }
   // Si precio esta ABAJO de la media = VENTA
   else if(precioVenta < media)
   {
      request.type = ORDER_TYPE_SELL;
      request.price = precioVenta;
      request.sl = NormalizeDouble(precioVenta + StopLoss_Puntos * punto * 10, digitos);
      request.tp = NormalizeDouble(precioVenta - TakeProfit_Puntos * punto * 10, digitos);
      request.comment = "RAUDY VENTA DEMO";
      if(!OrderSend(request, result))
         Print("Error venta: ", result.retcode);
   }
}
