import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="RAUDY SEÑAL ORO", page_icon="🟡")
st.title("🟡 RAUDY - SEÑAL DE ORO")
st.write("Te digo CUÁNDO comprar, jefe. No antes.")

# 1. Buscar precio del oro
oro = yf.download("GC=F", period="5d", interval="15m", progress=False)
precio = float(oro['Close'].iloc[-1])
precio_antes = float(oro['Close'].iloc[-20])
media = float(oro['Close'].tail(20).mean())

# 2. Calcular si está subiendo o bajando
cambio = ((precio - precio_antes) / precio_antes) * 100
minimo = float(oro['Close'].tail(20).min())

st.metric("PRECIO ORO AHORA", f"${precio:.2f}", f"{cambio:.2f}%")

# 3. LA SEÑAL - 3 reglas, jefe
st.subheader("🚦 TU SEÑAL, JEFE:")

cond1 = precio > minimo + 5  # Ya se paró la caída
cond2 = precio > media  # Ya está subiendo por encima del promedio
cond3 = cambio > -0.5  # No está cayendo fuerte

if cond1 and cond2:
    st.success("🟢 ¡COMPRA AHORA, JEFE! El oro se paró y empezó a subir.")
    st.write("**¿Qué hacer?** Compra un poquito, no todo tu dinero, jefe.")
elif cambio < -1:
    st.error("🔴 NO COMPRES, JEFE. El oro está cayendo fuerte.")
    st.write("**¿Qué hacer?** Quédate quieto, guarda tu plata, jefe.")
else:
    st.warning("🟡 ESPERA, JEFE. Todavía no está claro.")
    st.write("**¿Qué hacer?** No hagas nada. Espera la luz verde, jefe.")

st.divider()
st.write(f"Precio mínimo reciente: ${minimo:.2f}")
st.write(f"Promedio: ${media:.2f}")
st.write("Si el precio está por encima del promedio = bueno para comprar, jefe.")

# 4. Para tu negocio en la calle, jefe
st.divider()
st.subheader("💰 PARA TU NEGOCIO EN CHF, JEFE")
gramo_24k = (precio / 31.1035) * 0.88
st.write(f"**24K:** {gramo_24k:.2f} CHF / gramo - Tú compra a {gramo_24k*0.75:.2f} CHF")
st.write(f"**18K:** {gramo_24k*0.75:.2f} CHF / gramo")
st.write(f"**14K:** {gramo_24k*0.583:.2f} CHF / gramo")
st.caption("Así sabes cuánto pagarle al cliente, jefe, sin que te engañen.")
