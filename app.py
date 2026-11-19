
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
   h_M5 = iMA(_Symbol, PERIOD_M5, 20, 0, MODE_EMA, PRICE
