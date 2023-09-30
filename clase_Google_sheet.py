import gspread
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

class ConexionGoogleSheets:
    '''
    Clase para conectarse con google sheets y obtener dataframes a partir de la informacion en las hojas del libro
    para conectarse con el usuario, se debe compartir el libro con este correo: cuenta-de-servicio-chat-bot1@composed-apogee-400402.iam.gserviceaccount.com
    es posible que si es un usuario diferente se deba asignar un rol desde google cloud como editos al proyecto chat-bot1 para que pueda acceder
    con esta clave y correo dados
    '''
    def __init__(self, key_path):
        '''
        este constructor Permite generar conexion a las hojas de google sheet, solo se necesita crear la llave de autenticacion(parametro)
        y la credencial de acceso de google cloud(configuracion en google cloud), este video explica como hacer lo que hay en este metodo y el
        de obtener dataframe https://www.youtube.com/watch?v=jeZWv5PQJAk 
        '''
        self.key_path = key_path
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = service_account.Credentials.from_service_account_file(key_path, scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.service.spreadsheets()

    def obtener_dataframe(self, id_google_sheet, hoja='Hoja 1', rango=None):
        '''
        Retorna un dataframe a partir del id hoja de google sheet que se pasa por parametro, usando la conexion que se creo en el constructor, 
        el rango se debe pasar en este formato 'A1:B5' y lo toma de la hoja que se pasa por parametro
        '''
        if rango is None:
            # Obtener todos los valores en la hoja especificada
            result = self.sheet.values().get(spreadsheetId=id_google_sheet, range=hoja).execute()
            values = result.get('values', [])
        else:
            # Obtener los valores en el rango especificado
            result = self.sheet.values().get(spreadsheetId=id_google_sheet, range=f'{hoja}!{rango}').execute()
            values = result.get('values', [])

        # Crear un DataFrame a partir de los valores
        if values:
            df = pd.DataFrame(values[1:], columns=values[0])
        else:
            df = pd.DataFrame()

        return df
