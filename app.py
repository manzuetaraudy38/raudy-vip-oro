import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="RAUDY ANALISTA ORO", page_icon="🤖")
st.title("🤖 ROBOT RAUDY - ANALISTA DE ORO")
st.write("Yo analizo como el Jefe me enseñó. 5 pasos, jefe.")

# --- 1. BUSCAR DATOS ---
try:
    oro = yf.download("GC=F", period="5d", interval="1h", progress=False, auto_adjust=True)
    if isinstance(oro.columns, pd.MultiIndex):
        oro.columns = oro.columns.get_level_values(0)
    oro = oro.dropna()
except Exception as e:
    st.error("Jefe, no pude bajar el precio ahora. Dale a Refresh.")
    st.stop()

if len(oro) < 10:
    st.error("Jefe, todavía no baja el precio. Espera 1 minuto y dale a Refresh.")
    st.stop()

precio = float(oro['Close'].iloc[-1])

# Media para la tendencia
media_20 = float(oro['Close'].tail(20).mean())
media_50 = float(oro['Close'].tail(50).mean())

# --- PASO 1: TENDENCIA ---
st.subheader("1️⃣ PASO 1 - ¿PARA DÓNDE VA, JEFE?")
if precio > media_20 > media_50:
    tendencia = "SUBIENDO 🟢"
    tendencia_texto = "El oro va subiendo como escalera para arriba, jefe."
elif precio < media_20 < media_50:
    tendencia = "BAJANDO 🔴"
    tendencia_texto = "El oro va bajando como escalera para abajo, jefe. NO compres."
else:
    tendencia = "QUIETO / LADO 🟡"
    tendencia_texto = "El oro está quieto, para los lados, jefe. Esperando."

st.info(f"**Tendencia: {tendencia}** - {tendencia_texto}")

# --- PASO 2: PISO Y TECHO ---
st.subheader("2️⃣ PASO 2 - PISO Y TECHO, JEFE")
piso = float(oro['Low'].tail(50).min())
techo = float(oro['High'].tail(50).max())

st.write(f"**🟦 PISO (Soporte): ${piso:.2f}** - Si llega aquí y rebota, es bueno para comprar.")
st.write(f"**🟥 TECHO (Resistencia): ${techo:.2f}** - Si llega aquí y se choca, es bueno para vender.")
st.write(f"**Precio ahora: ${precio:.2f}** - Está a ${precio-piso:.2f} del piso y a ${techo-precio:.2f} del techo.")

# --- PASO 3: VELAS ---
st.subheader("3️⃣ PASO 3 - ¿QUÉ DICEN LAS VELAS, JEFE?")
ultima_v = oro.iloc[-1]
penultima_v = oro.iloc[-2]

def tipo_vela(v):
    if float(v['Close']) > float(v['Open']):
        return "VERDE 🟢"
    elif float(v['Close']) < float(v['Open']):
        return "ROJA 🔴"
    else:
        return "CHIQUITA 🟡"

v1 = tipo_vela(penultima_v)
v2 = tipo_vela(ultima_v)

st.write(f"Vela anterior: **{v1}**")
st.write(f"Última vela: **{v2}**")

if v1 == "VERDE 🟢" and v2 == "VERDE 🟢":
    velas_texto = "¡2 VELAS VERDES SEGUIDAS, JEFE! Los compradores están fuertes."
elif v1 == "ROJA 🔴" and v2 == "ROJA 🔴":
    velas_texto = "2 velas rojas, jefe. Los vendedores están fuertes. Peligro."
else:
    velas_texto = "Velas mezcladas, jefe. Nadie está ganando todavía."
st.write(velas_texto)

# --- PASO 4 y 5: SEÑAL FINAL ---
st.divider()
st.subheader("🚦 PASO 4 y 5 - MI DECISIÓN FINAL, JEFE:")

cerca_piso = precio < (piso + (techo-piso)*0.2)
dos_verdes = v1 == "VERDE 🟢" and v2 == "VERDE 🟢"
tendencia_buena = precio > media_20

if cerca_piso and dos_verdes and tendencia_buena:
    st.success("### 🟢 ¡COMPRA AHORA, JEFE! ¡ESTÁ BUENA!")
    entrada = precio
    stop = piso - 5
    meta = precio + (precio - stop) * 2
    st.write(f"**COMPRA EN:** ${entrada:.2f}")
    st.write(f"**SI SALE MAL, VENDE EN:** ${stop:.2f} (Solo pierdes ${entrada-stop:.2f}, jefe)")
    st.write(f"**SI SALE BIEN, VENDE EN:** ${meta:.2f} (Ganas ${meta-entrada:.2f}, jefe. El doble, jefe!)")
    st.write("**¿Qué hago, jefe?** Compra un poquito, no todo tu dinero. Con calma.")

elif tendencia == "BAJANDO 🔴":
    st.error("### 🔴 NO COMPRES, JEFE. ESTÁ BAJANDO.")
    st.write("Guarda tu plata, jefe. Espera que se pare la caída y llegue al piso.")
    st.write(f"Espera a que baje a ${piso:.2f} y ahí mira si rebota.")

else:
    st.warning("### 🟡 ESPERA, JEFE. TODAVÍA NO ESTÁ CLARA.")
    st.write("No entres a lo loco, jefe. El que espera, gana.")
    if precio > media_20:
        st.write(f"Si sube y se mantiene arriba de ${media_20:.2f}, ahí se pone buena, jefe.")
    else:
        st.write(f"Si baja a ${piso:.2f} y rebota con 2 velas verdes, ahí se pone buena, jefe.")

st.divider()
st.subheader("💰 PARA TU NEGOCIO EN LA CALLE, JEFE")
gramo = (precio / 31.1035) * 0.88
st.write(f"**24K:** {gramo:.2f} CHF/g - Tú compra a {gramo*0.75:.2f} CHF")
st.write(f"**18K:** {gramo*0.75:.2f} CHF/g - Tú compra a {gramo*0.65:.2f} CHF")
st.write(f"**14K:** {gramo*0.583:.2f} CHF/g")

st.caption("Robot Raudy - Piensa como el Jefe. No entres si dice ESPERA, jefe.")
