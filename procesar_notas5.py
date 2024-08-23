import pandas as pd
import numpy as np
import os
from funciones_auxiliares import ingresar_genero, calcular_nro_insuficientes, calcular_nro_intentos, procesar_nota_parciales, procesar_notas_con_dos_rec, limpiar_nota

# Ruta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# PROCESAMIENTO DE NOTAS 5
ruta_notas5 = os.path.join(directorio_actual, 'notas5.xlsx')

# Mapeo de las columnas específicas para Notas5
column_mapping = {
    'Apellido(s) y Nombre(s)': 'nombre',
    'P1': 'parcial_1_1',
    'P2': 'parcial_2_1',
    'Rec-P1': 'parcial_1_2',
    'Rec-P2': 'parcial_2_2',
    '2doRec-P2': 'parcial_2_3',
    'NOTA FINAL': 'nota_final',
    'Observaciones': 'observaciones'
}

# Leer el archivo excel, omitiendo la primera fila de títulos y usando la segunda fila para los encabezados
df_notas_raw = pd.read_excel(ruta_notas5)

# Renombrar las columnas según el mapeo
df_notas_raw = df_notas_raw.rename(columns=column_mapping)

# Seleccionar solo las columnas necesarias
columnas_necesarias = list(column_mapping.values())
df_notas5 = df_notas_raw.loc[:, columnas_necesarias].copy()

# Procesar las notas de parciales y recuperatorios
df_notas5['parcial_1'] = df_notas5.apply(lambda row: procesar_nota_parciales(row['parcial_1_1'], row['parcial_1_2']), axis=1)
df_notas5['parcial_2'] = df_notas5.apply(lambda row: procesar_notas_con_dos_rec(row['parcial_2_1'], row['parcial_2_2'], row['parcial_2_3']), axis=1)

#Procesar las notas finales
df_notas5['nota_final'] = df_notas5['nota_final'].apply(limpiar_nota)

# Agregar la columna genero utilizando la función auxiliar
ingresar_genero(df_notas5)

# Calcular nro_insuficientes usando la función auxiliar
df_notas5['nro_insuficientes'] = df_notas5['observaciones'].apply(calcular_nro_insuficientes).fillna(0).astype(int)

# Calcular nro_intentos usando la función auxiliar
calcular_nro_intentos(df_notas5)
df_notas5['nro_intentos'] = df_notas5['nro_intentos'].astype(int)

# Agregar la columna aprobacion (1 si nota_final >= 6, 0 de lo contrario)
df_notas5['aprobacion'] = df_notas5['nota_final'].apply(lambda x: 1 if x >= 6 else 0)

# Seleccionar solo las columnas finales
df_notas5_final = df_notas5[['genero', 'parcial_1', 'parcial_2', 'nota_final', 'aprobacion', 'nro_insuficientes', 'nro_intentos']]

# Mostrar los primeros 10 elementos con todas las columnas para verificar
print("Notas1 procesado:")
print(df_notas5_final.head(10))

# Guardar el DataFrame procesado en un archivo nuevo
ruta_salida = os.path.join(directorio_actual, 'notas5_procesado.xlsx')
df_notas5_final.to_excel(ruta_salida, index=False)