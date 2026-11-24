# RAUDY ORO - ROBOT IMPRIMIDOR DE RECIBO - GINEBRA
# Instalar antes: pip install python-escpos

from escpos.printer import Usb
from datetime import datetime
import os

def imprimir_recibo():
    print("=== RAUDY ORO - GINEBRA ===")
    print("Llena los datos, jefe:\n")

    # Datos del vendedor
    nombre = input("Nombre del vendedor: ")
    id_doc = input("No. Pasaporte / Permiso / ID: ")
    direccion = input("Direccion: ")
    descripcion = input("Que es? Anillo / Cadena / Pulsera: ")
    peso = float(input("Peso en gramos: "))
    quilates = input("Quilates (24K / 22K / 18K / 14K / 10K): ")
    precio_gramo = float(input("Precio por gramo CHF: "))

    total = peso * precio_gramo
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Intentar imprimir en impresora termica
    try:
        # Cambia estos numeros por los de tu impresora
        # Para saberlos: en Windows ve a Administrador de dispositivos
        p = Usb(0x0416, 0x5011, 0, 0x81, 0x03)
        
        p.set(align='center', bold=True, double_height=True, double_width=True)
        p.text("RAUDY ORO\n")
        p.set(align='center', bold=False, double_height=False, double_width=False)
        p.text("GINEBRA - COMPRA DE ORO\n")
        p.text("--------------------------------\n")
        p.set(align='left')
        p.text(f"Fecha: {fecha}\n")
        p.text(f"Vendedor: {nombre}\n")
        p.text(f"ID / Permiso: {id_doc}\n")
        p.text(f"Direccion: {direccion}\n")
        p.text("--------------------------------\n")
        p.text(f"Articulo: {descripcion}\n")
        p.text(f"Peso: {peso} g\n")
        p.text(f"Quilates: {quilates}\n")
        p.text(f"Precio/g: {precio_gramo:.2f} CHF\n")
        p.set(align='center', bold=True, double_height=True)
        p.text(f"TOTAL: {total:.2f} CHF\n")
        p.set(align='center', bold=False, double_height=False)
        p.text("--------------------------------\n")
        p.set(align='left')
        p.text("Declaro que este oro es mio\n")
        p.text("y no es robado.\n")
        p.text("Je declare que cet or\n")
        p.text("m'appartient et n'est pas vole.\n")
        p.text("\n\n")
        p.text("Firma Vendedor: ___________\n")
        p.text("\n")
        p.text("Firma Comprador: ___________\n")
        p.text("\n\n")
        p.text("Guardar 10 anos - Conserver 10 ans\n")
        p.text("Gracias - Merci!\n")
        p.cut()
        print(f"\n¡LISTO JEFE! Impreso. Total: {total:.2f} CHF")

    except Exception as e:
        print("\n--- NO HAY IMPRESORA, JEFE. GUARDO EN TXT ---")
        print(f"Error: {e}")
        # Si no hay impresora, guarda en archivo txt
        with open("recibo_oro.txt", "w", encoding="utf-8") as f:
            f.write("RAUDY ORO - GINEBRA\n")
            f.write(f"Fecha: {fecha}\n")
            f.write(f"Vendedor: {nombre}\n")
            f.write(f"ID: {id_doc}\n")
            f.write(f"Direccion: {direccion}\n")
            f.write(f"Articulo: {descripcion}\n")
            f.write(f"Peso: {peso} g - Quilates: {quilates}\n")
            f.write(f"Precio/g: {precio_gramo:.2f} CHF\n")
            f.write(f"TOTAL: {total:.2f} CHF\n")
            f.write("Declaro que este oro es mio y no es robado.\n")
        print("Guardado como recibo_oro.txt - lo puedes imprimir normal")

    # Guardar copia en historial
    with open("historial_oro.csv", "a", encoding="utf-8") as f:
        f.write(f"{fecha};{nombre};{id_doc};{descripcion};{peso};{quilates};{precio_gramo};{total}\n")

if __name__ == "__main__":
    while True:
        imprimir_recibo()
        otra = input("\n¿Otro recibo, jefe? (s/n): ")
        if otra.lower() != "s":
            print("¡Nos vemos, jefe! ¡A vender caro!")
            break
