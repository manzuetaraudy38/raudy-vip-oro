# ROBOT DOBLE EN 1 - TRADING CON IA - JEFE
# 1 = Robot Comprador, 2 = Robot Vendedor, Chip IA decide

class RobotTradingJefe:
    def __init__(self):
        self.dinero = 1000
        self.cripto = 0
        self.chip_ia = "ACTIVO"

    def robot_1_comprador(self, precio, tendencia):
        # Si baja el precio y la IA dice COMPRA
        if tendencia == "BAJA" and precio < 90:
            print("ROBOT 1 JEFE: ¡COMPRO, JEFE!")
            return "COMPRAR"
        return "ESPERAR"

    def robot_2_vendedor(self, precio, tendencia):
        # Si sube el precio y la IA dice VENDE
        if tendencia == "SUBE" and precio > 110:
            print("ROBOT 2 JEFE: ¡VENDO, JEFE!")
            return "VENDER"
        return "ESPERAR"

    def chip_ia_decide(self, precio, tendencia):
        print(f"CHIP IA JEFE: Precio {precio} - Tendencia {tendencia}")
        accion1 = self.robot_1_comprador(precio, tendencia)
        accion2 = self.robot_2_vendedor(precio, tendencia)

        if accion1 == "COMPRAR":
            self.cripto += 1
            self.dinero -= precio
            print(f"¡COMPRADO, JEFE! Dinero: {self.dinero}")
        elif accion2 == "VENDER":
            self.cripto -= 1
            self.dinero += precio
            print(f"¡VENDIDO, JEFE! Dinero: {self.dinero}")
        else:
            print("CHIP IA: ESPERAMOS, JEFE. No hay jugada.")

# PRUEBA, JEFE
robot = RobotTradingJefe()
robot.chip_ia_decide(85, "BAJA")
robot.chip_ia_decide(115, "SUBE")
robot.chip_ia_decide(100, "LATERAL")
