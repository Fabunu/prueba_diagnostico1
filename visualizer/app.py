import streamlit as st
import socket
import os
import threading
import time
from collections import Counter
import streamlite as ui
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

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
    #registro del hilo una vez al iniciar la funcion
    add_script_run_ctx(threading.current_thread())
    #mientras este activo
    while st.session_state.streaming:
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
                #detener el bucle
                st.session_state.streaming = False
                time.sleep(1)
                break


# Botón para iniciar la escucha del socket
if st.button("Iniciar Streaming") and not st.session_state.streaming:
    st.session_state.streaming = True
    ctx = get_script_run_ctx()
    hilo=threading.Thread(target=start_visualizer,daemon=True)
    add_script_run_ctx(hilo)
    hilo.start()

#Actualizar ui
with placeholder.container():
    ui.renderizar_datos(st.session_state.word_counts)

#refrescar el grafico para movimiento
if st.session_state.streaming:
    time.sleep(0.1)
    st.rerun()