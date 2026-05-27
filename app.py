import streamlit as st
import pandas as pd
import json
import os
from sqlalchemy import create_engine

# 1. METADATOS Y CONFIGURACIÓN DE LA INTERFAZ WEB
st.set_page_config(
    page_title="PharmaGuard Dashboard",
    page_icon="💊",
    layout="wide"
)

# CREDENCIALES DE CONEXIÓN A TU MOTOR LOCAL MYSQL
DB_USER = "root"
DB_PASSWORD = "123456789"  # ⚠️ Recuerda colocar tu contraseña de MySQL aquí si configuraste una
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "pharmaguard_db"

# RUTAS DINÁMICAS PARA EL VADEMÉCUM CIENTÍFICO
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "interacciones_vademecum.json")

def obtener_datos_mysql():
    """Establece conexión con el motor relacional y extrae los medicamentos."""
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string)
    query = "SELECT * FROM inventario_medicamentos;"
    return pd.read_sql(query, con=engine)

def cargar_vademecum_completo():
    """Lee las reglas científicas documentales del archivo JSON perimetral."""
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("reglas", [])
    return []

# 2. DISEÑO VISUAL DE LA SOLUCIÓN CLÍNICA
st.title("💊 PharmaGuard — Panel de Consulta Clínica")
st.markdown("---")

try:
    # Extracción en tiempo real desde ambas fuentes (Arquitectura Híbrida)
    df_meds = obtener_datos_mysql()
    reglas_vademecum = cargar_vademecum_completo()
    
    # KPI Visual en la cabecera
    st.metric(label="Total de Medicamentos Validados en Sistema", value=len(df_meds))
    
    st.subheader("🔍 Buscador Inteligente de Fármacos")
    
    # Caja de texto interactiva para el usuario clínico
    busqueda = st.text_input("Escribe el nombre del medicamento que deseas consultar (ej: clorfenamina, losartan, omeprazol):")
    
    if busqueda:
        # Normalizamos la entrada del usuario para que calce con la limpieza de Pandas
        termino = busqueda.strip().lower()
        
        # Filtrado del DataFrame usando Pandas
        resultado = df_meds[df_meds['medicamento_normalizado'].str.contains(termino, na=False)]
        
        if not resultado.empty:
            for index, fila in resultado.iterrows():
                nombre_med = fila['medicamento_normalizado']
                
                # Desplegable elegante para cada fármaco encontrado
                with st.expander(f"📋 Ficha Técnica: {nombre_med.upper()} ({fila['categoria_normalizada'].capitalize()})"):
                    
                    # 🧠 EL CRUCE CIENTÍFICO: Buscamos si el fármaco actual está involucrado en el JSON
                    alertas_encontradas = [
                        r for r in reglas_vademecum 
                        if r["componente_1"] == nombre_med or r["componente_2"] == nombre_med
                    ]
                    
                    # Si existen alertas farmacológicas, las desplegamos de forma prioritaria en recuadros rojos
                    if alertas_encontradas:
                        for alerta in alertas_encontradas:
                            # Identificamos el contra-componente para avisarle al médico con claridad
                            otro_componente = alerta['componente_2'] if alerta['componente_1'] == nombre_med else alerta['componente_1']
                            
                            st.error(
                                f"⚠️ **ALERTA DE INTERACCIÓN FARMACOLÓGICA ({alerta['nivel_riesgo'].upper()})**\n\n"
                                f"**Combinación crítica detectada:** {nombre_med.upper()} + {otro_componente.upper()}\n\n"
                                f"**Descripción clínica del riesgo:** {alerta['descripcion']}"
                            )
                    
                    # Despliegue en columnas del resto del dataset que limpiamos del CSV
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**🔹 ¿Para qué sirve?:** {fila['para_que_sirve']}")
                        st.markdown(f"**🔹 Dosis Terapéutica:** {fila['dosis_terapeutica']}")
                        st.markdown(f"**🔹 Dosis Máxima Diaria:** {fila['dosis_maxima']}")
                        
                    with col2:
                        st.markdown(f"**⚠️ Precauciones:** {fila['precauciones']}")
                        st.markdown(f"**🚫 Efectos Secundarios:** {fila['efectos_secundarios']}")
                        st.markdown(f"**🍏 Dieta Especial (Data Masking):** {fila['dieta_especial']}")
        else:
            st.warning("⚠️ No se encontraron registros que coincidan con ese término en la base de datos.")
            
    st.markdown("---")
    
    # 3. OBSERVABILIDAD DE DATOS (TABLA GLOBAL RELACIONAL)
    st.subheader("📊 Vista General de la Base de Datos Relacional")
    st.dataframe(df_meds, use_container_width=True)

except Exception as e:
    st.error(f"🚨 Error operacional en el Frontend: {str(e)}")
    st.info("💡 Asegúrate de haber ejecutado 'python main.py' previamente para levantar las tablas en MySQL.")