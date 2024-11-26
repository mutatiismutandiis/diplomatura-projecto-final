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
        fechas = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', observaciones)
        return len(fechas)
    return np.nan

def calcular_nro_intentos(df):
    """ Calcula el número de intentos basado en la nota final y los insuficientes. """
    def determinar_intentos(row):
        if pd.isna(row['nota_final']):
            return row['nro_insuficientes']
        else:
            return 1 + row['nro_insuficientes']
    
    df['nro_intentos'] = df.apply(determinar_intentos, axis=1)

def procesar_nota_parciales(parcial, recuperatorio):
    """ Procesa las notas de un parcial y su recuperatorio, eligiendo la mayor y convirtiéndola al formato de 0 a 10. """
    # Convertir guiones a NaN para poder hacer comparaciones numéricas
    parcial = pd.to_numeric(str(parcial).replace('*', ''), errors='coerce')
    recuperatorio = pd.to_numeric(str(recuperatorio).replace('*', ''), errors='coerce')


    # Si ambos son NaN, retornar NaN
    if np.isnan(parcial) and np.isnan(recuperatorio):
        return np.nan
    
    # Si uno es NaN, tomar el otro y dividir por 10
    if np.isnan(parcial):
        return round(recuperatorio / 10, 2)
    if np.isnan(recuperatorio):
        return round(parcial / 10, 2)
    
    # Si ambos son numéricos, tomar el mayor y dividir por 10
    return round(max(parcial, recuperatorio) / 10, 2)

def procesar_notas_con_dos_rec(parcial, rec1, rec2):
    """ Procesa las notas de un parcial con dos recuperatorios, eligiendo la mayor y convirtiéndola al formato de 0 a 10. """
    # Eliminar asteriscos si existen y convertir guiones y celdas vacías a NaN
    notas = pd.to_numeric([str(parcial).replace('*', ''), str(rec1).replace('*', ''), str(rec2).replace('*', '')], errors='coerce')

    # Filtrar solo valores numéricos válidos
    notas = [nota for nota in notas if not np.isnan(nota)]

    # Si no hay valores numéricos válidos, retornar NaN
    if not notas:
        return np.nan
    
    # Tomar el mayor valor y dividirlo por 10, retornando el resultado redondeado
    return round(max(notas) / 10, 2)

def limpiar_nota(nota):
    """ Limpia la nota eliminando la fecha entre paréntesis y convirtiéndola en un número. """
    # Eliminar el texto entre paréntesis y convertir a número
    nota = re.sub(r'\s*\(.*\)', '', str(nota)).strip()
    return pd.to_numeric(nota, errors='coerce')
