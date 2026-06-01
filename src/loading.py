import os
import time
from sqlalchemy import create_engine, text
import pandas as pd

# CONFIGURACIÓN DE CONEXIÓN (Al escribir "sqlite" en DB_HOST se activará el Plan B local)
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "sqlite"  # <- Mantén "sqlite" para la u, o cambia a "localhost" si usas XAMPP
DB_PORT = "3306"
DB_NAME = "pharmaguard_db"

def ejecutar_etapa_carga(df_certificado):
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 4: CARGA TRANSACCIONAL (POLÍGLOTA)")
    print("="*60)
    
    if df_certificado is None or df_certificado.empty:
        print(" No hay datos certificados para cargar.")
        return False

    tiempo_inicio = time.time()
    try:
        # 1. DETECTAR EL MOTOR DE BASE DE DATOS (SWITCH AUTOMÁTICO)
        if DB_HOST.lower() == "sqlite":
            print("[SQLite] Activando Plan de Contingencia - Base de datos embebida local...")
            connection_string = "sqlite:///pharmaguard_db.db"
            engine = create_engine(connection_string)
        else:
            print(f"[MySQL] Conectando al servidor relacional en {DB_HOST}:{DB_PORT}...")
            connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            engine = create_engine(connection_string)
        
        # 2. IDEMPOTENCIA: Estructura y limpieza adaptada al motor seleccionado
        with engine.connect() as conn:
            print(f"[{'SQLite' if DB_HOST.lower() == 'sqlite' else 'MySQL'}] Asegurando limpieza de registros previos...")
            
            # Crear la tabla si no existe (Sintaxis compatible con ambos motores)
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
            
            # Limpieza limpia según el motor para evitar fallos de sintaxis
            if DB_HOST.lower() == "sqlite":
                conn.execute(text("DELETE FROM inventario_medicamentos;"))
            else:
                conn.execute(text("TRUNCATE TABLE inventario_medicamentos;"))
                
            conn.commit()

        print(f"[{'SQLite' if DB_HOST.lower() == 'sqlite' else 'MySQL'}] Insertando masivamente (Bulk Insert) {len(df_certificado)} registros clínicos...")
        
        # 3. BULK INSERT
        df_certificado.to_sql(
            name="inventario_medicamentos", 
            con=engine, 
            if_exists="append", 
            index=False
        )
        
        latencia = time.time() - tiempo_inicio
        print(f" Carga masiva en {'SQLite' if DB_HOST.lower() == 'sqlite' else 'MySQL'} completada con éxito.")
        print(f" Latencia de Carga: {latencia:.4f} segundos.")
        print("="*60)
        return True
        
    except Exception as e:
        print(f" Error crítico en la fase de Carga: {str(e)}")
        print("="*60)
        return False
