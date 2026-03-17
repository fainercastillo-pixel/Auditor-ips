import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auditor IPS Sincelejo", layout="wide")
st.title("🏥 Sistema de Auditoría RIPS - IPS")

archivo_subido = st.file_uploader("Sube el archivo Excel de la IPS", type=["xlsx"])

if archivo_subido is not None:
    # Leemos el archivo forzando que DOCUMENTO sea texto
    df = pd.read_excel(archivo_subido, dtype={'DOCUMENTO': str})
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
    # 1. Creamos el filtro de errores para el reporte
    df_errores = df[df['DOCUMENTO'].isna() | df['CUPS'].isna()]

    st.subheader("Vista Previa de los Datos")
    st.table(df.head(10)) 

    # 2. Si hay errores, mostramos el botón de descarga
    if not df_errores.empty:
        st.warning(f"⚠️ Se encontraron {len(df_errores)} registros con errores.")
        
        # Convertimos los errores a un Excel para descargar
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_errores.to_excel(writer, index=False, sheet_name='Errores')
        
        st.download_button(
            label="📥 Descargar Reporte de Errores",
            data=output.getvalue(),
            file_name="reporte_errores_RIPS.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.success("✅ ¡Excelente! No se encontraron errores en DOCUMENTO o CUPS.")
