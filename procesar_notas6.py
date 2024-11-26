import pandas as pd
import numpy as np
import os
from funciones_auxiliares import ingresar_genero, calcular_nro_insuficientes, calcular_nro_intentos, procesar_nota_parciales, limpiar_nota

# Ruta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# PROCESAMIENTO DE NOTAS 6
ruta_notas6 = os.path.join(directorio_actual, 'notas6.xlsx')

# Mapeo de las columnas específicas para Notas5
column_mapping = {
    'Apellido y Nombre': 'nombre',
    'Parcial 1': 'parcial_1_1',
    'Parcial 2': 'parcial_2_1',
    'Rec Parcial 1': 'parcial_1_2',
    'Rec Parcial 2': 'parcial_2_2',
    'Nota Final': 'nota_final',
    'Observaciones': 'observaciones'
}

# Leer el archivo excel, omitiendo la primera fila de títulos y usando la segunda fila para los encabezados
df_notas_raw = pd.read_excel(ruta_notas6)

# Renombrar las columnas según el mapeo
df_notas_raw = df_notas_raw.rename(columns=column_mapping)

# Seleccionar solo las columnas necesarias
columnas_necesarias = list(column_mapping.values())
df_notas6 = df_notas_raw.loc[:, columnas_necesarias].copy()

# Conservar solo nombre de pila
df_notas6['nombre'] = df_notas6['nombre'].apply(lambda x: x.split(",")[1].strip() if isinstance(x, str) and "," in x else x)

# Procesar las notas de parciales y recuperatorios
df_notas6['parcial_1'] = df_notas6.apply(lambda row: procesar_nota_parciales(row['parcial_1_1'], row['parcial_1_2']), axis=1)
df_notas6['parcial_2'] = df_notas6.apply(lambda row: procesar_nota_parciales(row['parcial_2_1'], row['parcial_2_2']), axis=1)

#Limpiar las notas finales
df_notas6['nota_final'] = df_notas6['nota_final'].apply(limpiar_nota)

# Agregar la columna genero utilizando la función auxiliar
ingresar_genero(df_notas6)

# Calcular nro_insuficientes usando la función auxiliar
df_notas6['nro_insuficientes'] = df_notas6['observaciones'].apply(calcular_nro_insuficientes).fillna(0).astype(int)

# Calcular nro_intentos usando la función auxiliar
calcular_nro_intentos(df_notas6)
df_notas6['nro_intentos'] = df_notas6['nro_intentos'].astype(int)

# Agregar la columna aprobacion (1 si nota_final >= 6, 0 de lo contrario)
df_notas6['aprobacion'] = df_notas6['nota_final'].apply(lambda x: 1 if x >= 6 else 0)

# Seleccionar solo las columnas finales
df_notas6_final = df_notas6[['genero', 'parcial_1', 'parcial_2', 'nota_final', 'aprobacion', 'nro_insuficientes', 'nro_intentos']]

# Mostrar los primeros 10 elementos con todas las columnas para verificar
print("Notas1 procesado:")
print(df_notas6_final.head(10))

# Guardar el DataFrame procesado en un archivo nuevo
ruta_salida = os.path.join(directorio_actual, 'notas6_procesado.xlsx')
df_notas6_final.to_excel(ruta_salida, index=False)
