import os
import time
import json
import pandas as pd

# 1. DEFINICIÓN DE RUTAS DINÁMICAS (Evita rutas absolutas rígidas de un solo PC)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "Medicamentos_.csv") # Coincide con tu archivo real físico
JSON_PATH = os.path.join(BASE_DIR, "data", "interacciones_vademecum.json")

def extraer_csv_operativo():
    """Busca el CSV de inventario local y lo lee aplicando tolerancia a fallos."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Error: No existe el archivo CSV transaccional en {CSV_PATH}")
    
    try:
        # Intentamos UTF-8 e ignoramos filas desalineadas (comas extras de tipeo humano)
        return pd.read_csv(CSV_PATH, encoding="utf-8", on_bad_lines='skip')
    except Exception:
        # Respaldo en Latin-1 para tolerar tildes de registros clínicos del español
        return pd.read_csv(CSV_PATH, encoding="latin-1", on_bad_lines='skip')

def extraer_json_cientifico():
    """Busca y carga la matriz documental de interacciones farmacológicas."""
    if not os.path.exists(JSON_PATH):
        raise FileNotFoundError(f"Error: No existe la matriz científica JSON en {JSON_PATH}")
        
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        with open(JSON_PATH, "r", encoding="latin-1") as f:
            return json.load(f)

def ejecutar_ingesta():
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 1: INGESTA HÍBRIDA (DESACOPLADA)")
    print("="*60)
    
    tiempo_inicio = time.time()
    try:
        # A. Absorción del Inventario Físico (Estructura Plana/Tabular)
        print("[Pandas] Extrayendo registros desde el archivo perimetral CSV...")
        df_medicamentos = extraer_csv_operativo()
        
        # B. Absorción de la Matriz Médica (Estructura Jerárquica/Multidimensional)
        print("[JSON] Consumiendo matriz científica global de interacciones...")
        dict_vademecum = extraer_json_cientifico()
        
        latencia = time.time() - tiempo_inicio
        print(f" Ingesta híbrida finalizada con éxito.")
        print(f" -> Lote operativo: {len(df_medicamentos)} filas clínicas absorbidas.")
        print(f" -> Matriz científica: {len(dict_vademecum)} principios activos indexados.")
        print(f" Latencia de Ingesta: {latencia:.4f} segundos.")
        print("="*60)
        
        # Retornamos ambas estructuras para alimentar las transformaciones vectoriales
        return df_medicamentos, dict_vademecum
        
    except Exception as e:
        print(f" Error crítico en la Ingesta Híbrida: {str(e)}")
        print("="*60)
        return None, None
