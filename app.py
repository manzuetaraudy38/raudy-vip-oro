import streamlit as st
from datetime import datetime

st.set_page_config(page_title="RAUDY ORO - Recibo", page_icon="💰")
st.title("💰 RAUDY ORO - GINEBRA")
st.subheader("Robot Imprimidor de Recibo")

# Formulario
nombre = st.text_input("Nombre del vendedor")
id_doc = st.text_input("No. Pasaporte / Permiso / ID")
direccion = st.text_input("Direccion")
descripcion = st.selectbox("Que es?", ["Anillo", "Cadena", "Pulsera", "Arete", "Otro"])
peso = st.number_input("Peso en gramos", min_value=0.0, step=0.1)
quilates = st.selectbox("Quilates", ["24K", "22K", "18K", "14K", "10K"])

# Precio automatico segun quilates - TU PRECIO DE COMPRA, JEFE
precios = {"24K": 55, "22K": 50, "18K": 45, "14K": 32, "10K": 22}
precio_gramo = st.number_input("Precio por gramo CHF", value=precios[quilates])

if st.button("🧾 HACER RECIBO", use_container_width=True):
    total = peso * precio_gramo
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    st.success(f"TOTAL A PAGAR: {total:.2f} CHF")
    
    recibo = f"""

    RAUDY ORO - GINEBRA

    Fecha: {fecha}
    Vendedor: {nombre}
    ID: {id_doc}
    Direccion: {direccion}

    Articulo: {descripcion}
    Peso: {peso} g
    Quilates: {quilates}
    Precio/g: {precio_gramo} CHF

    TOTAL: {total:.2f} CHF

    Declaro que este oro es mio
    y no es robado.
    Firma Vendedor: _________
    Firma Comprador: ________
    Guardar 10 anos

    """
    st.code(recibo)
    st.download_button("📥 DESCARGAR RECIBO", recibo, file_name="recibo_oro.txt")
    st.info("Dale a Imprimir en tu celular, jefe, y ya sale el papelito.")
