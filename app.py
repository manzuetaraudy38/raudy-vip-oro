import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="RAUDY ORO - Robot", page_icon="💰")
st.title("💰 RAUDY ORO - GINEBRA")
st.subheader("🤖 Robot Señal + Recibo")

# --- PRECIO REAL EN VIVO ---
st.header("📈 PRECIO ORO EN VIVO")
try:
    r = requests.get("https://data-asg.goldprice.org/dbXRates/USD", timeout=10)
    precio_usd_onza = r.json()['items'][0]['curr']
    precio_chf_gramo = (precio_usd_onza * 0.835) / 31.1035
    st.success(f"Precio ahora: {precio_chf_gramo:.2f} CHF / gramo 24K")
except:
    precio_chf_gramo = 95.68
    st.warning(f"Sin internet, uso precio de hoy: {precio_chf_gramo} CHF")

# --- SEÑALES ---
col1, col2 = st.columns(2)
with col1:
    compra = st.number_input("Avisame si BAJA a:", value=93.0)
with col2:
    venta = st.number_input("Avisame si SUBE a:", value=97.0)

if precio_chf_gramo <= compra:
    st.error(f"🟢 ¡JEFE, COMPRA AHORA! Esta a {precio_chf_gramo:.2f}")
elif precio_chf_gramo >= venta:
    st.error(f"🔴 ¡JEFE, VENDE AHORA! Esta a {precio_chf_gramo:.2f}")
else:
    st.info("🟡 Espera jefe, todavia no. No compres caro.")

# --- TABLA PRECIOS ---
st.header("💎 Precio por Quilates - HOY")
st.write(f"24K: {precio_chf_gramo:.2f} CHF | 22K: {precio_chf_gramo*0.916:.2f} | 18K: {precio_chf_gramo*0.75:.2f} | 14K: {precio_chf_gramo*0.585:.2f}")

# --- CALCULADORA Y RECIBO ---
st.header("🧾 Hacer Recibo")
nombre = st.text_input("Nombre vendedor")
id_doc = st.text_input("Pasaporte / ID")
descripcion = st.selectbox("Que es?", ["Anillo", "Cadena", "Pulsera", "Arete", "Otro"])
peso = st.number_input("Peso gramos", min_value=0.0, step=0.1)
quilates = st.selectbox("Quilates", ["24K", "22K", "18K", "14K", "10K"])

# Tu precio de COMPRA - para ganar, jefe
precios_compra = {"24K": 75, "22K": 68, "18K": 55, "14K": 42, "10K": 30}
precio_gramo = st.number_input("Precio que TU pagas por gramo", value=precios_compra[quilates])

if st.button("🧾 HACER RECIBO", use_container_width=True):
    total = peso * precio_gramo
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.success(f"TOTAL A PAGAR: {total:.2f} CHF")
    recibo = f"""
RAUDY ORO - GINEBRA
Fecha: {fecha}
Vendedor: {nombre}
ID: {id_doc}
Articulo: {descripcion} {quilates}
Peso: {peso} g - Precio/g: {precio_gramo} CHF
TOTAL: {total:.2f} CHF
Declaro que este oro es mio y no es robado.
Firma Vendedor: ____ Firma Comprador: ____
"""
    st.code(recibo)
    st.download_button("📥 DESCARGAR RECIBO", recibo, file_name="recibo.txt")

if st.button("🔄 Actualizar Precio"):
    st.rerun()
