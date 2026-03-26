#python ligero
FROM python:3.11-slim

# ver los logs del miner
ENV PYTHONUNBUFFERED=1

# se instala git en el contenedor(esto es para el pydriller)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# se define la carpeta de trabajo en el contenedor
WORKDIR /app

#copia los requerimientos para aprovevhar el cache del docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#instala librerias
RUN pip install --no-cache-dir -r requirements.txt

# copia el codigo main
COPY . .

#se eexpone el puerto del socket
EXPOSE 5000

#arranque dle miner
CMD ["python", "main.py"]