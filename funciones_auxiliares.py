import pandas as pd
import numpy as np
import re

def ingresar_genero(df):
    """ Solicita al usuario ingresar el género para cada estudiante. """
    def obtener_genero(nombre):
        genero = input(f"Ingrese el género para {nombre} (M/F): ").strip().upper()
        while genero not in ['M', 'F']:
            print("Ingrese M para masculino o F para femenino.")
            genero = input(f"Ingrese el género para {nombre} (M/F): ").strip().upper()
        return genero

    df['genero'] = df['nombre'].apply(obtener_genero)
    df['genero'] = df['genero'].map({'M': 1, 'F': 0})  # Convertir M/F a 1/0

def calcular_nro_insuficientes(observaciones):
    """ Calcula el número de insuficientes basado en las observaciones. """
    if pd.isna(observaciones):
        return np.nan
    
    if 'INS' in observaciones:
        fechas = re.findall(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', observaciones)
        return len(fechas)
    return np.nan

def calcular_nro_intentos(df):
    """ Calcula el número de intentos basado en la nota final y los insuficientes. """
    def determinar_intentos(row):
        if pd.isna(row['nota_final']):
            return 0 if pd.isna(row['nro_insuficientes']) else row['nro_insuficientes']
        else:
            return 1 if pd.isna(row['nro_insuficientes']) else 1 + row['nro_insuficientes']
    
    df['nro_intentos'] = df.apply(determinar_intentos, axis=1)

