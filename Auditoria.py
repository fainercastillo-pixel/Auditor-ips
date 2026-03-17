import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Auditor IPS Sincelejo", layout="wide")
st.title("🏥 Sistema de Auditoría RIPS - IPS")

archivo_subido = st.file_uploader("Sube el archivo Excel de la IPS", type=["xlsx"])

if archivo_subido is not None:
    # LEER EXCEL: Forzamos que DOCUMENTO y CUPS se lean como texto para evitar los .000
    df = pd.read_excel(archivo_subido, dtype={'DOCUMENTO': str, 'CUPS': str})
    
    # Limpiamos nombres de columnas y quitamos decimales residuales
    df.columns = df.columns.str.strip().str.upper()
    if 'DOCUMENTO' in df.columns:
        df['DOCUMENTO'] = df['DOCUMENTO'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)
    if 'CUPS' in df.columns:
        df['CUPS'] = df['CUPS'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)

    # Identificar errores
    errores_condicion = (df['DOCUMENTO'] == '') | (df['CUPS'] == '')
    df_errores = df[errores_condicion]
    total_errores = len(df_errores)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df))
    with col2:
        st.metric("Errores Detectados", total_errores)
    with col3:
        valor_riesgo = df.loc[errores_condicion, 'VALOR'].sum()
        st.metric("Dinero en Riesgo", f"${valor_riesgo:,.0f}")

    # Mostrar Tabla (SOLO UNA VEZ)
    st.subheader("Vista Previa de los Datos")
    st.table(df.head(10)) 

    # Botón de Descarga
    if total_errores > 0:
        st.warning(f"⚠️ Se encontraron {total_errores} registros con errores.")
        
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
        st.success("✅ ¡Excelente! No se encontraron errores.")
