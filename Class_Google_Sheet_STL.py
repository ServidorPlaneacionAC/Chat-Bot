import streamlit as st
import pygsheets
import pandas as pd

class ConexionGoogleSheets:
    '''
    Permite conectarse a google sheets y extraer la informacion de alli
    '''
    def __init__(self, key_path):
        self.key_path = key_path
        self.gc = pygsheets.authorize(service_file=key_path)

    def obtener_dataframe(self, id_google_sheet, hoja='Hoja 1', rango=None):
        '''
        Genera un data frame de la info que esta en al hoja de google, si tiene rango trae solamente la info del rango
        sino trae el rango especificado, por defecto el parametro hoja trae Hoja 1
        '''
        spreadsheet = self.gc.open_by_key(id_google_sheet)
        worksheet = spreadsheet.worksheet_by_title(hoja)
        if worksheet:
            if rango:
                data = worksheet.get_as_df(start=rango.split(":")[0], end=rango.split(":")[1])
            else:
                data = worksheet.get_as_df()
            return data
        else:
            return pd.DataFrame()
