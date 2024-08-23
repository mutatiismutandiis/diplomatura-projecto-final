import pandas as pd
import os
from funciones_auxiliares import ingresar_genero, calcular_nro_insuficientes, calcular_nro_intentos, procesar_nota_parciales

# Ruta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# PROCESAMIENTO DE NOTAS 3
ruta_notas4 = os.path.join(directorio_actual, 'notas4.xlsx')

# Leer el archivo excel sin encabezados para obtener todas las filas
df_raw = pd.read_excel(ruta_notas4, skiprows=1)

# Seleccionar solo las columnas necesarias: 'nombre', 'parcial_1', 'parcial_2', 'nota_final', 'observaciones'
df_notas4 = df_raw.iloc[:, [0, 4, 7, 8, 9, 12, 14]].copy()

# Renombrar las columnas seleccionadas
df_notas4.columns = ['nombre', 'parcial_1_1', 'parcial_2_1', 'rec_parcial_1', 'rec_parcial_2', 'nota_final', 'observaciones']

# Procesar las notas de parciales y recuperatorios
df_notas4['parcial_1'] = df_notas4.apply(lambda row: procesar_nota_parciales(row['parcial_1_1'], row['rec_parcial_1']), axis=1)
df_notas4['parcial_2'] = df_notas4.apply(lambda row: procesar_nota_parciales(row['parcial_2_1'], row['rec_parcial_2']), axis=1)

# Agregar la columna genero utilizando la función auxiliar
ingresar_genero(df_notas4)

# Calcular nro_insuficientes usando la función auxiliar
df_notas4['nro_insuficientes'] = df_notas4['observaciones'].apply(calcular_nro_insuficientes).fillna(0).astype(int)

# Calcular nro_intentos usando la función auxiliar
calcular_nro_intentos(df_notas4)
df_notas4['nro_intentos'] = df_notas4['nro_intentos'].astype(int)

# Agregar la columna aprobacion (1 si nota_final >= 6, 0 de lo contrario)
df_notas4['aprobacion'] = df_notas4['nota_final'].apply(lambda x: 1 if x >= 6 else 0)

# Seleccionar solo las columnas finales
df_notas4_final = df_notas4[['genero', 'parcial_1', 'parcial_2', 'nota_final', 'aprobacion', 'nro_insuficientes', 'nro_intentos']]

# Mostrar los primeros 10 elementos con todas las columnas para verificar
print("Notas1 procesado:")
print(df_notas4_final.head(10))

# Guardar el DataFrame procesado en un archivo nuevo
ruta_salida = os.path.join(directorio_actual, 'notas4_procesado.xlsx')
df_notas4_final.to_excel(ruta_salida, index=False)