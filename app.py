//+------------------------------------------------------------------+
//|      RAUDY BANK V11 - IA LEARNA - SOLO PARA XM MT5 GOLD#        |
//|  APRENDE DE TUS ERRORES COMO LEARNA - SE ADAPTA A TI - XM        |
//+------------------------------------------------------------------+
#property copyright "RAUDY BANK V11 - LEARNA IA XM"
#property version   "11.00"
#property strict
#include <Trade\Trade.mqh>
CTrade trade;

input double Lote = 0.01; // JEFE: LEARNA - Nunca lo subas. 0.01 = seguro
input double RiesgoDolar = 10.0;   // JEFE: Pierdes max 10
input double GananciaDolar = 30.0;  // JEFE: Ganas 30 = 3x
input int MaxOperacionesDia = 1;
input int MinPuntosIA = 4; // JEFE: Base 4, pero LEARNA lo sube a 5 si el mercado esta loco
input bool ModoIA = true;
input bool AlarmaActiva = true;
input bool ModoAprendizaje = true; // JEFE: true = APRENDE como LEARNA. NO lo apagues
input bool SoloOperarSiEsGOLD = true;
input int HoraInicioXM = 8;
input int HoraFinXM = 20;
input double NivelCompraFijo = 3700;
input double NivelVentaFijo = 3760;
input int EsperaTrasPerderMin = 60; // JEFE: LEARNA - Si pierdes, espera 60 min

int h_M1, h_M5, h_M15, h_H1, h_H4;
int h_RSI, h_ATR, h_MACD;
datetime diaActual = 0;
int operacionesHoy = 0;
bool alarmaHoyYaSono = false;

// --- JEFE: MEMORIA LEARNA ---
int ganadasHoy = 0;
int perdidasHoy = 0;
int rachaGanadora = 0;
int rachaPerdedora = 0;
double profitHoy = 0;
datetime ultimaPerdidaTiempo = 0;
string ultimaLeccion = "SIN LECCION TODAVIA - EMPEZANDO COMO LEARNA";
int puntosExigidosHoy = 4;

int OnInit()
{
   string simbolo = _Symbol;
   if(SoloOperarSiEsGOLD && simbolo != "GOLD#" && simbolo != "GOLD" && simbolo != "XAUUSD" && simbolo != "XAUUSD#")
   {
      Alert("JEFE! V11 LEARNA ES SOLO PARA GOLD# DE XM! Tu estas en: " + simbolo);
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
   // JEFE: LEARNA - Nuevo: MACD para confirmar, como un profesor extra
   h_MACD = iMACD(_Symbol, PERIOD_M15, 12, 26, 9, PRICE_CLOSE);
   trade.SetExpertMagicNumber(20270111);
   trade.SetDeviationInPoints(30);
   Print("RAUDY V11 LEARNA XM LISTO - GOLD# - Aprende como LEARNA");
   return(INIT_SUCCEEDED);
}

// --- JEFE: LEARNA APRENDE CUANDO SE CIERRA UNA OPERACION ---
void OnTradeTransaction(const MqlTradeTransaction& trans, const MqlTradeRequest& request, const MqlTradeResult& result)
{
   if(trans.type != TRADE_TRANSACTION_DEAL_ADD) return;
   if(trans.symbol != _Symbol) return;
   // Solo cuando se cierra (salida)
   if(trans.deal_type != DEAL_TYPE_SELL && trans.deal_type != DEAL_TYPE_BUY) return;

   // Buscar el deal para ver profit
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
                  ultimaLeccion = "JEFE, PERDISTE 2 SEGUIDAS. APRENDI: VOY A ESPERAR 60 MIN Y PEDIR 5 PUNTOS";
               else
                  ultimaLeccion = "JEFE, PERDISTE 1. APRENDI: VOY A TENER MAS CUIDADO";
            }
         }
      }
   }
}

void MostrarTablero(double bid, double ask, double compraIA, double ventaIA, double distSL, double distTP, int puntos, double rsi, double atr, double spread, double macd)
{
   string t1 = "👑 RAUDY V11 LEARNA - XM - GOLD#";
   string t2 = "XM PRECIO: " + DoubleToString(bid,2) + " | SPREAD: " + DoubleToString(spread,2) + " | MACD: " + DoubleToString(macd,2);
   string t3 = "IA COMPRA: " + DoubleToString(compraIA,2) + " | IA VENTA: " + DoubleToString(ventaIA,2);
   string t4 = "SL=" + DoubleToString(bid-distSL,2) + " (-" + DoubleToString(RiesgoDolar,0) + "$) TP=" + DoubleToString(bid+distTP,2) + " (+" + DoubleToString(GananciaDolar,0) + "$)";
   string t5 = "PUNTOS: " + IntegerToString(puntos) + "/" + IntegerToString(puntosExigidosHoy) + " | RSI: " + DoubleToString(rsi,1) + " | ATR: " + DoubleToString(atr,2);
   string t6 = "HOY: " + IntegerToString(operacionesHoy) + "/" + IntegerToString(MaxOperacionesDia) + " | GANADAS: " + IntegerToString(ganadasHoy) + " | PERDIDAS: " + IntegerToString(perdidasHoy) + " | PROFIT HOY: $" + DoubleToString(profitHoy,2);
   string t7 = "";
   if(puntos >= puntosExigidosHoy) t7 = "🟢 ¡JEFE! ¡LEARNA DICE LISTO! ¡YA HAY " + IntegerToString(puntos) + " PUNTOS!";
   else t7 = "🟡 ESPERA JEFE - LEARNA DICE: TODAVIA NO - FALTAN PUNTOS";
   string t8 = "📚 LECCION LEARNA: " + ultimaLeccion;
   Comment(t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5 + "\n" + t6 + "\n" + t7 + "\n" + t8);
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

   // --- JEFE: LEARNA - LOTE INTELIGENTE ---
   double loteSeguro = Lote;
   if(loteSeguro > 0.05) loteSeguro = 0.01;
   if(ModoAprendizaje && rachaPerdedora >= 2) loteSeguro = 0.01; // JEFE: Si pierdes, vuelve a 0.01
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
      ultimaLeccion = "NUEVO DIA JEFE - LEARNA EMPIEZA DE CERO";
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

   bool alcista = (bid > m1[0] && bid > m5[0] && bid > m15[0] && bid > h1[0] && bid > h4[0]);
   bool bajista = (bid < m1[0] && bid < m5[0] && bid < m15[0] && bid < h1[0] && bid < h4[0]);
   bool macdCompra = (macdMain[0] > macdSignal[0]);
   bool macdVenta = (macdMain[0] < macdSignal[0]);

   // --- JEFE: LEARNA ADAPTA LA DIFICULTAD ---
   puntosExigidosHoy = MinPuntosIA;
   if(ModoAprendizaje)
   {
      if(atrArr[0] > 20) puntosExigidosHoy = 5; // Mercado loco = mas dificil
      if(rachaPerdedora >= 2) puntosExigidosHoy = 5; // Si perdiste = mas dificil
      if(rachaGanadora >= 2) puntosExigidosHoy = 4; // Si ganas = normal
   }

   int puntos = 0;
   if(alcista || bajista) puntos += 2;
   if(alcista && rsiArr[0] < 70) puntos += 1;
   if(bajista && rsiArr[0] > 30) puntos += 1;
   if(atrArr[0] > 5 && atrArr[0] < 30) puntos += 1;
   double distancia = MathAbs(bid - h1[0]);
   if(distancia > 10 && distancia < 80) puntos += 1;
   // JEFE: PUNTO EXTRA LEARNA - MACD confirma
   if(alcista && macdCompra) puntos += 1;
   if(bajista && macdVenta) puntos += 1;
   if(puntos > 6) puntos = 6; // Max 6

   MostrarTablero(bid, ask, NivelCompraIA, NivelVentaIA, distSL, distTP, puntos, rsiArr[0], atrArr[0], spreadEnDolares, macdMain[0]);

   if(AlarmaActiva && puntos >= puntosExigidosHoy && !alarmaHoyYaSono)
   {
      alarmaHoyYaSono = true;
      string dir = alcista ? "COMPRA" : "VENTA";
      Alert("👑 RAUDY V11 LEARNA - JEFE! APRENDI! YA HAY " + IntegerToString(puntos) + " PUNTOS! " + dir + " GOLD# A " + DoubleToString(bid,2));
      PlaySound("alert.wav");
      SendNotification("RAUDY V11 LEARNA - JEFE! " + IntegerToString(puntos) + " puntos! " + dir + " GOLD# XM: " + DoubleToString(bid,2) + " | " + ultimaLeccion);
      Print("ALARMA LEARNA JEFE - " + dir);
   }

   // --- REGLAS LEARNA + XM ---
   if(!enHorarioXM) return;
   if(PositionsTotal() > 0) return;
   if(operacionesHoy >= MaxOperacionesDia) return;

   // JEFE: LEARNA - Si perdiste hace poco, espera
   if(ModoAprendizaje && rachaPerdedora >= 2)
   {
      if(TimeCurrent() - ultimaPerdidaTiempo < EsperaTrasPerderMin * 60)
         return;
   }

   if(puntos >= puntosExigidosHoy)
   {
      if(alcista && macdCompra && MathAbs(bid - NivelCompraIA) <= 15)
      {
         double sl = NormalizeDouble(ask - distSL, digits);
         double tp = NormalizeDouble(ask + distTP, digits);
         double precio = NormalizeDouble(ask, digits);
         if(trade.Buy(loteSeguro, _Symbol, precio, sl, tp, "RAUDY V11 LEARNA COMPRA"))
            operacionesHoy++;
      }
      if(bajista && macdVenta && MathAbs(bid - NivelVentaIA) <= 15)
      {
         double sl = NormalizeDouble(bid + distSL, digits);
         double tp = NormalizeDouble(bid - distTP, digits);
         double precio = NormalizeDouble(bid, digits);
         if(trade.Sell(loteSeguro, _Symbol, precio, sl, tp, "RAUDY V11 LEARNA VENTA"))
            operacionesHoy++;
      }
   }
}
