import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar el archivo Excel
archivo = 'conjunto_datos_completo.xlsx'
df = pd.read_excel(archivo)

# Generar variables binarias para parcial_1 y parcial_2 (Aprobado = 1, No Aprobado = 0)
df['parcial_1_aprobado'] = df['parcial_1'].apply(lambda x: 1 if pd.notnull(x) and x >= 6 else 0)
df['parcial_2_aprobado'] = df['parcial_2'].apply(lambda x: 1 if pd.notnull(x) and x >= 6 else 0)

# Ver los primeros registros para confirmar
print(df[['parcial_1', 'parcial_1_aprobado', 'parcial_2', 'parcial_2_aprobado']].head())

# Regresión Logística
# Variables explicativas: genero, parcial_1_aprobado, parcial_2_aprobado, nro_insuficientes
# Variable respuesta: aprobacion
X = df[['genero', 'parcial_1_aprobado', 'parcial_2_aprobado', 'nro_insuficientes']]
y = df['aprobacion']

# Dividir los datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de regresión logística
modelo = LogisticRegression()

# Entrenar el modelo con los datos de entrenamiento
modelo.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = modelo.predict(X_test)

# Evaluar el modelo: precisión y matriz de confusión
precision = accuracy_score(y_test, y_pred)
matriz_confusion = confusion_matrix(y_test, y_pred)

print(f"Precisión del modelo: {precision}")
print("Matriz de confusión:")
print(matriz_confusion)

# Imprimir coeficientes del modelo
coeficientes = pd.DataFrame(modelo.coef_[0], X.columns, columns=['Coeficiente'])
print("Coeficientes del modelo:")
print(coeficientes)

# Imprimir el intercepto del modelo
print(f"Intercepto del modelo: {modelo.intercept_[0]}")

# Cálculo de falsos positivos y falsos negativos
falsos_positivos = np.sum((y_test == 0) & (y_pred == 1))
falsos_negativos = np.sum((y_test == 1) & (y_pred == 0))

print(f"Falsos positivos: {falsos_positivos}")
print(f"Falsos negativos: {falsos_negativos}")

# Visualización de la matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(matriz_confusion, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Aprobado', 'Aprobado'], yticklabels=['No Aprobado', 'Aprobado'])
plt.xlabel('Predicción')
plt.ylabel('Valor Real')
plt.title('Matriz de Confusión')
plt.show()