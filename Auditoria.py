import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Auditor IPS Sincelejo", layout="wide")

st.title("🏥 Sistema de Auditoría RIPS - IPS")
st.markdown("Sube tu archivo de facturación para detectar posibles glosas antes de enviar a la EPS.")

# Subidor de archivos
archivo_subido = st.file_uploader("Elige el archivo Excel de la IPS", type=["xlsx"])

if archivo_subido is not None:
    df = pd.read_excel(archivo_subido)
    # Esto asegura que los nombres de las columnas no tengan espacios y empiecen con Mayúscula
    # 1. Normalizamos nombres de columnas a MAYÚSCULAS
    df.columns = df.columns.str.strip().str.upper()

    # 2. Buscamos vacíos usando los nombres en MAYÚSCULAS
    errores_doc = df[df['DOCUMENTO'].isna()]
    errores_cups = df[df['CUPS'].isna()]
    total_errores = len(errores_doc) + len(errores_cups)
    
    # --- TABLERO DE CONTROL ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df))
    with col2:
        st.metric("Errores Detectados", total_errores)
    with col3:
        # Aquí también usamos MAYÚSCULAS para DOCUMENTO, CUPS y VALOR
        condicion = df['DOCUMENTO'].isna() | df['CUPS'].isna()
        valor_riesgo = df.loc[condicion, 'VALOR'].sum()
        st.metric("Dinero en Riesgo", f"${valor_riesgo:,}")

    # --- VISUALIZACIÓN ---
    st.subheader("Vista Previa de los Datos")
    st.dataframe(df.style.highlight_null(color='red')) # Resalta los errores en rojo

    if total_errores > 0:
        st.warning(f"Se encontraron {total_errores} errores. Descarga el reporte para corregir.")
        
        # Botón para descargar solo los errores
        df_errores = pd.concat([errores_doc, errores_cups]).drop_duplicates()
        st.download_button(
            label="📥 Descargar Reporte de Errores",
            data=df_errores.to_csv(index=False).encode('utf-8'),
            file_name='errores_para_corregir.csv',
            mime='text/csv',
        )
    else:
        st.success("✅ ¡Excelente! No se detectaron errores de facturación.")