# ROBOT IA - MULTITIMEFRAME - JEFE
# 1m - 5m - 15m - 1h - 4h
# Solo entra si todos los marcos están de acuerdo

import time
import pandas as pd
import ccxt

# --- CONFIGURACION JEFE ---
SYMBOL = 'EUR/USD'  # Cambia a BTC/USDT, XAU/USD, etc.
TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h']
EMA_FAST = 9
EMA_SLOW = 21
RSI_PERIOD = 14
RISK_POR_TRADE = 0.01  # 1% por trade

exchange = ccxt.binance({
    'enableRateLimit': True,
})

def get_velas(symbol, timeframe, limit=100):
    """Baja las velas de un timeframe"""
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    return df

def calcular_indicadores(df):
    """EMA + RSI"""
    df['ema_fast'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

def tendencia(df):
    """Devuelve 1 = ALCISTA, -1 = BAJISTA, 0 = SIN CLARO"""
    ultima = df.iloc[-1]
    anterior = df.iloc[-2]
    
    # EMA cruzada + precio arriba/abajo
    if ultima['ema_fast'] > ultima['ema_slow'] and ultima['close'] > ultima['ema_slow']:
        if ultima['rsi'] < 70:  # No sobrecomprado
            return 1
    if ultima['ema_fast'] < ultima['ema_slow'] and ultima['close'] < ultima['ema_slow']:
        if ultima['rsi'] > 30:  # No sobrevendido
            return -1
    return 0

def analizar_todo():
    """Analiza los 5 timeframes"""
    resultados = {}
    print("\n--- ANALISIS JEFE ---")
    for tf in TIMEFRAMES:
        df = get_velas(SYMBOL, tf)
        df = calcular_indicadores(df)
        t = tendencia(df)
        resultados[tf] = t
        nombre = "🟢 SUBE" if t == 1 else "🔴 BAJA" if t == -1 else "⚪ NEUTRO"
        print(f"{tf}: {nombre} | Precio: {df.iloc[-1]['close']} | RSI: {df.iloc[-1]['rsi']:.1f}")
    return resultados

def robot_ia():
    print("ROBOT JEFE ENCENDIDO - Esperando confirmacion de 5 marcos...")
    while True:
        try:
            res = analizar_todo()
            
            # LOGICA JEFE: 4H manda, 1H confirma, 15m/5m/1m entran
            tf_4h = res['4h']
            tf_1h = res['1h']
            tf_15m = res['15m']
            tf_5m = res['5m']
            tf_1m = res['1m']
            
            # COMPRA - Todos alcistas
            if tf_4h == 1 and tf_1h == 1 and tf_15m == 1 and tf_5m == 1 and tf_1m == 1:
                print(">>> 🚀 SEÑAL COMPRA FUERTE - TODOS EN VERDE JEFE")
                # AQUI PONES TU ORDEN DE COMPRA
                # exchange.create_market_buy_order(SYMBOL, cantidad)
            
            # VENTA - Todos bajistas
            elif tf_4h == -1 and tf_1h == -1 and tf_15m == -1 and tf_5m == -1 and tf_1m == -1:
                print(">>> 📉 SEÑAL VENTA FUERTE - TODOS EN ROJO JEFE")
                # AQUI PONES TU ORDEN DE VENTA
                # exchange.create_market_sell_order(SYMBOL, cantidad)
            
            # COMPRA SUAVE - 4H y 1H mandan, 1m confirma
            elif tf_4h == 1 and tf_1h == 1 and tf_1m == 1:
                print(">>> ✅ SEÑAL COMPRA SUAVE - 4H + 1H + 1m JEFE")
            
            elif tf_4h == -1 and tf_1h == -1 and tf_1m == -1:
                print(">>> ✅ SEÑAL VENTA SUAVE - 4H + 1H + 1m JEFE")
            
            else:
                print(">>> ⏳ ESPERANDO JEFE - No hay acuerdo entre marcos")
            
            print("Esperando 60 segundos...")
            time.sleep(60)
            
        except Exception as e:
            print(f"Error jefe: {e}")
            time.sleep(10)

# --- ENCENDER ---
if __name__ == "__main__":
    robot_ia()
