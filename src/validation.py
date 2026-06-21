import os
import pandas as pd
from pydantic import BaseModel, field_validator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "logs", "errores_validacion.log")

# Asegurar la autocreación de la carpeta /logs de forma limpia
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

class MedicamentoEsquema(BaseModel):
    """Molde inviolable de control de calidad estructural y semántico[cite: 127, 128]."""
    id_medicamento: int
    medicamento_normalizado: str
    categoria_normalizada: str
    para_que_sirve: str
    dosis_terapeutica: str
    dosis_maxima: str
    precauciones: str
    efectos_secundarios: str
    dieta_especial: str

    @field_validator('medicamento_normalizado', 'categoria_normalizada')
    @classmethod
    def validar_no_vacio(cls, valor: str) -> str:
        # Frena el efecto dominó impidiendo cadenas vacías o tipos nulos ocultos de Pandas [cite: 125]
        if not valor.strip() or valor.lower() == 'nan':
            raise ValueError("Control de Gobierno: El campo mandatorio no puede estar vacío.")
        return valor

def ejecutar_etapa_validacion(df_limpio, rol_usuario="Quimico Farmaceutico"):
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 3: GOBIERNO DE DATOS Y COMPUERTA DE CALIDAD")
    print("="*60)
    
    # 1. CONTROL TÉCNICO ADICIONAL EXIGIDO POR EL DOCENTE: Validación de Roles (RBAC)
    roles_autorizados = ["DataOps Admin", "Quimico Farmaceutico"]
    if rol_usuario not in roles_autorizados:
        print(f" ❌ Error de Seguridad: El rol '{rol_usuario}' carece de privilegios de auditoría de datos.")
        return None, 100.0  # Bloqueo inmediato devolviendo tasa de error máxima
        
    print(f" [Seguridad] Acceso autorizado para el rol: '{rol_usuario}'.")

    if df_limpio is None or df_limpio.empty:
        print(" No hay datos para validar.")
        return None, 0.0

    aprobados = []
    anomalias = 0
    total_registros = len(df_limpio)

    # Limpieza previa del log de auditoría para garantizar idempotencia en cada corrida
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    print("[Pydantic] Evaluando consistencia semántica y tipado estricto fila por fila[cite: 128]...")
    for index, fila in df_limpio.iterrows():
        dict_fila = fila.to_dict()
        try:
            # Forzamos la fila al molde estricto de Pydantic
            med_certificado = MedicamentoEsquema(**dict_fila)
            aprobados.append(med_certificado.model_dump())
        except Exception as e:
            # CUARENTENA AUTOMATIZADA: Desvío lateral resiliente [cite: 135]
            anomalias += 1
            registro_error = f"❌ Fila ID {dict_fila.get('id_medicamento')} -> {dict_fila.get('medicamento_normalizado')}: {str(e)}\n"
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(registro_error)

    # =========================================================================
    # 2. CÁLCULO DE KPIs DE OBSERVABILIDAD EXIGIDOS (KPI 1: Data Error Rate) [cite: 388]
    # =========================================================================
    tasa_error_datos = (anomalias / total_registros) * 100
    UMBRAL_CRITICO = 5.0 # Límite fijado en el plan de gobernanza [cite: 389]

    print(f"\n Reporte Final de Calidad Operacional:")
    print(f"   - Total Ingerido: {total_registros} filas.")
    print(f"   - Registros Certificados: {len(aprobados)} [Aprobados hacia Carga]")
    print(f"   - Registros Rechazados: {anomalias} [Enviados a Cuarentena] [cite: 135]")
    print(f"   - Tasa de Error calculada: {tasa_error_datos:.2f}% [cite: 388]")
    
    # Evaluación del umbral crítico operativo
    if tasa_error_datos > UMBRAL_CRITICO:
        print(f" ⚠️ ALERTA CRÍTICA: La tasa de error supera el umbral tolerable del {UMBRAL_CRITICO}%. Revise las fuentes.")
    elif anomalias > 0:
        print(f" Aviso: Registros anómalos aislados de forma aislada en: {LOG_PATH} [cite: 135, 139]")
    else:
        print(" Certificación Exitosa: 100% de los datos cumplen las restricciones de negocio[cite: 128].")
        
    print("="*60)
    
    # Devolvemos el DataFrame certificado listo para el Bulk Insert de MySQL y la métrica de KPI [cite: 374]
    return pd.DataFrame(aprobados), tasa_error_datos
