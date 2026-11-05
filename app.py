# ===== RAUDY - 50 ANALIZADORES + LUZ + 6 COSAS - SOLO AGREGAR, NO BORRAR NADA =====
import random

historial_senales = []  # 1. HISTORIAL DE AYER

def analizar_50_raudy(precio, eur, gbp):
    # Cada analizador vota: COMPRA / VENTA / ESPERA
    votos = []
    
    # 1 SWING - tu logica original
    if precio <= 3905: votos.append(("1 SWING", "COMPRA"))
    elif precio >= 3980: votos.append(("1 SWING", "VENTA"))
    else: votos.append(("1 SWING", "ESPERA"))

    # 2 RAPIDO - si subio 5 en 5 min = compra rapida
    if len(historial_oro) >= 2 and precio > historial_oro[-2] + 5: votos.append(("2 RAPIDO", "COMPRA"))
    elif len(historial_oro) >= 2 and precio < historial_oro[-2] - 5: votos.append(("2 RAPIDO", "VENTA"))
    else: votos.append(("2 RAPIDO", "ESPERA"))

    # 3 TENDENCIA - arriba de 3940 = subiendo
    votos.append(("3 TENDENCIA", "COMPRA" if precio > 3940 else "VENTA"))
    # 4 NOTICIAS - usa tu filtro que ya tienes
    f = filtro_noticias(precio)
    votos.append(("4 NOTICIAS", "ESPERA" if not f["puede"] else "COMPRA" if precio < 3940 else "VENTA"))
    # 5 VELAS - si esta cerca de maximo = venta
    votos.append(("5 VELAS", "VENTA" if precio >= 3970 else "COMPRA" if precio <= 3910 else "ESPERA"))
    # 6 ORO Y DOLAR - si EUR sube, ORO sube
    votos.append(("6 ORO Y DOLAR", "COMPRA" if eur > 1.115 else "VENTA"))
    # 7 SOPORTE / RESISTENCIA
    votos.append(("7 SOPORTE", "COMPRA" if precio <= 3910 else "VENTA" if precio >= 3970 else "ESPERA"))
    # 8 VOLUMEN - simulado por movimiento rapido
    votos.append(("8 VOLUMEN", "COMPRA" if len(historial_oro)>=5 and abs(precio-historial_oro[-5])>10 else "ESPERA"))
    # 9 ZONA PELIGROSA
    votos.append(("9 ZONA PELIGROSA", "ESPERA" if abs(precio-3940) < 5 else "COMPRA" if precio < 3940 else "VENTA"))
    # 10 al 49 - usan la misma logica de zonas para no romper tu app, cada uno mira un nivel diferente
    niveles_compra = [3900,3890,3865,3910,3920,3880,3870,3850,3930,3925,3905,3895,3885,3860,3840,3950,3935,3915,3902,3892]
    niveles_venta = [3980,3990,4020,3970,3960,4000,4010,4030,4040,3995,3985,3975,4005,4025,4050,3965,3992,4015,3988,4008]
    for i in range(10, 30):
        nc = niveles_compra[i-10]
        votos.append((f"{i} NIVEL {nc}", "COMPRA" if precio <= nc+5 else "ESPERA"))
    for i in range(30, 50):
        nv = niveles_venta[i-30]
        votos.append((f"{i} NIVEL {nv}", "VENTA" if precio >= nv-5 else "ESPERA"))

    # 50 MAESTRO SUPREMO - cuenta los votos
    c_compra = sum(1 for _,v in votos if v=="COMPRA")
    c_venta = sum(1 for _,v in votos if v=="VENTA")
    c_espera = sum(1 for _,v in votos if v=="ESPERA")
    
    if c_compra >= 35:
        maestro = {"señal": "👑🔥 COMPRA DIOS - LA MEJOR DEL DIA", "color": "#00ff00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE FUERTE - COMPRA DIOS"}
    elif c_venta >= 35:
        maestro = {"señal": "👑🔥 VENTA DIOS - LA MEJOR DEL DIA", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA FUERTE - VENTA DIOS"}
    elif c_compra > c_venta + 5:
        maestro = {"señal": "🟢 COMPRA FUERTE", "color": "#00aa00", "luz": "#00ff00", "texto_luz": "🟢 LUZ VERDE - COMPRA"}
    elif c_venta > c_compra + 5:
        maestro = {"señal": "🔴 VENTA FUERTE", "color": "#ff0000", "luz": "#ff0000", "texto_luz": "🔴 LUZ ROJA - VENTA"}
    else:
        maestro = {"señal": "🟡 ESPERA - LOS 50 NO ESTAN DE ACUERDO", "color": "#FFA500", "luz": "#FFA500", "texto_luz": "🟡 LUZ AMARILLA - ESPERA"}

    maestro["votos_compra"] = c_compra
    maestro["votos_venta"] = c_venta
    maestro["votos_espera"] = c_espera
    maestro["lista"] = votos
    return maestro
