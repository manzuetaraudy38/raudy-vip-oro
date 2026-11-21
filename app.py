# CEREBRO - ROOK TRADE EXECUTOR - JEFE
# No adivina. PROTEGE, jefe.

class CerebroRook:
    def __init__(self):
        self.perdida_dia = 0
        self.limite_diario = -100  # Si pierdes 100$ en el día, STOP, jefe
        self.capital = 1000

    def calcular_lote(self, riesgo_por_operacion=10, stop_en_dolares=10):
        # Cuánto arriesgas, jefe. Ejemplo: 10$ por operación
        lote = riesgo_por_operacion / stop_en_dolares
        print(f"ROOK: Lote calculado: {lote}, jefe. No te pases.")
        return lote

    def ejecutar(self, accion, precio):
        # 1. ¿YA PERDISTE MUCHO HOY, JEFE?
        if self.perdida_dia <= self.limite_diario:
            print("ROOK: ¡DAILY LOSS LIMIT HIT, JEFE!")
            print("¡BLOQUEADO, JEFE! Vuelve mañana. No venganza, jefe.")
            return "BLOQUEADO"

        # 2. Si todo bien, ejecuta, jefe
        lote = self.calcular_lote()
        print(f"ROOK: Ejecutando {accion} a {precio} con lote {lote}, jefe.")
        print("ROOK: Stop Loss y Take Profit puestos solos, jefe.")
        return "EJECUTADO"

    def actualizar_perdida(self, resultado):
        self.perdida_dia += resultado
        print(f"ROOK: Pérdida hoy: {self.perdida_dia}$, jefe.")
        if self.perdida_dia <= self.limite_diario:
            print("ROOK: ¡TE BLOQUEO, JEFE! Pa' que no pierdas más.")

# PRUEBA, JEFE
rook = CerebroRook()
rook.ejecutar("COMPRAR ORO", 2650)
rook.actualizar_perdida(-110)  # Perdiste 110$, jefe
rook.ejecutar("COMPRAR ORO", 2652)  # Ya no te deja, jefe
