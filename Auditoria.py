import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditor IPS Sincelejo", layout="wide")
st.title("🏥 Sistema de Auditoría RIPS - IPS")

archivo_subido = st.file_uploader("Sube el archivo Excel de la IPS", type=["xlsx"])

if archivo_subido is not None:
    df = pd.read_excel(archivo_subido)
    df.columns = df.columns.str.strip().str.upper()

    # Buscamos los errores
    errores_doc = df[df['DOCUMENTO'].isna()]
    errores_cups = df[df['CUPS'].isna()]
    total_errores = len(errores_doc) + len(errores_cups)
    
    # Mostramos las métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df))
    with col2:
        st.metric("Errores Detectados", total_errores)
    with col3:
        condicion = df['DOCUMENTO'].isna() | df['CUPS'].isna()
        valor_riesgo = df.loc[condicion, 'VALOR'].sum()
        st.metric("Dinero en Riesgo", f"${valor_riesgo:,}")

    # Mostramos la tabla
    st.subheader("Vista Previa de los Datos")
    st.table(df)
