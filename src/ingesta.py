import pandas as pd
import os
import time

# DEFINICIÓN DE RUTAS DINÁMICAS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "medicamentos_real.csv")

def extraer_csv_operativo():
    """Busca el CSV y lo lee manejando la codificación y saltando líneas corruptas."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Error: No existe el archivo CSV en {CSV_PATH}")
    
    try:
        # Intentamos UTF-8 e ignoramos filas desalineadas (ej: comas extras de tipeo humano)
        return pd.read_csv(CSV_PATH, encoding="utf-8", on_bad_lines='skip')
    except Exception:
        # Respaldo en Latin-1 para tolerar tildes y caracteres especiales del español
        return pd.read_csv(CSV_PATH, encoding="latin-1", on_bad_lines='skip')

def ejecutar_ingesta():
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 1: INGESTA DE DATOS")
    print("="*60)
    
    tiempo_inicio = time.time()
    try:
        print("[Python] Extrayendo registros desde el archivo perimetral...")
        df_medicamentos = extraer_csv_operativo()
        
        latencia = time.time() - tiempo_inicio
        print(f" Ingesta finalizada con éxito.")
        print(f" Registros absorbidos: {len(df_medicamentos)} filas clínicas.")
        print(f" Latencia de Ingesta: {latencia:.4f} segundos.")
        print("="*60)
        return df_medicamentos
    except Exception as e:
        print(f" Error crítico en la Ingesta: {str(e)}")
        print("="*60)
        return None