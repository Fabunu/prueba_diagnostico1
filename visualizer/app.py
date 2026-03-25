import streamlit as st
import socket
import os
import threading
import time
from collections import Counter
import streamlite as ui

#Configuración de conexión
HOST = os.environ.get("MINER_HOST", "miner")

PORT = 5000

#llamada a la interfaz
ui.configurar_interfaz()

#Estado de la aplicación para mantener el conteo
if 'word_counts' not in st.session_state:
    st.session_state.word_counts = Counter()
#Estado extra para saber si ya apretamos el botón
if 'streaming' not in st.session_state:
    st.session_state.streaming = False

placeholder = st.empty()

def start_visualizer():
    #Socket para conectarse al miner
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            # Buffer para acumular datos incompletos
            buffer = ""

            while True:
                #Recbimiento de datos
                data = s.recv(1024).decode("utf-8")
                if not data:
                    break

                buffer += data
                #separar contenido en base a los saltos de línea
                while "\n" in buffer:
                    word, buffer = buffer.split("\n", 1)
                    word = word.strip()
                    if word:
                        st.session_state.word_counts[word] += 1

        except Exception as e:
            st.error(f"Error de conexión: {e}")


# Botón para iniciar la escucha del socket
if st.button("Iniciar Streaming") and not st.session_state.escuchando:
    st.session_state.escuchando = True
    threading.Thread(target=start_visualizer(),daemon=True).start()

#Actualizar ui
with placeholder.container():
    ui.renderizar_datos(st.session_state.word_counts)

#refrescar el grafico para movimiento
if st.session_state.streaming:
    time.sleep(1)
    st.rerun