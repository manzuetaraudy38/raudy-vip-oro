# CORAZON DEL ROBOT SHINOBI - ORO / XAUUSD - JEFE
# Este es el cerebro, jefe. Lo demás es adorno.

import time

class CorazonShinobi:
    def __init__(self):
        self.capital = 1000  # Empieza en DEMO, jefe. No real.
        self.posicion = None
        self.stop_loss = 15  # Si pierde 15$, se sale, jefe
        self.take_profit = 30 # Si gana 30$, se sale, jefe

    def analizar(self, precio, ema_rapida, ema_lenta, rsi):
        # EMA = media. Si rápida cruza arriba = SUBE
        # RSI = fuerza. Si RSI < 30 = barato, si > 70 = caro
        print(f"SHINOBI JEFE: Precio {precio} | RSI {rsi}")

        # SEÑAL DE COMPRA, JEFE
        if ema_rapida > ema_lenta and rsi < 35 and self.posicion is None:
            print("SHINOBI: ¡KATANA ARRIBA, JEFE! ¡COMPRO ORO!")
            self.posicion = ("COMPRA", precio)
            return "COMPRAR"

        # SEÑAL DE VENTA, JEFE
        if ema_rapida < ema_lenta and rsi > 65 and self.posicion is None:
            print("SHINOBI: ¡KATANA ABAJO, JEFE! ¡VENDO ORO!")
            self.posicion = ("VENTA", precio)
            return "VENDER"

        # PROTECCION - CORAZON, JEFE
        if self.posicion:
            tipo, entrada = self.posicion
            ganancia = precio - entrada if tipo == "COMPRA" else entrada - precio

            if ganancia >= self.take_profit:
                print(f"SHINOBI: ¡GANAMOS {ganancia}$, JEFE! ¡SALIMOS!")
                self.posicion = None
                return "CERRAR GANANCIA"
            if ganancia <= -self.stop_loss:
                print(f"SHINOBI: ¡PERDIMOS {ganancia}$, JEFE! ¡SALIMOS PA' NO PERDER MÁS!")
                self.posicion = None
                return "CERRAR PERDIDA"

        print("SHINOBI: Esperando, jefe. Como ninja, jefe.")
        return "ESPERAR"

# PRUEBA DEL CORAZON, JEFE
shinobi = CorazonShinobi()
shinobi.analizar(precio=2650, ema_rapida=2655, ema_lenta=2640, rsi=28)
shinobi.analizar(precio=2680, ema_rapida=2660, ema_lenta=2650, rsi=72)
