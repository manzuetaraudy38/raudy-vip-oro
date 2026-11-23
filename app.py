//+------------------------------------------------------------------+
//|  ROBOT DEMO - PLAN 50 EN 100 - JEFE RAUDY                       |
//|  SOLO DEMO - Cuenta: 1056619 - Capital.ComBah-Demo              |
//|  NO USAR EN REAL                                                 |
//+------------------------------------------------------------------+
#property copyright "Robot Demo Raudy - 50 en 100"
#property version   "1.00"
#include <Trade\Trade.mqh>

CTrade trade;

// --- TUS DATOS, JEFE ---
input double Lote = 0.01;          // Siempre 0.01, nunca mas
input double Mi_StopLoss = 3635;   // Si baja aqui, pierdo poquito
input double Mi_TakeProfit = 3650; // Si sube aqui, gano
input double Mi_Entrada = 3640;    // Solo compra si esta cerca de 3640
input ulong  Mi_Magic = 1056619;   // Tu numero de cuenta

//+------------------------------------------------------------------+
int OnInit()
  {
   trade.SetExpertMagicNumber(Mi_Magic);
   Print("Robot Demo Raudy listo - Cuenta 1056619 - Plan 50 en 100");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
void OnTick()
  {
   // Si ya hay un trade abierto, no abre otro, jefe
   if(PositionsTotal() > 0)
      return;

   double precio = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   // Solo compra ORO si el precio esta cerca de tu entrada
   // Si el precio esta entre 3638 y 3642, compra
   if(precio >= 3638 && precio <= 3642)
     {
      double sl = Mi_StopLoss;
      double tp = Mi_TakeProfit;

      // Abre la compra
      if(trade.Buy(Lote, _Symbol, precio, sl, tp, "Robot Demo 50 en 100"))
        {
         Print("COMPRA puesta, jefe! Lote: ", Lote, " Precio: ", precio);
        }
      else
        {
         Print("No se pudo abrir, jefe. Error: ", trade.ResultRetcode());
        }
     }
  }
//+------------------------------------------------------------------+
