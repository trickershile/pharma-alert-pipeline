from src.ingesta import ejecutar_ingesta
from src.transformation import ejecutar_transformacion
from src.validation import ejecutar_etapa_validacion
from src.loading import ejecutar_etapa_carga
import time

def correr_fabrica_dataops():
    print(" INICIANDO LÍNEA DE PRODUCCIÓN AUTOMATIZADA - PHARMAGUARD")
    tiempo_total_inicio = time.time()
    
    # 1. EJECUCIÓN ETAPA 1: INGESTA
    df_crudo = ejecutar_ingesta()
    
    if df_crudo is not None:
        # 2. EJECUCIÓN ETAPA 2: TRANSFORMACIÓN
        df_limpio = ejecutar_transformacion(df_crudo)
        
        # 3. EJECUCIÓN ETAPA 3: VALIDACIÓN
        df_certificado = ejecutar_etapa_validacion(df_limpio)
        
        # 4. EJECUCIÓN ETAPA 4: CARGA RELACIONAL EN MYSQL
        exito_operacional = ejecutar_etapa_carga(df_certificado)
        
        if exito_operacional:
            duracion_global = time.time() - tiempo_total_inicio
            print(f"\ [KPI GLOBAL MONITOREO] Pipeline ejecutado de extremo a extremo con éxito.")
            print(f" Tiempo total de procesamiento industrial: {duracion_global:.4f} segundos.")
            print(" ¡Los datos están validados y disponibles en tu servidor MySQL! Ready para la IA.\n")
        else:
            print(" Falla operacional: No se pudo escribir en el almacenamiento transaccional de MySQL.")
    else:
        print(" Falla de origen: Proceso abortado por inconsistencias en la ingesta.")

if __name__ == "__main__":
    correr_fabrica_dataops()