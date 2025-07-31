
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

st.set_page_config(page_title="Mantenimiento Diario - VITROS ECI Q", layout="centered")
st.title("🛠️ Registro de Mantenimiento VITROS ECI Q")

EXCEL_FILE = "mant_vitros_eci_q.xlsx"
RESPALDO_FILE = "respaldo_mant_vitros_eci_q.xlsx"

# Cargar o crear DataFrame
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Fecha y Hora", "Operador", "Mantenimiento Diario", "Mantenimiento Semanal", "Mantenimiento Mensual"])

# Función para respaldar
def hacer_respaldo():
    fecha_respaldo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    respaldo_path = f"respaldo_{fecha_respaldo}.xlsx"
    df.to_excel(respaldo_path, index=False)

# Formulario
with st.form("form_mantenimiento"):
    fecha_hora = st.text_input("📅 Fecha y Hora", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    operador = st.selectbox("👨‍🔧 Operador", [
        "Anibal Saavedra", "Juan Ramos", "Nycole Farias", "Stefanie Maureira", 
        "Maria J.Vera", "Felipe Fernandez", "Paula Gutierrez", 
        "Paola Araya", "Maria Rodriguez", "Pamela Montenegro"
    ])
    mant_diario = st.multiselect("🧹 Mantenimiento Diario", [
        "Vacear desechos solidos", "Limpiar sonda de lavado", "Limpiar sonda de Reactivos", 
        "Limpiar puntas de dispensado", "Retirar reactivos vacios", 
        "Cargar puntas en rotores", "Verificar inventario de reactivos"
    ])
    mant_semanal = st.multiselect("🧽 Mantenimiento Semanal", [
        "Limpiar Brazo de la muestra", "Limpiar lanzadera", 
        "Limpiar incubador-anillo-lamina calefactora-sensores int y ext", "Fibra optica"
    ])
    mant_mensual = st.multiselect("🔧 Mantenimiento Mensual", [
        "Copia de seguridad", "Revisar filtro de reactivos", 
        "Cambio cartucho de absorcion vapor", "Cambio filtro botella SLU"
    ])
    guardar = st.form_submit_button("✅ Guardar Registro")

    if guardar:
        nueva_fila = {
            "Fecha y Hora": fecha_hora,
            "Operador": operador,
            "Mantenimiento Diario": ", ".join(mant_diario),
            "Mantenimiento Semanal": ", ".join(mant_semanal),
            "Mantenimiento Mensual": ", ".join(mant_mensual)
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        hacer_respaldo()
        st.success("✅ Registro guardado correctamente.")

# Buscar por mes
st.markdown("### 🔍 Buscar registros por mes")
meses_disponibles = sorted({d[:7] for d in df["Fecha y Hora"].astype(str) if isinstance(d, str)}, reverse=True)
mes_seleccionado = st.selectbox("📆 Mes", meses_disponibles)

if mes_seleccionado:
    df_filtrado = df[df["Fecha y Hora"].astype(str).str.startswith(mes_seleccionado)]
    st.dataframe(df_filtrado, use_container_width=True)

    # Descargar Excel filtrado
    def to_excel_bytes(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    excel_filtrado = to_excel_bytes(df_filtrado)
    st.download_button(
        label="📥 Descargar Registros del Mes",
        data=excel_filtrado,
        file_name=f"registros_{mes_seleccionado}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Footer
st.markdown("---")
st.markdown("👨‍🔧 Desarrollado por Anibal Saavedra | Clínica Río Blanco")
