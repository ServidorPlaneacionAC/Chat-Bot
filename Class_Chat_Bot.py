import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('stopwords-es')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from unidecode import unidecode
import re
import streamlit as st

class ChatBot:
    def __init__(self):
        self.stop_words = set(stopwords.words('spanish'))
        self.palabras_personalizadas=["quien", "cuando", "donde"] #palabras que son importantes y los stopwords eliminan
        self.tipo_busqueda = {
            "Informe": ['informe', 'reporte', 'actualizar informe','tablero'],
            "Fuente de Datos": ['fuente de datos', 'base de datos', 'actualizar datos'],
            "Responsable": ['responsable', 'encargado', 'persona a cargo']
        }   #palabras para determinar el tipo de peticion

    def clasificar_tipo_peticion(self,palabras, categorias_palabras):
        '''
        Recibe como parametros una lista de palabras y un diccionario con una lista de palabras en los valores,
        las claves del diccionario son categorias, clasifica cada elemento de palabras en las categorias (claves dicc)
        retorna un diccionario indicando la compatibilidad en terminos porcentuales con cada categoria
        '''
        resultados = {}
        asignadas=0
        for categoria, palabras_clave in categorias_palabras.items():
            conteo = sum(1 for palabra in palabras if palabra in palabras_clave)
            resultados[categoria]=conteo
            asignadas=asignadas+conteo
        if asignadas >0:
            for categoria in categorias_palabras.keys():
                resultados[categoria]=(resultados[categoria]/asignadas)*100
        else:
            resultados = {}
        return resultados

    def extraer_palabras_clave(self, texto):
        '''
        extrae las palabras clave para hacer analisis de un texto
        '''
        words = word_tokenize(texto.lower())  # Convertir a minúsculas para mayor consistencia
        words=[unidecode(word) for word in words]
        palabras_clave = []

        for palabra in words:
            if palabra.isalnum() and palabra not in self.stop_words or palabra in self.palabras_personalizadas:
                palabras_clave.append(palabra)
        return palabras_clave
    
    def obtener_top(self,diccionario,n=100):
        '''
        Retorna una lista con el top n elementos, recibe un diccionario con numeros en el valor y con base en este
        genera el top 
        '''
        items_ordenados = sorted(diccionario.items(), key=lambda item: item[1], reverse=True)
        top = []  
        # st.write(items_ordenados)

        if items_ordenados[0][1]<=15 and items_ordenados[0][1]>0:
            ''' evalua los numeros donde el valor es menor a 10 y genera grupos de valores
                mostranod los todos los grupos menos el último
            '''
            valores_contados = self.contar_valores(items_ordenados)
            valores=list(valores_contados.keys())
            if len(valores_contados)>1:
                valores=list(valores_contados.keys())[:-1]
            top=[tupla[0] for tupla in items_ordenados if tupla[1] in valores]             
        else:  
            for clave, valor in items_ordenados:
                if valor != 0 and valor>15:
                    top.append(clave)            
                if len(top) == n:
                    break
            
        return top
    
    def contar_valores(self,items_ordenados):
        '''
        Permite identificar cuantos elementos de la tupla tienen la misma coincidencia
        
        Parametros:
        items_ordenados -> Lista de tuplas (categoria, coincidencia): indica las coincidencias por categoria

        Retorna:
        Diccionario -> Diccionario con los numeros en la clave y la cantidad de veces que se repite
          como valor, no toma en cuenta para el conteo los que tienen como numero 0
        '''
        conteo_valores = {}
        # Contar las repeticiones de los valores en la segunda posición de las tuplas
        for tupla in items_ordenados:
            if tupla[1]!= 0:
                valor = tupla[1]
                conteo_valores[valor] = conteo_valores.get(valor, 0) + 1
        
        # Mostrar el resultado
        # for valor, conteo in conteo_valores.items():
        #     st.write(f'El valor {valor} se repite {conteo} veces.')
        return conteo_valores
    
    def df_filtrado(self,lista,df):
        '''
        Recibe como paramtro una lista con los campos que se filtrara el df, recibe un df que se filtrará y se retorna
        como resultado
        '''
        df_lista = pd.DataFrame({'valor': lista})
        df_lista['orden'] = df_lista.index
        df_filtrado = df.merge(df_lista, left_on='Titulo', right_on='valor', how='inner')
        df_filtrado = df_filtrado.sort_values(by='orden')
        df_filtrado = df_filtrado.drop(columns='orden')
        return df_filtrado

    def es_enlace(self,cadena):
        '''
            funcion que permite determinar si un string es o no un enlace
            Retorna: True or False
        '''
        patron_enlace = re.compile(
            r'^(http|https)://'  # Protocolo http o https
            r'([a-zA-Z0-9.-]+)'  # Dominio
            r'(\.[a-zA-Z]{2,})'   # Extensión de dominio
            r'(/[a-zA-Z0-9%.-]*)*'  # Ruta opcional
            r'(\?[a-zA-Z0-9&=.-]*)*'  # Parámetros de consulta opcionales
            r'(#\w*)*$',  # Fragmento opcional
            re.IGNORECASE
        )
        
        return bool(re.match(patron_enlace, cadena))