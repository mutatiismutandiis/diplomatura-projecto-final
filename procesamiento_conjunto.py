import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'chrome'

# Leer el archivo conjunto de datos
archivo = 'conjunto_datos_completo.xlsx'

# Leer el DataFrame del archivo completo
df = pd.read_excel(archivo)

# Columnas con calificaciones a analizar
calificaciones = ['parcial_1', 'parcial_2', 'nota_final']

# Estadísticas descriptivas generales para las calificaciones de los parciales y la nota final
estadisticas_descriptivas = df[calificaciones].describe(percentiles=[0.25, 0.5, 0.75])
rango_intercuartilico = estadisticas_descriptivas.loc['75%'] - estadisticas_descriptivas.loc['25%']
estadisticas_descriptivas.loc['rango_intercuartilico'] = rango_intercuartilico

# Mostrar estadísticas descriptivas
print("Estadísticas descriptivas:")
print(estadisticas_descriptivas)

# Histograma Calificaciones Parcial 1
fig_parcial1 = px.histogram(df, x='parcial_1', nbins=10, labels={'parcial_1': 'Calificación'})
fig_parcial1.update_layout(
     title='Histograma de Calificaciones - Parcial 1',
     xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1,  # Intervalos de 1 en 1
        range=[0, 10]
    ),
    yaxis_title='Frecuencia'
)
fig_parcial1.update_traces(marker_line_width=2, marker_line_color='black')
fig_parcial1.show()
pio.write_html(fig_parcial1, file='histograma_parcial_1.html', auto_open=True)

# Histograma Calificaciones Parcial 2
fig_parcial2 = px.histogram(df, x='parcial_2', nbins=10, labels={'parcial_2': 'Calificación'}, range_x=[0, 10])
fig_parcial2.update_layout(
    title='Histograma de Calificaciones - Parcial 2',
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1,  # Intervalos de 1 en 1
        range=[0, 10]
    ),
    yaxis_title='Frecuencia'
)
fig_parcial2.update_traces(marker_line_width=2, marker_line_color='black')
fig_parcial2.show()

# =============================================================================
# # Diagrama de bastones para la Calificación Final
# plt.figure(figsize=(10, 6))
# sns.countplot(x='nota_final', data=df, palette='viridis')
# plt.title('Diagrama de Bastones - Calificación Final')
# plt.xlabel('Calificación Final')
# plt.ylabel('Frecuencia')
# plt.grid(True)
# plt.savefig('diagrama_bastones_nota_final.png')
# plt.show()
# 
# # Proporción de estudiantes por género
# print("Proporción de estudiantes por género:")
# proporcion_genero = df['genero'].value_counts(normalize=True)
# print(proporcion_genero)
# 
# # Filtrar por género: 1 = Hombre, 0 = Mujer
# df_mujeres = df[df['genero'] == 0]
# df_hombres = df[df['genero'] == 1]
# 
# # Calcular estadísticas descriptivas por género
# estadisticas_mujeres = df_mujeres[calificaciones].describe(percentiles=[0.25, 0.5, 0.75])
# estadisticas_hombres = df_hombres[calificaciones].describe(percentiles=[0.25, 0.5, 0.75])
# 
# # Rango intercuartílico por género
# rango_intercuartilico_mujeres = estadisticas_mujeres.loc['75%'] - estadisticas_mujeres.loc['25%']
# estadisticas_mujeres.loc['rango_intercuartilico'] = rango_intercuartilico_mujeres
# 
# rango_intercuartilico_hombres = estadisticas_hombres.loc['75%'] - estadisticas_hombres.loc['25%']
# estadisticas_hombres.loc['rango_intercuartilico'] = rango_intercuartilico_hombres
# 
# # Mostrar estadísticas descriptivas por género
# print("\nEstadísticas descriptivas - Mujeres:")
# print(estadisticas_mujeres)
# 
# print("\nEstadísticas descriptivas - Hombres:")
# print(estadisticas_hombres)
# 
# # Histograma para las calificaciones del Parcial 1 por género
# bins = np.arange(0, 11, 1)
# plt.figure(figsize=(10, 6))
# sns.histplot(df_mujeres['parcial_1'], bins=bins, color='blue', label='Mujeres', kde=False, alpha=0.7, zorder=2)
# sns.histplot(df_hombres['parcial_1'], bins=bins, color='green', label='Hombres', kde=False, alpha=0.6, zorder=1)
# plt.title('Histograma de Calificaciones - Parcial 1 por Género')
# plt.xlabel('Calificación')
# plt.ylabel('Frecuencia')
# plt.xticks(bins)  # Asegurarse de que los ticks del eje x coincidan con los bins
# plt.legend()
# plt.grid(True)
# plt.savefig('histograma_parcial_1_por_genero.png')
# plt.show()
# 
# # Histograma para las calificaciones del Parcial 2 por género
# plt.figure(figsize=(10, 6))
# bins=10
# sns.histplot(df_mujeres['parcial_2'], bins=bins, color='blue', label='Mujeres', kde=False, alpha=0.7, zorder=2)
# sns.histplot(df_hombres['parcial_2'], bins=bins, color='green', label='Hombres', kde=False, alpha=0.6, zorder=1)
# plt.title('Histograma de Calificaciones - Parcial 2 por Género')
# plt.xlabel('Calificación')
# plt.ylabel('Frecuencia')
# plt.legend()
# plt.grid(True)
# plt.savefig('histograma_parcial_2_por_genero.png')
# plt.show()
# 
# # Diagrama de bastones para la Calificación Final por género
# plt.figure(figsize=(10, 6))
# sns.countplot(x='nota_final', hue='genero', data=df, palette='viridis')
# plt.title('Diagrama de Bastones - Calificación Final por Género')
# plt.xlabel('Calificación Final')
# plt.ylabel('Frecuencia')
# plt.grid(True)
# plt.savefig('diagrama_bastones_nota_final_por_genero.png')
# plt.show()
# 
# # Añadir una columna 'genero_label' para los boxplots
# df['genero_label'] = df['genero'].map({0: 'Mujeres', 1: 'Hombres'})
# 
# # Crear boxplots para cada calificación
# for calificacion in calificaciones:
#     plt.figure(figsize=(12, 6))
#     sns.boxplot(x='genero_label', y=calificacion, data=df, palette="Set2")
#     plt.title(f'Boxplot de Calificaciones - {calificacion.replace("_", " ").title()} por Género')
#     plt.xlabel('Género')
#     plt.ylabel('Calificación')
#     plt.grid(True)
#     plt.savefig(f'boxplot_{calificacion}_por_genero.png')
#     plt.show()
# 
# # Comparación de tasas de aprobación
# tasa_aprobacion_general = df['aprobacion'].mean()
# tasa_aprobacion_mujeres = df_mujeres['aprobacion'].mean()
# tasa_aprobacion_hombres = df_hombres['aprobacion'].mean()
# 
# print("Tasa de Aprobación General:", tasa_aprobacion_general)
# print("Tasa de Aprobación Mujeres:", tasa_aprobacion_mujeres)
# print("Tasa de Aprobación Hombres:", tasa_aprobacion_hombres)
# 
# # Análisis de las variables "Número de insuficientes" y "Número de intentos"
# # Reemplazar valores vacíos en 'nro_insu' por ceros
# df['nro_insuficientes'].fillna(0, inplace=True)
# 
# # Convertir a entero si es necesario
# df['nro_insuficientes'] = df['nro_insuficientes'].astype(int)
# 
# # Análisis del número de intentos
# estadisticas_intentos = df['nro_intentos'].describe(percentiles=[0.25, 0.5, 0.75])
# print("Estadísticas descriptivas del número de intentos:")
# print(estadisticas_intentos)
# 
# # Análisis del número de insuficientes
# estadisticas_insuf = df['nro_insuficientes'].describe(percentiles=[0.25, 0.5, 0.75])
# print("\nEstadísticas descriptivas del número de insuficientes:")
# print(estadisticas_insuf)
# 
# # Filtrar por género
# df_mujeres = df[df['genero'] == 0]
# df_hombres = df[df['genero'] == 1]
# 
# # Estadísticas descriptivas por género para el número de intentos
# estadisticas_intentos_mujeres = df_mujeres['nro_intentos'].describe(percentiles=[0.25, 0.5, 0.75])
# estadisticas_intentos_hombres = df_hombres['nro_intentos'].describe(percentiles=[0.25, 0.5, 0.75])
# 
# # Estadísticas descriptivas por género para el número de insuficientes
# estadisticas_insuf_mujeres = df_mujeres['nro_insuficientes'].describe(percentiles=[0.25, 0.5, 0.75])
# estadisticas_insuf_hombres = df_hombres['nro_insuficientes'].describe(percentiles=[0.25, 0.5, 0.75])
# 
# # Mostrar estadísticas descriptivas por género
# print("\nEstadísticas descriptivas - Mujeres (Número de intentos):")
# print(estadisticas_intentos_mujeres)
# 
# print("\nEstadísticas descriptivas - Hombres (Número de intentos):")
# print(estadisticas_intentos_hombres)
# 
# print("\nEstadísticas descriptivas - Mujeres (Número de insuficientes):")
# print(estadisticas_insuf_mujeres)
# 
# print("\nEstadísticas descriptivas - Hombres (Número de insuficientes):")
# print(estadisticas_insuf_hombres)
# 
# # Diagrama de Dispersión para Número de Intentos
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='nro_intentos', y='nro_insuficientes', hue='genero', data=df, palette={0: 'blue', 1: 'green'}, alpha=0.7)
# plt.title('Número de Intentos vs. Número de Insuficientes por Género')
# plt.xlabel('Número de Intentos')
# plt.ylabel('Número de Insuficientes')
# plt.legend(title='Género', labels=['Mujeres', 'Hombres'])
# plt.grid(True)
# plt.savefig('intentos_vs_insuficientes.png')
# plt.show()
# =============================================================================
