import pandas as pd
import os
from funciones_auxiliares import ingresar_genero, calcular_nro_insuficientes, calcular_nro_intentos

# Ruta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# PROCESAMIENTO DE NOTAS 2
ruta_notas2 = os.path.join(directorio_actual, 'notas2.xlsx')

# Leer el archivo excel sin encabezados para obtener todas las filas
df_raw = pd.read_excel(ruta_notas2, skiprows=2)

# Seleccionar solo las columnas necesarias: 'nombre', 'parcial_1', 'parcial_2', 'nota_final', 'observaciones'
df_notas2 = df_raw.iloc[:, [0, 6, 7, 9, 11]].copy()

# Renombrar las columnas seleccionadas
df_notas2.columns = ['nombre', 'parcial_1', 'parcial_2', 'nota_final', 'observaciones']

# 1. Convertir guiones a valores NaN en las columnas de parciales
df_notas2['parcial_1'] = pd.to_numeric(df_notas2['parcial_1'], errors='coerce')
df_notas2['parcial_2'] = pd.to_numeric(df_notas2['parcial_2'], errors='coerce')

# Agregar la columna genero utilizando la función auxiliar
ingresar_genero(df_notas2)

# Calcular nro_insuficientes usando la función auxiliar
df_notas2['nro_insuficientes'] = df_notas2['observaciones'].apply(calcular_nro_insuficientes).fillna(0).astype(int)

# Calcular nro_intentos usando la función auxiliar
calcular_nro_intentos(df_notas2)
df_notas2['nro_intentos'] = df_notas2['nro_intentos'].astype(int)

# Agregar la columna aprobacion (1 si nota_final >= 6, 0 de lo contrario)
df_notas2['aprobacion'] = df_notas2['nota_final'].apply(lambda x: 1 if x >= 6 else 0)

# Seleccionar solo las columnas finales
df_notas2_final = df_notas2[['genero', 'parcial_1', 'parcial_2', 'nota_final', 'aprobacion', 'nro_insuficientes', 'nro_intentos']]

# Mostrar los primeros 10 elementos con todas las columnas para verificar
print("Notas1 procesado:")
print(df_notas2_final.head(10))

# Guardar el DataFrame procesado en un archivo nuevo
ruta_salida = os.path.join(directorio_actual, 'notas2_procesado.xlsx')
df_notas2_final.to_excel(ruta_salida, index=False)

print(f"Datos procesados y guardados en {ruta_salida}")

