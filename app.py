//+------------------------------------------------------------------+
//|      RAUDY BANK V12 - IA LEARNA + APP VELAS - SOLO XM MT5       |
//|  4H MANDA - SOLO COMPRA CON 4-5 VERDES - SI 3 ROJAS NO ENTRA    |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK V12 - LEARNA + VELAS XM"
#property version   "12.00"
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01; // JEFE: Nunca lo subas. 0.01 = seguro
input double RiesgoDolar = 10.0;
input double GananciaDolar = 30.0;
input int MaxOperacionesDia = 1;
input int MinPuntosIA = 4;
input bool ModoIA = true;
input bool AlarmaActiva = true;
input bool ModoAprendizaje = true; // JEFE: LEARNA - true = aprende
input bool ModoAppVelas = true; // JEFE: true = obedece tu APP de velas. NO lo apagues
input bool SoloOperarSiEsGOLD = true;
input int HoraInicioXM = 8;
input int HoraFinXM = 20;
input double NivelCompraFijo = 3700;
input double NivelVentaFijo = 3760;
input int EsperaTrasPerderMin = 60;
input int EsperaTras3RojasMin = 30; // JEFE: APP - Si hay 3 rojas, espera 30 min

int h_M1, h_M5, h_M15, h_H1, h_H4;
int h_RSI, h_ATR, h_MACD;
datetime diaActual = 0;
int operacionesHoy = 0;
bool alarmaHoyYaSono = false;

// JEFE: MEMORIA LEARNA
int ganadasHoy = 0;
int perdidasHoy = 0;
int rachaGanadora = 0;
int rachaPerdedora = 0;
double profitHoy = 0;
datetime ultimaPerdidaTiempo = 0;
datetime ultima3RojasTiempo = 0;
string ultimaLeccion = "SIN LECCION TODAVIA - EMPEZANDO V12";
int puntosExigidosHoy = 4;
int verdesHoy = 0;
int rojasHoy = 0;

int OnInit()
{
   string simbolo = _Symbol;
   if(SoloOperarSiEsGOLD && simbolo != "GOLD#" && simbolo != "GOLD" && simbolo != "XAUUSD" && simbolo != "XAUUSD#")
   {
      Alert("JEFE! V12 ES SOLO PARA GOLD# DE XM! Tu estas en: " + simbolo);
      return(INIT_FAILED);
   }
   SymbolSelect(_Symbol, true);
   h_M1 = iMA(_Symbol, PERIOD_M1, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M5 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_M15 = iMA(_Symbol, PERIOD_M15, 20, 0, MODE_EMA, PRICE_CLOSE);
   h_H1 = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_H4 = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_EMA, PRICE_CLOSE);
   h_RSI = iRSI(_Symbol, PERIOD_M15, 14, PRICE_CLOSE);
   h_ATR = iATR(_Symbol, PERIOD_H1, 14);
   h_MACD = iMACD(_Symbol, PERIOD_M15, 12, 26, 9, PRICE_CLOSE);
   trade.SetExpertMagicNumber(20270112);
   trade.SetDeviationInPoints(30);
   Print("RAUDY V12 LEARNA + VELAS XM LISTO - 4H MANDA");
   return(INIT_SUCCEEDED);
}

void OnTradeTransaction(const MqlTradeTransaction& trans, const MqlTradeRequest& request, const MqlTradeResult& result)
{
   if(trans.type != TRADE_TRANSACTION_DEAL_ADD) return;
   if(trans.symbol != _Symbol) return;
   if(trans.deal_type != DEAL_TYPE_SELL && trans.deal_type != DEAL_TYPE_BUY) return;
   if(HistoryDealSelect(trans.deal))
   {
      long entry = HistoryDealGetInteger(trans.deal, DEAL_ENTRY);
      if(entry == DEAL_ENTRY_OUT || entry == DEAL_ENTRY_INOUT)
      {
         double prof = HistoryDealGetDouble(trans.deal, DEAL_PROFIT) + HistoryDealGetDouble(trans.deal, DEAL_SWAP) + HistoryDealGetDouble(trans.deal, DEAL_COMMISSION);
         if(ModoAprendizaje)
         {
            profitHoy += prof;
            if(prof >= 0)
            {
               ganadasHoy++; rachaGanadora++; rachaPerdedora = 0;
               ultimaLeccion = "MUY BIEN JEFE! GANASTE! SIGUE ASI - LEARNA";
            }
            else
            {
               perdidasHoy++; rachaPerdedora++; rachaGanadora = 0;
               ultimaPerdidaTiempo = TimeCurrent();
               if(rachaPerdedora >= 2)
                  ultimaLeccion = "JEFE, PERDISTE 2 SEGUIDAS. APRENDI: ESPERO 60 MIN Y PIDO 5 PUNTOS";
               else
                  ultimaLeccion = "JEFE, PERDISTE 1. APRENDI: MAS CUIDADO";
            }
         }
      }
   }
}

void MostrarTablero(double bid, double ask, double compraIA, double ventaIA, double distSL, double distTP, int puntos, double rsi, double atr, double spread, double macd, int verdes, int rojas, string tendencia4H)
{
   string t1 = "👑 RAUDY V12 - LEARNA + VELAS - XM GOLD#";
   string t2 = "XM PRECIO: " + DoubleToString(bid,2) + " | SPREAD: " + DoubleToString(spread,2) + " | MACD: " + DoubleToString(macd,2);
   string t3 = "APP VELAS: 🟢 VERDES: " + IntegerToString(verdes) + " | 🔴 ROJAS: " + IntegerToString(rojas) + " | 4H: " + tendencia4H;
   string t4 = "IA COMPRA: " + DoubleToString(compraIA,2) + " | IA VENTA: " + DoubleToString(ventaIA,2);
   string t5 = "SL=" + DoubleToString(bid-distSL,2) + " (-" + DoubleToString(RiesgoDolar,0) + "$) TP=" + DoubleToString(bid+distTP,2) + " (+" + DoubleToString(GananciaDolar,0) + "$)";
   string t6 = "PUNTOS: " + IntegerToString(puntos) + "/" + IntegerToString(puntosExigidosHoy) + " | RSI: " + DoubleToString(rsi,1) + " | ATR: " + DoubleToString(atr,2);
   string t7 = "HOY: " + IntegerToString(operacionesHoy) + "/" + IntegerToString(MaxOperacionesDia) + " | GANADAS: " + IntegerToString(ganadasHoy) + " | PERDIDAS: " + IntegerToString(perdidasHoy) + " | PROFIT: $" + DoubleToString(profitHoy,2);
   string t8 = "";
   if(verdes >= 4 && puntos >= puntosExigidosHoy) t8 = "🟢 ¡JEFE! ¡APP DICE 4-5 VERDES! ¡LISTO PARA COMPRA!";
   else if(rojas >= 3) t8 = "🔴 ¡JEFE! ¡3 ROJAS! ¡NO ENTRES! ¡ESPERA! ¡CAYENDO!";
   else t8 = "🟡 ESPERA JEFE - APP DICE: MERCADO MEZCLADO - NO ENTRES";
   string t9 = "📚 LECCION: " + ultimaLeccion;
   Comment(t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5 + "\n" + t6 + "\n" + t7 + "\n" + t8 + "\n" + t9);
}

void OnTick()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   if(bid <= 0 || ask <= 0) return;

   int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   long stopLevel = SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double spreadEnDolares = ask - bid;
   if(tickValue <= 0 || tickSize <= 0) return;

   double loteSeguro = Lote;
   if(loteSeguro > 0.05) loteSeguro = 0.01;
   if(ModoAprendizaje && rachaPerdedora >= 2) loteSeguro = 0.01;
   if(loteSeguro < minLot) loteSeguro = minLot;
   if(loteSeguro > maxLot) loteSeguro = maxLot;
   loteSeguro = MathFloor(loteSeguro / lotStep) * lotStep;
   if(loteSeguro < minLot) loteSeguro = minLot;

   double valorPorPunto = (loteSeguro * tickValue) / tickSize;
   if(valorPorPunto <= 0) return;
   double distSL = RiesgoDolar / valorPorPunto;
   double distTP = GananciaDolar / valorPorPunto;
   double distMinima = (stopLevel + 5) * point;
   if(distSL < distMinima) distSL = distMinima;
   if(distTP < distMinima) distTP = distMinima;

   MqlDateTime t; TimeToStruct(TimeCurrent(), t);
   datetime hoy = StructToTime(t) - (t.hour*3600 + t.min*60 + t.sec);
   static double NivelCompraIA = 0;
   static double NivelVentaIA = 0;
   if(hoy != diaActual || NivelCompraIA == 0)
   {
      diaActual = hoy;
      operacionesHoy = 0; ganadasHoy = 0; perdidasHoy = 0; profitHoy = 0;
      rachaGanadora = 0; rachaPerdedora = 0;
      alarmaHoyYaSono = false;
      ultimaLeccion = "NUEVO DIA JEFE - V12 EMPIEZA DE CERO";
      if(ModoIA)
      {
         NivelCompraIA = MathRound(bid - 25);
         NivelVentaIA = MathRound(bid + 25);
      }
      else
      {
         NivelCompraIA = NivelCompraFijo;
         NivelVentaIA = NivelVentaFijo;
      }
   }
   bool enHorarioXM = (t.hour >= HoraInicioXM && t.hour < HoraFinXM);

   double m1[], m5[], m15[], h1[], h4[], rsiArr[], atrArr[], macdMain[], macdSignal[];
   if(CopyBuffer(h_M1,0,0,1,m1)<=0) return;
   if(CopyBuffer(h_M5,0,0,1,m5)<=0) return;
   if(CopyBuffer(h_M15,0,0,1,m15)<=0) return;
   if(CopyBuffer(h_H1,0,0,1,h1)<=0) return;
   if(CopyBuffer(h_H4,0,0,1,h4)<=0) return;
   if(CopyBuffer(h_RSI,0,0,1,rsiArr)<=0) return;
   if(CopyBuffer(h_ATR,0,0,1,atrArr)<=0) return;
   if(CopyBuffer(h_MACD,0,0,1,macdMain)<=0) return;
   if(CopyBuffer(h_MACD,1,0,1,macdSignal)<=0) return;

   // --- JEFE: APP VELAS - CONTAR VERDES Y ROJAS ---
   // VERDE = precio arriba de EMA, ROJA = precio abajo de EMA
   int verdes = 0; int rojas = 0;
   if(bid > m1[0]) verdes++; else rojas++;
   if(bid > m5[0]) verdes++; else rojas++;
   if(bid > m15[0]) verdes++; else rojas++;
   if(bid > h1[0]) verdes++; else rojas++;
   if(bid > h4[0]) verdes++; else rojas++;
   verdesHoy = verdes; rojasHoy = rojas;

   // JEFE: 4H MANDA - CONFIRMACION MAESTRA
   string tendencia4H = "🟡 MEZCLADO";
   bool h4Verde = (bid > h4[0]);
   bool h4Roja = (bid < h4[0]);
   if(h4Verde) tendencia4H = "🟢 VERDE - SUBIENDO";
   if(h4Roja) tendencia4H = "🔴 ROJA - CAYENDO";

   // JEFE: Si hay 3 rojas, marca el tiempo para esperar
   if(ModoAppVelas && rojas >= 3 && ultima3RojasTiempo == 0)
   {
      ultima3RojasTiempo = TimeCurrent();
      ultimaLeccion = "JEFE, HAY 3 ROJAS COMO EN TU FOTO. APRENDI: ESPERO 30 MIN";
   }
   if(rojas < 3) ultima3RojasTiempo = 0;

   bool alcista = (verdes >= 4); // JEFE: APP - Solo si 4 o 5 verdes
   bool bajista = (rojas >= 4);
   bool macdCompra = (macdMain[0] > macdSignal[0]);
   bool macdVenta = (macdMain[0] < macdSignal[0]);

   // JEFE: Si 4H es roja, NUNCA compra - aunque haya verdes en M1
   if(ModoAppVelas && h4Roja) alcista = false;
   // JEFE: Si 4H es verde, NUNCA vende
   if(ModoAppVelas && h4Verde) bajista = false;

   puntosExigidosHoy = MinPuntosIA;
   if(ModoAprendizaje)
   {
      if(atrArr[0] > 20) puntosExigidosHoy = 5;
      if(rachaPerdedora >= 2) puntosExigidosHoy = 5;
      if(rachaGanadora >= 2) puntosExigidosHoy = 4;
   }

   int puntos = 0;
   if(alcista || bajista) puntos += 2;
   if(alcista && rsiArr[0] < 70) puntos += 1;
   if(bajista && rsiArr[0] > 30) puntos += 1;
   if(atrArr[0] > 5 && atrArr[0] < 30) puntos += 1;
   double distancia = MathAbs(bid - h1[0]);
   if(distancia > 10 && distancia < 80) puntos += 1;
   if(alcista && macdCompra) puntos += 1;
   if(bajista && macdVenta) puntos += 1;
   // JEFE: PUNTO EXTRA APP - Si tienes 5 verdes, +1
   if(verdes == 5) puntos += 1;
   if(puntos > 7) puntos = 7;

   MostrarTablero(bid, ask, NivelCompraIA, NivelVentaIA, distSL, distTP, puntos, rsiArr[0], atrArr[0], spreadEnDolares, macdMain[0], verdes, rojas, tendencia4H);

   if(AlarmaActiva && verdes >= 4 && puntos >= puntosExigidosHoy && !alarmaHoyYaSono)
   {
      alarmaHoyYaSono = true;
      Alert("👑 RAUDY V12 - JEFE! APP DICE " + IntegerToString(verdes) + " VERDES! 4H " + tendencia4H + " COMPRA GOLD# A " + DoubleToString(bid,2));
      PlaySound("alert.wav");
      SendNotification("RAUDY V12 - JEFE! " + IntegerToString(verdes) + " VERDES! " + IntegerToString(puntos) + " puntos! COMPRA GOLD# XM: " + DoubleToString(bid,2));
   }
   // JEFE: Alarma de peligro si hay 3 rojas
   if(AlarmaActiva && rojas >= 3 && !alarmaHoyYaSono)
   {
      alarmaHoyYaSono = true;
      Alert("🔴 RAUDY V12 - JEFE! 3 ROJAS! NO ENTRES! CAYENDO! GOLD# " + DoubleToString(bid,2));
      SendNotification("RAUDY V12 - JEFE! 3 ROJAS! NO ENTRES! GOLD# " + DoubleToString(bid,2));
   }

   if(!enHorarioXM) return;
   if(PositionsTotal() > 0) return;
   if(operacionesHoy >= MaxOperacionesDia) return;

   // JEFE: LEARNA - Si perdiste 2, espera
   if(ModoAprendizaje && rachaPerdedora >= 2)
   {
      if(TimeCurrent() - ultimaPerdidaTiempo < EsperaTrasPerderMin * 60)
         return;
   }
   // JEFE: APP - Si hay 3 rojas, espera 30 min
   if(ModoAppVelas && rojas >= 3)
   {
      if(TimeCurrent() - ultima3RojasTiempo < EsperaTras3RojasMin * 60)
         return;
   }

   if(puntos >= puntosExigidosHoy)
   {
      if(alcista && macdCompra && verdes >= 4 && MathAbs(bid - NivelCompraIA) <= 15)
      {
         double sl = NormalizeDouble(ask - distSL, digits);
         double tp = NormalizeDouble(ask + distTP, digits);
         double precio = NormalizeDouble(ask, digits);
         if(trade.Buy(loteSeguro, _Symbol, precio, sl, tp, "RAUDY V12 COMPRA 4-5 VERDES"))
            operacionesHoy++;
      }
      if(bajista && macdVenta && rojas >= 4 && MathAbs(bid - NivelVentaIA) <= 15)
      {
         double sl = NormalizeDouble(bid + distSL, digits);
         double tp = NormalizeDouble(bid - distTP, digits);
         double precio = NormalizeDouble(bid, digits);
         if(trade.Sell(loteSeguro, _Symbol, precio, sl, tp, "RAUDY V12 VENTA 4-5 ROJAS"))
            operacionesHoy++;
      }
   }
}
