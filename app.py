# CEREBRO - GOLD SCALPING BOT - MT5 XAUUSD - JEFE
# Entra rápido, sale rápido, jefe.

class CerebroGoldScalping:
    def __init__(self):
        self.posicion = None
        self.take_profit = 5  # Gana 5$ y sale, jefe. Poquito pero rápido.
        self.stop_loss = 3    # Pierde 3$ y sale, jefe.

    def operar(self, precio, banda_arriba, banda_abajo, ema):
        print(f"ORO: {precio}$ | Arriba: {banda_arriba} | Abajo: {banda_abajo}")

        # SI TOCA ABAJO = BARATO, JEFE. ¡COMPRA!
        if precio <= banda_abajo and self.posicion is None:
            print("GOLD BOT: ¡PRECIO ABAJO, JEFE! ¡COMPRO!")
            self.posicion = ("COMPRA", precio)
            return "COMPRAR"

        # SI TOCA ARRIBA = CARO, JEFE. ¡VENDE!
        if precio >= banda_arriba and self.posicion is None:
            print("GOLD BOT: ¡PRECIO ARRIBA, JEFE! ¡VENDO!")
            self.posicion = ("VENTA", precio)
            return "VENDER"

        # SALIDA RAPIDA, JEFE. SCALPING, JEFE.
        if self.posicion:
            tipo, entrada = self.posicion
            ganancia = precio - entrada if tipo == "COMPRA" else entrada - precio
            if ganancia >= self.take_profit:
                print(f"¡GANAMOS {ganancia}$, JEFE! ¡SALIMOS RAPIDO!")
                self.posicion = None
                return "CERRAR"
            if ganancia <= -self.stop_loss:
                print(f"Perdimos {ganancia}$, jefe. Salimos.")
                self.posicion = None
                return "CERRAR"

        print("Esperando, jefe. Buscando toque de banda...")
        return "ESPERAR"

# PRUEBA, JEFE
bot = CerebroGoldScalping()
bot.operar(precio=2648, banda_arriba=2660, banda_abajo=2650, ema=2655)
bot.operar(precio=2653, banda_arriba=2660, banda_abajo=2650, ema=2655)
