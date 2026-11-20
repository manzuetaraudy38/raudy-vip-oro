//@version=6
indicator("JEFE 12 ROBOTS COMPLETO - HABLA", overlay=true, max_labels_count=500)

// ============ CONFIG, JEFE ============
emaRapidaLen = input.int(9, "EMA Rapida JEFE")
emaLentaLen = input.int(21, "EMA Lenta JEFE")
rsiLen = input.int(14, "RSI JEFE")

// ============ FUNCION DEL ROBOT, JEFE ============
getSenal(tf) =>
    c = request.security(syminfo.tickerid, tf, close)
    emaR = request.security(syminfo.tickerid, tf, ta.ema(close, emaRapidaLen))
    emaL = request.security(syminfo.tickerid, tf, ta.ema(close, emaLentaLen))
    r = request.security(syminfo.tickerid, tf, ta.rsi(close, rsiLen))
    compra = ta.crossover(emaR, emaL) and r > 50
    venta = ta.crossunder(emaR, emaL) and r < 50
    [compra, venta, emaR, emaL, r]

// ============ 12 ROBOTS, JEFE ============
// COMPRA - 6 robots, jefe
[compraM1, ventaM1, _, _, _] = getSenal("1")
[compraM5, ventaM5, _, _, _] = getSenal("5")
[compraM15, ventaM15, _, _, _] = getSenal("15")
[compraH1, ventaH1, _, _, _] = getSenal("60")
[compraH4, ventaH4, _, _, _] = getSenal("240")
// Robot 6 de COMPRA = Confirmacion total, jefe. Cuando 3 o mas dicen COMPRA, jefe
compraExtra = (compraM1 ? 1 : 0) + (compraM5 ? 1 : 0) + (compraM15 ? 1 : 0) + (compraH1 ? 1 : 0) + (compraH4 ? 1 : 0) >= 3

// VENTA - 6 robots, jefe
ventaExtra = (ventaM1 ? 1 : 0) + (ventaM5 ? 1 : 0) + (ventaM15 ? 1 : 0) + (ventaH1 ? 1 : 0) + (ventaH4 ? 1 : 0) >= 3

// ============ EMA EN PANTALLA, JEFE ============
emaR9 = ta.ema(close, emaRapidaLen)
emaL21 = ta.ema(close, emaLentaLen)
plot(emaR9, "EMA 9 JEFE", color=color.new(color.green, 0), linewidth=2)
plot(emaL21, "EMA 21 JEFE", color=color.new(color.red, 0), linewidth=2)

// ============ DIBUJA COMPRA, JEFE ============
plotshape(compraM1, title="COMPRA M1", style=shape.labelup, location=location.belowbar, color=color.green, text="C M1", textcolor=color.white, size=size.tiny)
plotshape(compraM5, title="COMPRA M5", style=shape.labelup, location=location.belowbar, color=color.green, text="C M5", textcolor=color.white, size=size.small)
plotshape(compraM15, title="COMPRA M15", style=shape.labelup, location=location.belowbar, color=color.green, text="C M15", textcolor=color.white, size=size.small)
plotshape(compraH1, title="COMPRA H1", style=shape.labelup, location=location.belowbar, color=color.green, text="C H1", textcolor=color.white, size=size.small)
plotshape(compraH4, title="COMPRA H4", style=shape.labelup, location=location.belowbar, color=color.yellow, text="C H4 JEFE", textcolor=color.black, size=size.normal)
plotshape(compraExtra, title="COMPRA EXTRA", style=shape.labelup, location=location.belowbar, color=color.new(color.green, 0), text="COMPRA JEFE", textcolor=color.white, size=size.normal)

// ============ DIBUJA VENTA, JEFE ============
plotshape(ventaM1, title="VENTA M1", style=shape.labeldown, location=location.abovebar, color=color.red, text="V M1", textcolor=color.white, size=size.tiny)
plotshape(ventaM5, title="VENTA M5", style=shape.labeldown, location=location.abovebar, color=color.red, text="V M5", textcolor=color.white, size=size.small)
plotshape(ventaM15, title="VENTA M15", style=shape.labeldown, location=location.abovebar, color=color.red, text="V M15", textcolor=color.white, size=size.small)
plotshape(ventaH1, title="VENTA H1", style=shape.labeldown, location=location.abovebar, color=color.red, text="V H1", textcolor=color.white, size=size.small)
plotshape(ventaH4, title="VENTA H4", style=shape.labeldown, location=location.abovebar, color=color.orange, text="V H4 JEFE", textcolor=color.white, size=size.normal)
plotshape(ventaExtra, title="VENTA EXTRA", style=shape.labeldown, location=location.abovebar, color=color.new(color.red, 0), text="VENTA JEFE", textcolor=color.white, size=size.normal)

// ============ TABLA EN PANTALLA, JEFE ============
var table tabla = table.new(position.top_right, 3, 7, bgcolor=color.new(color.black, 80), border_width=1, border_color=color.gray)

if barstate.islast
    table.cell(tabla, 0, 0, "ROBOT JEFE", text_color=color.yellow, text_size=size.normal)
    table.cell(tabla, 1, 0, "COMPRA", text_color=color.green, text_size=size.normal)
    table.cell(tabla, 2, 0, "VENTA", text_color=color.red, text_size=size.normal)

    table.cell(tabla, 0, 1, "M1", text_color=color.white)
    table.cell(tabla, 1, 1, compraM1 ? "✅" : "-", text_color=color.green)
    table.cell(tabla, 2, 1, ventaM1 ? "✅" : "-", text_color=color.red)

    table.cell(tabla, 0, 2, "M5", text_color=color.white)
    table.cell(tabla, 1, 2, compraM5 ? "✅" : "-", text_color=color.green)
    table.cell(tabla, 2, 2, ventaM5 ? "✅" : "-", text_color=color.red)

    table.cell(tabla, 0, 3, "M15", text_color=color.white)
    table.cell(tabla, 1, 3, compraM15 ? "✅" : "-", text_color=color.green)
    table.cell(tabla, 2, 3, ventaM15 ? "✅" : "-", text_color=color.red)

    table.cell(tabla, 0, 4, "H1", text_color=color.white)
    table.cell(tabla, 1, 4, compraH1 ? "✅" : "-", text_color=color.green)
    table.cell(tabla, 2, 4, ventaH1 ? "✅" : "-", text_color=color.red)

    table.cell(tabla, 0, 5, "H4 JEFE", text_color=color.yellow)
    table.cell(tabla, 1, 5, compraH4 ? "✅" : "-", text_color=color.green)
    table.cell(tabla, 2, 5, ventaH4 ? "✅" : "-", text_color=color.red)

    table.cell(tabla, 0, 6, "TOTAL", text_color=color.yellow)
    table.cell(tabla, 1, 6, compraExtra ? "COMPRA JEFE" : "-", text_color=color.green)
    table.cell(tabla, 2, 6, ventaExtra ? "VENTA JEFE" : "-", text_color=color.red)

// ============ ALERTAS QUE HABLAN, JEFE ============
// 6 de COMPRA, jefe
alertcondition(compraM1, title="1 COMPRA M1", message="COMPRA JEFE COMPRA M1 ORO COMPRA")
alertcondition(compraM5, title="2 COMPRA M5", message="COMPRA JEFE COMPRA M5 ORO COMPRA")
alertcondition(compraM15, title="3 COMPRA M15", message="COMPRA JEFE COMPRA M15 ORO COMPRA")
alertcondition(compraH1, title="4 COMPRA H1", message="COMPRA JEFE COMPRA H1 ORO COMPRA")
alertcondition(compraH4, title="5 COMPRA H4", message="COMPRA JEFE COMPRA H4 JEFE MANDA COMPRA")
alertcondition(compraExtra, title="6 COMPRA TOTAL", message="COMPRA JEFE COMPRA JEFE TODOS DICEN COMPRA ENTRA AHORA")

// 6 de VENTA, jefe
alertcondition(ventaM1, title="7 VENTA M1", message="VENTA JEFE VENTA M1 ORO VENTA")
alertcondition(ventaM5, title="8 VENTA M5", message="VENTA JEFE VENTA M5 ORO VENTA")
alertcondition(ventaM15, title="9 VENTA M15", message="VENTA JEFE VENTA M15 ORO VENTA")
alertcondition(ventaH1, title="10 VENTA H1", message="VENTA JEFE VENTA H1 ORO VENTA")
alertcondition(ventaH4, title="11 VENTA H4", message="VENTA JEFE VENTA H4 JEFE MANDA VENTA")
alertcondition(ventaExtra, title="12 VENTA TOTAL", message="VENTA JEFE VENTA JEFE TODOS DICEN VENTA ENTRA AHORA")
