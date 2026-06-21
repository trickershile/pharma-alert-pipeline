import os
import pandas as pd
from unidecode import unidecode

def limpiar_nombre_farmaco(texto):
    """Normaliza cadenas eliminando tildes, espacios y pasando a minúsculas[cite: 265, 266]."""
    if pd.isna(texto):
        return "no_especificado"
    return unidecode(str(texto)).strip().lower()

def ejecutar_transformacion(df_medicamentos):
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 2: SANEAMIENTO VECTORIAL Y MARCO LEGAL")
    print("="*60)
    
    if df_medicamentos is None or df_medicamentos.empty:
        print(" No hay datos para transformar.")
        return None, 0.0
        
    # INMUTABILIDAD ESTRICTA: Protegemos la fuente original clonando en memoria RAM [cite: 268, 269]
    df_proc = df_medicamentos.copy()
    print("[Pandas] Normalizando textos clínicos y aplicando Data Masking de seguridad...")
    
    # =========================================================================
    # CÁLCULO DE NUEVOS KPIs EXIGIDOS POR EL PROFESOR (KPI 3: Tasa de Imputación)
    # =========================================================================
    # Contamos cuántas celdas críticas venían vacías (NaN) en el origen antes de limpiar
    total_celdas_criticas = df_proc[['Para qué sirve', 'Dosis terapéutica', 'Dieta especial']].size
    total_nulos_detectados = df_proc[['Para qué sirve', 'Dosis terapéutica', 'Dieta especial']].isna().sum().sum()
    tasa_imputacion = (total_nulos_detectados / total_celdas_criticas) * 100
    
    # 1. GENERAR LLAVE PRIMARIA ÚNICA INCREMENTAL (Requisito SQL de producción)
    df_proc['id_medicamento'] = range(1, len(df_proc) + 1)
    
    # 2. NORMALIZAR LLAVES DE BÚSQUEDA (Match algorítmico perfecto para la IA) [cite: 267]
    df_proc['medicamento_normalizado'] = df_proc['Medicamento'].apply(limpiar_nombre_farmaco)
    df_proc['categoria_normalizada'] = df_proc['Categoría'].astype(str).str.strip().str.lower()
    
    # 3. SANEAMIENTO VECTORIAL NATIVO (Alta velocidad para grandes volúmenes de datos)
    df_proc['para_que_sirve'] = df_proc['Para qué sirve'].fillna('no especificado').astype(str).str.strip()
    df_proc['dosis_terapeutica'] = df_proc['Dosis terapéutica'].fillna('no especificado').astype(str).str.strip()
    df_proc['dosis_maxima'] = df_proc['Dosis máxima'].fillna('no especificado').astype(str).str.strip()
    df_proc['precauciones'] = df_proc['Precauciones'].fillna('ninguna').astype(str).str.strip()
    df_proc['efectos_secundarios'] = df_proc['Efectos secundarios'].fillna('no reportados').astype(str).str.strip()
    
    # 4. PRIVACIDAD POR DISEÑO (Ley N° 19.628 y Nueva Ley N° 21.719 de Datos de Salud) [cite: 276, 281, 282]
    # Reemplazamos el nulo vectorialmente antes de enmascarar
    dieta_limpia = df_proc['Dieta especial'].fillna('ninguna').astype(str).str.strip()
    
    # Optimización Vectorial de Data Masking Irreversible [cite: 283, 284]
    # Si la cadena es larga, extrae los 2 primeros y 2 últimos caracteres e inyecta la ofuscación intermedio [cite: 277, 278]
    df_proc['dieta_especial'] = dieta_limpia.all() # Inicialización por defecto
    df_proc['dieta_especial'] = dieta_limpia.get_indexer
    
    # Implementamos la máscara programática irreversible directamente en memoria [cite: 284]
    df_proc['dieta_especial'] = dieta_limpia.apply(
        lambda x: x[:2] + "****" + x[-2:] if len(x) > 4 else "****"
    )
    
    # 5. MAPEO ESTRUCTURAL FINAL DE COLUMNAS PARA PRODUCCIÓN INDUSTRIAL
    df_final = df_proc[[
        'id_medicamento', 'medicamento_normalizado', 'categoria_normalizada',
        'para_que_sirve', 'dosis_terapeutica', 'dosis_maxima',
        'precauciones', 'efectos_secundarios', 'dieta_especial'
    ]]
    
    print(f" Transformación finalizada. {len(df_final)} registros estandarizados.")
    print(f" KPI OMITIDO SUBSANADO -> Tasa de Imputación de Nulos: {tasa_imputacion:.2f}%")
    print("="*60)
    
    # Retornamos el dataframe limpio y la métrica capturada para la telemetría central
    return df_final, tasa_imputacion
