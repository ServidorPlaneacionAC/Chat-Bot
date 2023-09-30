
import pandas as pd
from Class_Google_Sheet_STL import ConexionGoogleSheets
from Class_Chat_Bot import ChatBot
import streamlit as st

def ejecutar_chatbot():
    ''' etapa 1 conectar con google y traer la información'''
    clave_google = 'composed-apogee-400402-8790137483dd.json'
    id_hoja = '1WkTJBx8-4xbKcgNun6kz3qLFPWZeiJCCrip49Jaqppk'
    conexion = ConexionGoogleSheets(clave_google)
    df=conexion.obtener_dataframe(id_google_sheet=id_hoja)

    ''' Etapa 2 disponer información del df y del cliente'''
    # Crear una instancia de la clase ChatBot
    chatbot = ChatBot()
    # si las palabras no estan bien separadas para compararlas con las palabras clave ejecutar esta linea, tiene mucho costo de recursos
    df['Palabras relacionadas'] = df['Palabras relacionadas'].apply(chatbot.extraer_palabras_clave)
    # si las palabras estan bien usar esta linea
    # df['columna2'] = df['columna2'].str.split(',')
    diccionario = dict(zip(df['Titulo'], df['Palabras relacionadas'])) #genero diccionario con clave titulo y valor palabras relacionadas
    input_text = "tienes necesito"
    keywords = chatbot.extraer_palabras_clave(input_text)

    '''Iniciar análisis de mensaje'''
    requerimiento=chatbot.clasificar_tipo_peticion(keywords,diccionario) 
    if not requerimiento:
        st.write('lo siento no encuentro ninguna coincidencia con tu busqueda')
    else:
        informes=chatbot.obtener_top(requerimiento)
        df_filtrado=chatbot.df_filtrado(informes,df)
        st.write(f"Las coincidencias encontradas en orden de importancia son: .\n .\n {df_filtrado[['Titulo','Enlace','Responsable','Frecuencia de actualizacion']]}")


st.title("Aplicación con caja de texto y botón")
st.write("Hola soy el comandante, tu guia por los desarrollos en el negocio cárnico, indicame que buscas")
# Agregar una caja de texto
input_texto = st.text_input("Ingresa un texto:")

# Agregar un botón que ejecute la función mostrar_texto
if st.button("Mostrar"):
    ejecutar_chatbot()
