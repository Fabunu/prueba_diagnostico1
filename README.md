# prueba_diagnostico

Este proyecto es un sistema que busca cuáles son las palabras que más usan los programadores para nombrar sus funciones. Para hacerlo, se conecta a GitHub, descarga los proyectos más populares de Python y Java, y muestra un ranking en vivo con los resultados.

## cómo funciona?
El proyecto está empaquetado usando Docker para que funcione a la primera.
1. abrir una terminal y navegar a la carpeta principal del proyecto
2. se escribe el comando "docker compose up --build"
3. espera unos segundos hasta que la consola diga que el miner esta esperando la conexión
4. abre tu navegador de internet (Chrome, Firefox, etc.) y entra a esta dirección:
   http://localhost:8501
5. en la página web, haz clic en el botón "Iniciar Streaming".
6. para apagar el sistema, vuelve a la terminal y presiona Ctrl + C 

# Decisiones de diseño
Para que el proyecto funcione rápido y sea ordenado, se tomaron las siguientes decisiones:
* dos piezas separadas: El sistema está dividido en dos contenedores. Uno se encarga exclusivamente de descargar y leer el código en GitHub (el Miner), y el otro se encarga solo de dibujar la página web (Visualizer)
* conexión directa: Para que la página se actualice rapidísimo y en vivo, el Miner y el Visualizer se envían las palabras directamente a través de un túnel invisible (llamado Socket). Se decide no usar una base de datos para no hacer el sistema pesado ni lento.
* lectura inteligente: En lugar de buscar palabras a ciegas en los textos, el Miner usa herramientas especiales que entienden el código de Python y Java. Así, se asegura de extraer únicamente los nombres reales de las funciones y no palabras sueltas o comentarios.
* trabajo en segundo plano: Para que la página web no se quede "congelada" mientras espera que lleguen miles de palabras, el sistema recibe los datos por detrás (usando "hilos" o threads), dejando que la pantalla fluya libremente.

# Consideraciones
* el sistema está configurado para leer solo los últimos 10 cambios de cada proyecto y luego pasar al siguiente.
* cada vez que se inicia el programa, este le pregunta a GitHub cuáles son los 5 proyectos más famosos en ese momento exacto.
