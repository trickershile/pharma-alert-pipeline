from pydantic import BaseModel, field_validator
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "logs", "errores_validacion.log")

# Asegurar la autocreación de la carpeta /logs
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

class MedicamentoEsquema(BaseModel):
    """Molde de control de calidad estructural y semántico."""
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
        if not valor.strip() or valor.lower() == 'nan':
            raise ValueError("Control de Calidad: El campo mandatorio no puede estar vacío.")
        return valor

def ejecutar_etapa_validacion(df_limpio):
    print("\n" + "="*60)
    print(" DATAOPS PIPELINE - ETAPA 3: VALIDACIÓN (PYDANTIC)")
    print("="*60)
    
    if df_limpio is None or df_limpio.empty:
        print(" No hay datos para validar.")
        return None

    aprobados = []
    anomalias = 0

    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    print("[Pydantic] Evaluando consistencia semántica fila por fila...")
    for index, fila in df_limpio.iterrows():
        dict_fila = fila.to_dict()
        try:
            # Forzamos la fila al molde estricto
            med_certificado = MedicamentoEsquema(**dict_fila)
            aprobados.append(med_certificado.model_dump())
        except Exception as e:
            # MANEJO DE ANOMALÍAS: Captura el error de la fila y lo desvía al log
            anomalias += 1
            registro_error = f"❌ Fila ID {dict_fila.get('id_medicamento')} -> {dict_fila.get('medicamento_normalizado')}: {str(e)}\n"
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(registro_error)

    print(f"\n Reporte Final de Calidad:")
    print(f"   - Registros Certificados: {len(aprobados)}")
    print(f"   - Registros Rechazados: {anomalias}")
    
    if anomalias > 0:
        print(f" Alerta: Registros anómalos aislados en: {LOG_PATH}")
    else:
        print(" Certificación Completa: 100% de los datos cumplen con el estándar.")
    print("="*60)
    return pd.DataFrame(aprobados)