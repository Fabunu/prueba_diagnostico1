# 1. Usamos una imagen ligera de Python
FROM python:3.10-slim

# 2. Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 5. Copiamos e instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos tu código (app.py)
COPY . .

# 7. Exponemos el puerto que usa Streamlit por defecto
EXPOSE 8501

# 8. Comando para arrancar la aplicación
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]