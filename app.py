# CEREBRO - AUTOMATIC ENTRY & EXIT - JEFE
# Te pone TP y SL solo, jefe.

class CerebroAutoTP_SL:
    def calcular(self, precio_entrada, direccion, atr=10):
        print(f"JEFE, ENTRADA: {precio_entrada} | Direccion: {direccion}")

        # CEREBRO, JEFE: SL = 1 x ATR, TP = 2 x ATR. Ganas el doble de lo que arriesgas, jefe.
        if direccion == "COMPRA":
            sl = precio_entrada - atr
            tp1 = precio_entrada + atr
            tp2 = precio_entrada + (atr * 2)
            print(f"SL: {sl} (pierdes {atr}$)")
            print(f"TP1: {tp1} (ganas {atr}$)")
            print(f"TP2: {tp2} (ganas {atr*2}$, jefe!)")

        if direccion == "VENTA":
            sl = precio_entrada + atr
            tp1 = precio_entrada - atr
            tp2 = precio_entrada - (atr * 2)
            print(f"SL: {sl}")
            print(f"TP1: {tp1}")
            print(f"TP2: {tp2}")

        print("¡Listo, jefe! Ya no tienes que calcular nada.")
        return sl, tp1, tp2

# PRUEBA, JEFE. Como en la foto, jefe. Bitcoin
bot = CerebroAutoTP_SL()
bot.calcular(precio_entrada=97000, direccion="COMPRA", atr=300)
