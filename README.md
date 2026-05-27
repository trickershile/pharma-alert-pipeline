# 💊 PharmaGuard — Pipeline DataOps & Panel Clínico

PharmaGuard es un ecosistema automatizado de **Ingeniería de Datos y software clínico** diseñado para la ingesta, transformación, validación y despliegue de registros farmacológicos interactivos. El sistema implementa una arquitectura híbrida tolerante a fallos que procesa un dataset real de 163 medicamentos, aplicando reglas científicas de interacciones basada en el Vademécum y políticas estrictas de seguridad de la información.

---

## 🏗️ Arquitectura del Sistema (Flujo DataOps)

El proyecto está completamente modularizado bajo principios de DataOps, dividiendo el ciclo de vida del dato en 4 etapas consecutivas:

1. **Ingesta (`src/ingesta.py`)**: Extracción automatizada del archivo perimetral `medicamentos_real.csv` con tolerancia a fallos de formato humano a través del motor de Pandas (`on_bad_lines='skip'`).
2. **Transformación (`src/transformacion.py`)**: Saneamiento analítico y normalización vectorial. Remueve tildes de forma industrial (`unidecode`), unifica cadenas a minúsculas y aplica **Data Masking (Enmascaramiento de datos)** en conformidad con la **Ley N° 19.628 de Protección de la Vida Privada** en Chile.
3. **Validación (`src/validacion.py`)**: Control de calidad estricto fila por fila mediante esquemas de **Pydantic**. Si se detectan anomalías semánticas o estructurales, el registro es aislado de forma automatizada en un archivo físico (`logs/errores_validacion.log`) sin interrumpir la línea de producción.
4. **Carga (`src/carga.py`)**: Conexión relacional transaccional mediante **SQLAlchemy** e inyección masiva (*Bulk Insert*) en un servidor local **MySQL** para optimizar la latencia de red.

---

##  Tecnologías Utilizadas

* **Python 3.10**: Lenguaje núcleo del ecosistema.
* **Pandas**: Procesamiento matricial in-memory e inmutabilidad de dataframes.
* **Pydantic**: Orquestación y certificación del gobierno de datos.
* **SQLAlchemy & PyMySQL**: Capa de persistencia y conectores cliente-servidor SQL.
* **MySQL 8.0 / XAMPP**: Motor de base de datos relacional transaccional de producción.
* **Streamlit**: Frontend e interfaz gráfica interactiva para el personal de salud.
* **Docker**: Contenerización, portabilidad y aislamiento del entorno de ejecución.

---

##  KPIs Técnicos de Monitoreo (Observabilidad)

El pipeline captura métricas de rendimiento en tiempo real en cada ejecución, asegurando el cumplimiento de los objetivos de rendimiento:
* **Volumen Operacional**: 163 registros farmacológicos procesados en cascada.
* **Tolerancia a Fallos**: Skipeo automatizado de desalineaciones en el CSV de origen.
* **Latencia de Carga**: Inserción masiva en bloque optimizada para un rendimiento inferior a 1.0 segundos.
* **Garantía de Idempotencia**: Uso de políticas de limpieza estricta (`TRUNCATE TABLE`) antes de cada carga para evitar duplicidad de llaves primarias y corrupción analítica en la demo.

---

##  Estructura del Proyecto

```text
pharmaguard-pipeline/
├── data/
│   ├── medicamentos_real.csv        # Dataset clínico crudo (163 filas)
│   └── interacciones_vademecum.json # Matriz científica de alertas cruzadas
├── src/
│   ├── __init__.py                  # Inicializador del paquete Python
│   ├── ingesta.py                   # Etapa 1: Extracción perimetral
│   ├── transformacion.py            # Etapa 2: Pandas & Data Masking
│   ├── validacion.py                # Etapa 3: Pydantic & Logs de anomalías
│   └── carga.py                     # Etapa 4: SQLAlchemy & Bulk Insert MySQL
├── logs/
│   └── errores_validacion.log       # Aislamiento automatizado de registros corruptos
├── .env                             # Archivo local protegido de credenciales
├── .gitignore                       # Exclusión de basura analítica y logs locales
├── app.py                           # Frontend interactivo de consulta en Streamlit
├── Dockerfile                       # Receta de contenerización industrial slim
└── main.py                          # Orquestador y gatillo central del pipeline
 Despliegue Local Paso a Paso (Entorno de Desarrollo)
Si desea ejecutar la línea de producción y la interfaz gráfica directamente en su sistema operativo local utilizando Python y su servidor físico de MySQL (XAMPP), siga estas instrucciones:

Paso 1: Configurar el archivo de Variables de Envío (.env)
En la raíz del proyecto, asegúrese de tener un archivo llamado exactamente .env con las credenciales de acceso a su motor de base de datos local:


DB_USER="root"
DB_PASSWORD=""
DB_HOST="localhost"
DB_PORT="3306"
DB_NAME="pharmaguard_db"
Paso 2: Preparar la Base de Datos en MySQL
Abra su cliente de XAMPP, encienda el servicio MySQL, entre a su entorno (Workbench o phpMyAdmin) y cree el esquema lógico vacío ejecutando el siguiente comando SQL:

SQL
CREATE DATABASE pharmaguard_db;
Paso 3: Instalar las Dependencias de Python
Abra su terminal de Windows (PowerShell o CMD) posicionándose en la carpeta del proyecto pharma-alert-pipeline e instale las librerías necesarias con pip:

Bash
pip install pandas pydantic pymysql sqlalchemy streamlit unidecode python-dotenv
Paso 4: Ejecutar el Orquestador Central (Pipeline DataOps)
Corra el archivo principal main.py. Este script ejecutará de forma secuencial la Ingesta, la Transformación analítica (con Data Masking), la Validación estricta y el Bulk Insert en MySQL:

Bash
python main.py
Verifique en la consola que el reporte final muestre los 163 registros cargados con éxito y la latencia calculada.

Paso 5: Levantar la Aplicación Web (Frontend)
Una vez que la base de datos esté poblada, levante el panel de consulta interactivo de Streamlit ejecutando el comando a través del módulo de Python para evitar problemas de rutas en Windows:

Bash
python -m streamlit run app.py
Paso 6: Acceso al Sistema
El comando anterior abrirá automáticamente una pestaña en su navegador. Si no se despliega por sí solo, ingrese manualmente a la siguiente dirección local: http://localhost:8501

 Guía de Contingencia: Despliegue en Laboratorios de la Universidad
Las computadoras institucionales pueden tener restricciones de permisos o carecer de servicios activos como XAMPP o Docker Desktop. Para garantizar la continuidad de la demo ante la comisión, el sistema cuenta con un Plan de Resiliencia Arquitectural utilizando un motor de base de datos embebido:

Paso 1: Cambiar a Base de Datos Embebida (Plan B)
Si la computadora de la universidad no tiene XAMPP o el puerto 3306 está bloqueado, abra su archivo .env y modifique el Host escribiendo exactamente sqlite. Esto creará una base de datos física dentro de la misma carpeta de forma autónoma:


DB_USER="root"
DB_PASSWORD=""
DB_HOST="sqlite"
DB_PORT="3306"
DB_NAME="pharmaguard_db"

Paso 2: Ejecutar de Forma Directa (Sin dependencias externas)
Abra la terminal de Windows en la computadora del laboratorio y corra la línea de producción para poblar el archivo local embebido:

Bash
python main.py
Paso 3: Lanzar el Frontend Clínico
Ejecute la interfaz de Streamlit normalmente. El panel detectará el cambio arquitectural en el .env, leerá el archivo embebido y mostrará las alertas del JSON en tiempo real:

Bash
python -m streamlit run app.py