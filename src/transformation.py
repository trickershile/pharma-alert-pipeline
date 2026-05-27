import pandas as pd
from unidecode import unidecode  # Elimina tildes de forma industrial para evitar fallos de encoding

# 🧠 APRENDAMOS ESTO: Las funciones de soporte van fuera de la función principal
def enmascarar_dato_sensible(texto):
    """Aplica Data Masking para cumplir con la Ley N° 19.628 de Chile."""
    texto_str = str(texto)
    # Dejamos visibles los 2 primeros y 2 últimos caracteres, ofuscando el centro con asteriscos
    if len(texto_str) > 4:
        return texto_str[:2] + "****" + texto_str[-2:]
    return "****"

def limpiar_nombre_farmaco(texto):
    """Normaliza las cadenas eliminando tildes, espacios extras y pasando a minúsculas."""
    if pd.isna(texto):
        return "no_especificado"
    # unidecode transforma 'Losartán' en 'Losartan' para asegurar el match cruzado posterior
    return unidecode(str(texto)).strip().lower()

def ejecutar_transformacion(df_medicamentos):
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 2: LIMPIEZA Y TRANSFORMACIÓN (PANDAS)")
    print("="*60)
    
    # Control de flujo perimetral
    if df_medicamentos is None or df_medicamentos.empty:
        print(" No hay datos para transformar.")
        return None
        
    # INMUTABILIDAD: Clonamos la estructura para proteger el estado de la data cruda original
    df_proc = df_medicamentos.copy()
    print("[Pandas] Normalizando textos clínicos y aplicando Data Masking de seguridad...")
    
    # 1. GENERAR LLAVE PRIMARIA ÚNICA INCREMENTAL (Requisito SQL)
    df_proc['id_medicamento'] = range(1, len(df_proc) + 1)
    
    # 2. NORMALIZAR LLAVES DE BÚSQUEDA (Usa nuestra función con unidecode)
    df_proc['medicamento_normalizado'] = df_proc['Medicamento'].apply(limpiar_nombre_farmaco)
    df_proc['categoria_normalizada'] = df_proc['Categoría'].astype(str).str.strip().str.lower()
    
    # 3. DATA QUALITY: Tratamiento estricto de nulos en descripciones extensas
    df_proc['para_que_sirve'] = df_proc['Para qué sirve'].fillna('no especificado').astype(str).str.strip()
    df_proc['dosis_terapeutica'] = df_proc['Dosis terapéutica'].fillna('no especificado').astype(str).str.strip()
    df_proc['dosis_maxima'] = df_proc['Dosis máxima'].fillna('no especificado').astype(str).str.strip()
    df_proc['precauciones'] = df_proc['Precauciones'].fillna('ninguna').astype(str).str.strip()
    df_proc['efectos_secundarios'] = df_proc['Efectos secundarios'].fillna('no reportados').astype(str).str.strip()
    
    #  APRENDAMOS ESTO: Aquí corregimos el error. Rellenamos el nulo y aplicamos la ofuscación
    df_proc['dieta_especial_cruda'] = df_proc['Dieta especial'].fillna('ninguna').astype(str).str.strip()
    df_proc['dieta_especial'] = df_proc['dieta_especial_cruda'].apply(enmascarar_dato_sensible)
    
    # 4. MAPEO ESTRUCTURAL FINAL DE COLUMNAS
    df_final = df_proc[[
        'id_medicamento', 'medicamento_normalizado', 'categoria_normalizada',
        'para_que_sirve', 'dosis_terapeutica', 'dosis_maxima',
        'precauciones', 'efectos_secundarios', 'dieta_especial'
    ]]
    
    print(f" Transformación finalizada. {len(df_final)} registros estandarizados.")
    print("="*60)
    return df_final