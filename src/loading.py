import os
import time
from sqlalchemy import create_engine, text
import pandas as pd

# CONFIGURACIÓN DE CONEXIÓN A MYSQL (Modifica según tus credenciales si es necesario)
DB_USER = "root"
DB_PASSWORD = "123456789"          # Coloca tu contraseña de MySQL aquí si tienes una
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "pharmaguard_db" # Asegúrate de que esta base de datos exista en tu MySQL

def ejecutar_etapa_carga(df_certificado):
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 4: CARGA TRANSACCIONAL (MYSQL)")
    print("="*60)
    
    if df_certificado is None or df_certificado.empty:
        print(" No hay datos certificados para cargar.")
        return False

    tiempo_inicio = time.time()
    try:
        # 1. Crear la cadena de conexión (Connection String) para MySQL usando PyMySQL
        connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        print(f"[MySQL] Conectando al servidor relacional en {DB_HOST}:{DB_PORT}...")
        engine = create_engine(connection_string)
        
        # 2. IDEMPOTENCIA: Conectamos para limpiar la tabla antes de la demo y evitar llaves duplicadas
        with engine.connect() as conn:
            print("[MySQL] Asegurando limpieza de registros previos...")
            # Creamos la tabla de forma automática si no existía con la estructura correcta
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS inventario_medicamentos (
                    id_medicamento INT PRIMARY KEY,
                    medicamento_normalizado VARCHAR(255) NOT NULL,
                    categoria_normalizada VARCHAR(255) NOT NULL,
                    para_que_sirve TEXT,
                    dosis_terapeutica TEXT,
                    dosis_maxima TEXT,
                    precauciones TEXT,
                    efectos_secundarios TEXT,
                    dieta_especial TEXT
                );
            """))
            # Vaciamos la tabla para que la demo corra limpia e idéntica cada vez
            conn.execute(text("TRUNCATE TABLE inventario_medicamentos;"))
            conn.commit()

        print(f"[MySQL] Insertando masivamente (Bulk Insert) {len(df_certificado)} registros clínicos...")
        
        # 3. BULK INSERT: Pandas inyecta el DataFrame completo de un solo golpe en MySQL
        df_certificado.to_sql(
            name="inventario_medicamentos", 
            con=engine, 
            if_exists="append", 
            index=False
        )
        
        latencia = time.time() - tiempo_inicio
        print(" Carga masiva en MySQL completada con éxito.")
        print(f" Latencia de Carga: {latencia:.4f} segundos.")
        print("="*60)
        return True
        
    except Exception as e:
        print(f" Error crítico en la fase de Carga hacia MySQL: {str(e)}")
        print(" Consejo: Asegúrate de haber creado la base de datos ejecutando en MySQL: CREATE DATABASE pharmaguard_db;")
        print("="*60)
        return False