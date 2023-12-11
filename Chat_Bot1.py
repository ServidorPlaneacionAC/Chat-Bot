
import pandas as pd
from Class_Google_Sheet_STL import ConexionGoogleSheets
from Class_Chat_Bot import ChatBot
import streamlit as st

def ejecutar_chatbot(input_text):
    # ''' etapa 1 conectar con google y traer la información'''
    clave_google = 'composed-apogee-400402-8790137483dd.json'
    id_hoja = '1WkTJBx8-4xbKcgNun6kz3qLFPWZeiJCCrip49Jaqppk'
    conexion = ConexionGoogleSheets(clave_google)
    df=conexion.obtener_dataframe(id_google_sheet=id_hoja)

    # ''' Etapa 2 disponer información del df y del cliente'''
    # Crear una instancia de la clase ChatBot
    chatbot = ChatBot()
    # evaluo si el input es un enlace
    if chatbot.es_enlace(input_text):
        df=df[df['Enlace'] == input_text]
        if df.shape[0]==0:
            st.write('lo siento no encuentro ninguna coincidencia con tu busqueda')
        else:
            st.dataframe(df[['Titulo','Enlace','Responsable','Frecuencia de actualizacion']])
    else:
        # si las palabras no estan bien separadas para compararlas con las palabras clave ejecutar esta linea, tiene mucho costo de recursos
        df['Palabras relacionadas'] = df['Palabras relacionadas'].apply(chatbot.extraer_palabras_clave)
        # si las palabras estan bien usar esta linea
        # df['columna2'] = df['columna2'].str.split(',')
        diccionario = dict(zip(df['Titulo'], df['Palabras relacionadas'])) #genero diccionario con clave titulo y valor palabras relacionadas
        keywords = chatbot.extraer_palabras_clave(input_text)

        # '''Iniciar análisis de mensaje'''
        requerimiento=chatbot.clasificar_tipo_peticion(keywords,diccionario) 
        if not requerimiento:
            st.write('lo siento no encuentro ninguna coincidencia con tu busqueda')
        else:
            informes=chatbot.obtener_top(requerimiento)
            df_filtrado=chatbot.df_filtrado(informes,df)
            st.write(f"Lass coincidencias encontradas en orden de importancia son: .\n .\n ")
            
            # Crear una nueva columna con enlaces formateados en Markdown
            df_filtrado['Enlace'] = df_filtrado['Enlace'].apply(lambda x: (f"[{x}]( {x} )"))
            
            # Mostrar el DataFrame en Streamlit con la nueva columna de enlaces formateados
            st.dataframe(df_filtrado[['Titulo', 'Enlace', 'Responsable', 'Frecuencia de actualizacion']])
            for index, row in df_filtrado.iterrows():
                st.write(f"**{row['Titulo']}**")
                st.markdown(f"{row['Enlace']}")
                st.write(f"Responsable: {row['Responsable']}")
                st.write(f"Frecuencia de actualización: {row['Frecuencia de actualizacion']}")
                st.write("---")
            # st.dataframe(df_filtrado[['Titulo','Enlace','Responsable','Frecuencia de actualizacion']])



st.title("Explorador de modelos Cárnicos")
st.write("Hola soy tu guia por los desarrollos en el negocio cárnico, indicame que buscas")
# Agregar una caja de texto
input_texto = st.text_input("Cuentame que buscas")

# Define la URL de tu sitio de Google Sites
#google_sites_url = "http://www.calendario-colombia.com/calendario-2023"

# Crea un iframe para mostrar el sitio de Google Sites
# st.write(f'<iframe src="{google_sites_url}" width="800" height="600"></iframe>', unsafe_allow_html=True)


# Agregar un botón que ejecute la función mostrar_texto
if st.button("Mostrar"):
    ejecutar_chatbot(input_texto)
