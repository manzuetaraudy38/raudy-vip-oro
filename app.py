// ROBOT RAUDY - TUS PRECIOS - GOLD# M1
// Hecho para ti con tu foto - 17 Nov
// Solo DEMO, jefe

input double PrecioCompra = 3849.51; // Linea roja de tu foto
input double PrecioVenta = 3849.21;  // Linea azul de tu foto
input double Lote = 0.01; // Lo mas chiquito, jefe
input int VelasConfirmar = 3; // 3 velas en M1, no 5 porque M1 es muy rapido

void OnTick()
{
   double precio = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   
   // Contar velas
   int verdes = 0, rojas = 0;
   for(int i=1; i<=VelasConfirmar; i++)
   {
      double open = iOpen(_Symbol, PERIOD_M1, i);
      double close = iClose(_Symbol, PERIOD_M1, i);
      if(close > open) verdes++;
      if(close < open) rojas++;
   }

   // Si no hay operacion abierta
   if(PositionsTotal() == 0)
   {
      // COMPRA - Rompio tu linea roja 3849.51
      if(precio > PrecioCompra && verdes == VelasConfirmar)
      {
         Print("JEFE - COMPRA - Rompio 3849.51 - Precio: ", precio);
         // Aqui el robot abre COMPRA
      }

      // VENTA - Rompio tu linea azul 3849.21
      if(precio < PrecioVenta && rojas == VelasConfirmar)
      {
         Print("JEFE - VENTA - Rompio 3849.21 - Precio: ", precio);
         // Aqui el robot abre VENTA
      }

      // ENTRE MEDIO - NO HACE NADA
      if(precio >= PrecioVenta && precio <= PrecioCompra)
      {
         Print("JEFE - ESPERA - Esta entre 3849.21 y 3849.51");
      }
   }
}
