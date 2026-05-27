# 1. IMAGEN BASE INDUSTRIAL
# Usamos una versión oficial y liviana (slim) de Python 3.10
FROM python:3.10-slim

# 2. DIRECTORIO DE TRABAJO
# Creamos la carpeta interna dentro del contenedor donde se alojará el software
WORKDIR /app

# 3. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA (Para compilar conectores si fuera necesario)
# Limpiamos caché inmediatamente para mantener la imagen ultra ligera (Práctica DataOps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. COPIAR REQUISITOS E INSTALAR LIBRERÍAS DE PYTHON
# Instalamos las 5 librerías clave que sostienen tu fábrica y tu frontend
RUN pip install --no-cache-dir \
    pandas \
    pydantic \
    pymysql \
    sqlalchemy \
    streamlit \
    unidecode

# 5. COPIAR EL CÓDIGO FUENTE AL CONTENEDOR
# Llevamos tus módulos, tu frontend, tu orquestador y tu carpeta de datos clínicos
COPY src/ /app/src/
COPY data/ /app/data/
COPY main.py /app/
COPY app.py /app/

# 6. EXPONER EL PUERTO DEL FRONTEND
# Streamlit usa por defecto el puerto 8501 para mostrar la interfaz web
EXPOSE 8501

# 7. COMANDO DE DISPARO POR DEFECTO
# Al encender el contenedor, este levantará inmediatamente tu aplicación web
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]