import streamlit as st
import pandas as pd

def configurar_interfaz():
    st.set_page_config(page_title="Frecuencia de Repositorios", layout="wide")
    st.title("Ranking de Palabras")
    st.write("Visualización de términos más usados en métodos de Python y Java.")



def renderizar_datos(word_counts):
    # Obtenemos las 10 palabras más frecuentes
    top_data = word_counts.most_common(10)
    df = pd.DataFrame(top_data, columns=["Palabra", "Frecuencia"])

    if not df.empty:
        #dos columnas
        col1, col2 = st.columns([1,2])
        with col1:
            #Lista de palabras más usadas
            st.subheader("Lista de Posiciones")
<<<<<<< HEAD
            st.dataframe(df, width= "stretch")
        with col2:
            # Gráfico de las palabras más usadas
            st.subheader("Gráfico de Frecuencias")
            st.bar_chart(df.set_index("Palabra"), width="stretch")
=======
            st.dataframe(df, use_container_width=True)
        with col2:
            # Gráfico de las palabras más usadas
            st.subheader("Gráfico de Frecuencias")
            st.bar_chart(df.set_index("Palabra"), use_container_width=True)
>>>>>>> 300303a (Estructura del visualizador con Streamlit y conexión por socket)
    else:
        st.info("Esperando datos del Miner...")