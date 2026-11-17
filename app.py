// Robot Raudy - GOLD# M5 - Precio 3849.51
// Solo DEMO, jefe. No lo uses en real sin probar.

input double PrecioReferencia = 3849.51;
input int VelasConfirmar = 5;
input double Lote = 0.01;

void OnTick()
{
   double precio = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   
   // Contar velas verdes y rojas
   int verdes = 0, rojas = 0;
   for(int i=1; i<=VelasConfirmar; i++)
   {
      double open = iOpen(_Symbol, PERIOD_M5, i);
      double close = iClose(_Symbol, PERIOD_M5, i);
      if(close > open) verdes++;
      if(close < open) rojas++;
   }
   
   // COMPRA FUERTE
   if(precio > PrecioReferencia && verdes == 5)
   {
      // Solo si no hay operación abierta
      if(PositionsTotal() == 0)
      {
         // Aquí abre COMPRA
         Print("JEFE - COMPRA FUERTE - Precio: ", precio, " Velas verdes: ", verdes);
      }
   }
   
   // VENTA FUERTE
   if(precio < PrecioReferencia && rojas == 5)
   {
      if(PositionsTotal() == 0)
      {
         // Aquí abre VENTA
         Print("JEFE - VENTA FUERTE - Precio: ", precio, " Velas rojas: ", rojas);
      }
   }
}
