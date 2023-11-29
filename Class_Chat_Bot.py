import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('stopwords-es')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from unidecode import unidecode

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
    
    def obtener_top(self,diccionario,n=3):
        '''
        Retorna una lista con el top 3 elementos, recibe un diccionario con numeros en el valor y con base en este
        genera el top 
        '''
        items_ordenados = sorted(diccionario.items(), key=lambda item: item[1], reverse=True)
        top = []        
        for clave, valor in items_ordenados:
            if valor != 0:
                top.append(clave)            
            if len(top) == n:
                break
        
        return top
    
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
