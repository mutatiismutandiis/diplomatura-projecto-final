import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np

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
# Definimos manualmente los intervalos
bin_edges = np.linspace(0, 10, 11)
fig_parcial2 = px.histogram(df, x='parcial_2', labels={'parcial_2': 'Calificación'})
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
fig_parcial2.update_traces(xbins=dict(start=bin_edges[0], end=bin_edges[-1], size=1), marker_line_width=2, marker_line_color='black')
fig_parcial2.show()
pio.write_html(fig_parcial1, file='histograma_parcial_2.html', auto_open=True)
 
# Proporción de estudiantes por género
print("Proporción de estudiantes por género:")
proporcion_genero = df['genero'].value_counts(normalize=True)
print(proporcion_genero)
 
# Filtrar por género: 1 = Hombre, 0 = Mujer
df_mujeres = df[df['genero'] == 0]
df_hombres = df[df['genero'] == 1]
 
# Calcular estadísticas descriptivas por género
estadisticas_mujeres = df_mujeres[calificaciones].describe(percentiles=[0.25, 0.5, 0.75])
estadisticas_hombres = df_hombres[calificaciones].describe(percentiles=[0.25, 0.5, 0.75])
 
# Rango intercuartílico por género
rango_intercuartilico_mujeres = estadisticas_mujeres.loc['75%'] - estadisticas_mujeres.loc['25%']
estadisticas_mujeres.loc['rango_intercuartilico'] = rango_intercuartilico_mujeres
 
rango_intercuartilico_hombres = estadisticas_hombres.loc['75%'] - estadisticas_hombres.loc['25%']
estadisticas_hombres.loc['rango_intercuartilico'] = rango_intercuartilico_hombres
 
# Mostrar estadísticas descriptivas por género
print("\nEstadísticas descriptivas - Mujeres:")
print(estadisticas_mujeres)
 
print("\nEstadísticas descriptivas - Hombres:")
print(estadisticas_hombres)

# Histograma interactivo para las calificaciones del Parcial 1 por género
fig_parcial1_genero = px.histogram(df, x='parcial_1', color='genero', nbins=10,
                                   labels={'parcial_1': 'Calificación', 'genero': 'Género'},
                                   color_discrete_map={0: 'blue', 1: 'green'},
                                   barmode='overlay',  # Superponer los dos histogramas para compararlos
                                   opacity=0.7)
fig_parcial1_genero.update_layout(
    title='Histograma de Calificaciones - Parcial 1 por Género',
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1,
        range=[0, 10]
    ),
    yaxis_title='Frecuencia',
    legend_title_text='Género'
)
fig_parcial1_genero.for_each_trace(lambda t: t.update(name='Mujeres' if t.name == '0' else 'Varones'))
fig_parcial1_genero.update_traces(marker_line_width=2, marker_line_color='black')
fig_parcial1_genero.show()

# Guardar el gráfico interactivo Parcial 1 por género
pio.write_html(fig_parcial1_genero, file='histograma_parcial_1_por_genero.html', auto_open=True)

# Histograma interactivo para las calificaciones del Parcial 2 por género
fig_parcial2_genero = px.histogram(df, x='parcial_2', color='genero',
                                   labels={'parcial_2': 'Calificación', 'genero': 'Género'},
                                   color_discrete_map={0: 'blue', 1: 'green'},
                                   barmode='overlay',
                                   opacity=0.7)
fig_parcial2_genero.update_layout(
    title='Histograma de Calificaciones - Parcial 2 por Género',
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1,
        range=[0, 10]
    ),
    yaxis_title='Frecuencia',
    legend_title_text='Género'
)
fig_parcial2_genero.for_each_trace(lambda t: t.update(name='Mujeres' if t.name == '0' else 'Varones'))
fig_parcial2_genero.update_traces(xbins=dict(start=bin_edges[0], end=bin_edges[-1], size=1), marker_line_width=2, marker_line_color='black')
fig_parcial2_genero.show()

# Guardar el gráfico interactivo Parcial 2 por género
pio.write_html(fig_parcial2_genero, file='histograma_parcial_2_por_genero.html', auto_open=True) 

# Crear una nueva columna 'genero_label' para etiquetar los géneros correctamente en los boxplots
df['genero_label'] = df['genero'].map({0: 'Mujeres', 1: 'Hombres'})

# Crear boxplots interactivos para cada calificación (Parcial 1, Parcial 2, Nota Final)
for calificacion in calificaciones:
    fig_boxplot = px.box(df, x='genero_label', y=calificacion, color='genero_label',
                         labels={'genero_label': 'Género', calificacion: 'Calificación'},
                         title=f'Boxplot de Calificaciones - {calificacion.replace("_", " ").title()} por Género',
                         color_discrete_map={'Mujeres': 'blue', 'Hombres': 'green'})
    
    fig_boxplot.update_layout(
        xaxis_title='Género',
        yaxis_title='Calificación',
        legend_title_text='Género'
    )
    
    fig_boxplot.update_traces(marker_line_width=2, marker_line_color='black')
    
    # Mostrar el gráfico interactivo
    fig_boxplot.show()
    
    # Guardar el gráfico como un archivo HTML
    pio.write_html(fig_boxplot, file=f'boxplot_{calificacion}_por_genero.html', auto_open=True)


# Comparación de tasas de aprobación
tasa_aprobacion_general = df['aprobacion'].mean()
tasa_aprobacion_mujeres = df_mujeres['aprobacion'].mean()
tasa_aprobacion_hombres = df_hombres['aprobacion'].mean()
 
print("Tasa de Aprobación General:", tasa_aprobacion_general)
print("Tasa de Aprobación Mujeres:", tasa_aprobacion_mujeres)
print("Tasa de Aprobación Hombres:", tasa_aprobacion_hombres)

# Análisis de las variables "Número de insuficientes" y "Número de intentos"
# Reemplazar valores vacíos en 'nro_insu' por ceros
df['nro_insuficientes'].fillna(0, inplace=True)
 
# Convertir a entero si es necesario
df['nro_insuficientes'] = df['nro_insuficientes'].astype(int)
 
# Análisis del número de intentos
estadisticas_intentos = df['nro_intentos'].describe(percentiles=[0.25, 0.5, 0.75])
print("Estadísticas descriptivas del número de intentos:")
print(estadisticas_intentos)

# Análisis del número de insuficientes
estadisticas_insuf = df['nro_insuficientes'].describe(percentiles=[0.25, 0.5, 0.75])
print("\nEstadísticas descriptivas del número de insuficientes:")
print(estadisticas_insuf)
 
# Filtrar por género
df_mujeres = df[df['genero'] == 0]
df_hombres = df[df['genero'] == 1]

# Estadísticas descriptivas por género para el número de intentos
estadisticas_intentos_mujeres = df_mujeres['nro_intentos'].describe(percentiles=[0.25, 0.5, 0.75])
estadisticas_intentos_hombres = df_hombres['nro_intentos'].describe(percentiles=[0.25, 0.5, 0.75])

# Estadísticas descriptivas por género para el número de insuficientes
estadisticas_insuf_mujeres = df_mujeres['nro_insuficientes'].describe(percentiles=[0.25, 0.5, 0.75])
estadisticas_insuf_hombres = df_hombres['nro_insuficientes'].describe(percentiles=[0.25, 0.5, 0.75])
 
# Mostrar estadísticas descriptivas por género
print("\nEstadísticas descriptivas - Mujeres (Número de intentos):")
print(estadisticas_intentos_mujeres)
 
print("\nEstadísticas descriptivas - Hombres (Número de intentos):")
print(estadisticas_intentos_hombres)
 
print("\nEstadísticas descriptivas - Mujeres (Número de insuficientes):")
print(estadisticas_insuf_mujeres)
 
print("\nEstadísticas descriptivas - Hombres (Número de insuficientes):")
print(estadisticas_insuf_hombres)
