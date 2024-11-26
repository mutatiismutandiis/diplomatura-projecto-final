import pandas as pd
import numpy as np
import os
from funciones_auxiliares import ingresar_genero, calcular_nro_insuficientes, calcular_nro_intentos

# Ruta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# PROCESAMIENTO DE NOTAS 1
ruta_notas1 = os.path.join(directorio_actual, 'notas1.xlsx')

# Mapeo de las columnas específicas para Notas1
column_mapping = {
    'APELLIDO Y NOMBRE': 'nombre',
    'PARCIAL 1 (07/05)': 'parcial_1',
    'PARCIAL 2 (04/06)': 'parcial_2',
    'NOTA FINAL': 'nota_final',
    'Observaciones': 'observaciones'
}

# Leer el archivo excel, omitiendo la primera fila de títulos y usando la segunda fila para los encabezados
df_notas1 = pd.read_excel(ruta_notas1, header=1)

# Conservar solo nombre de pila
df_notas1['APELLIDO Y NOMBRE'] = df_notas1['APELLIDO Y NOMBRE'].apply(lambda x: x.split(', ')[1] if ',' in x else x)

# Renombrar las columnas según el mapeo
df_notas1 = df_notas1.rename(columns=column_mapping)

# Seleccionar solo las columnas necesarias
columnas_necesarias = list(column_mapping.values())
df_notas1 = df_notas1[columnas_necesarias]

# Convertir guiones a valores NaN en las columnas de parciales
df_notas1['parcial_1'] = pd.to_numeric(df_notas1['parcial_1'], errors='coerce')
df_notas1['parcial_2'] = pd.to_numeric(df_notas1['parcial_2'], errors='coerce')

# Limpiar la columna de nota final
def limpiar_nota_final(nota):
    if pd.isna(nota) or nota.strip() == '-':
        return np.nan
    # Extraer solo el número antes del paréntesis
    partes = str(nota).split(' (')
    try:
        return float(partes[0])
    except ValueError:
        return np.nan

df_notas1['nota_final'] = df_notas1['nota_final'].apply(limpiar_nota_final)

# Agregar la columna genero utilizando la función auxiliar
ingresar_genero(df_notas1)

# Calcular nro_insuficientes usando la función auxiliar
df_notas1['nro_insuficientes'] = df_notas1['observaciones'].apply(calcular_nro_insuficientes)

# Calcular nro_intentos usando la función auxiliar
calcular_nro_intentos(df_notas1)

# Agregar la columna aprobacion (1 si nota_final >= 6, 0 de lo contrario)
df_notas1['aprobacion'] = df_notas1['nota_final'].apply(lambda x: 1 if x >= 6 else 0)

# Seleccionar solo las columnas finales
df_notas1_final = df_notas1[['genero', 'parcial_1', 'parcial_2', 'nota_final', 'aprobacion', 'nro_insuficientes', 'nro_intentos']]

# Mostrar los primeros 10 elementos con todas las columnas para verificar
print("Notas1 procesado:")
print(df_notas1_final.head(10))

# Guardar el DataFrame procesado en un archivo nuevo
ruta_salida = os.path.join(directorio_actual, 'notas1_procesado.xlsx')
df_notas1_final.to_excel(ruta_salida, index=False)

print(f"Datos procesados y guardados en {ruta_salida}")
