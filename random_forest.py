import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo Excel
archivo = 'conjunto_datos_completo.xlsx'
df = pd.read_excel(archivo)

# Generar variables binarias para parcial_1 y parcial_2 (Aprobado = 1, No Aprobado = 0)
df['parcial_1_aprobado'] = df['parcial_1'].apply(lambda x: 1 if pd.notnull(x) and x >= 6 else 0)
df['parcial_2_aprobado'] = df['parcial_2'].apply(lambda x: 1 if pd.notnull(x) and x >= 6 else 0)

# Definir las variables explicativas y la variable respuesta
X = df[['genero', 'parcial_1_aprobado', 'parcial_2_aprobado', 'nro_insuficientes']]
y = df['aprobacion']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo Random Forest
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Entrenar el modelo
modelo_rf.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred_rf = modelo_rf.predict(X_test)

# Evaluar el modelo: precisión y matriz de confusión
precision_rf = accuracy_score(y_test, y_pred_rf)
matriz_confusion_rf = confusion_matrix(y_test, y_pred_rf)

print(f"Precisión del modelo Random Forest: {precision_rf}")
print("Matriz de confusión del Random Forest:")
print(matriz_confusion_rf)

# Obtener la importancia de las variables
importancia_variables = modelo_rf.feature_importances_
columnas = X.columns

# Mostrar la importancia de las variables
for i, importancia in enumerate(importancia_variables):
    print(f"{columnas[i]}: {importancia}")

# VALIDACION CRUZADA
modelo_rf = RandomForestClassifier()
# Evaluar el modelo con k-fold cross-validation
scores = cross_val_score(modelo_rf, X, y, cv=5, scoring='accuracy')
print(f"Precisión del modelo Random Forest: {scores.mean()} (± {scores.std()})")

# OPTIMIZACIÓN DE HIPERPARÁMETROS
# Definir los hiperparámetros a optimizar
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

# Aplicar GridSearchCV para encontrar los mejores parámetros
grid_search_rf = GridSearchCV(estimator=modelo_rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')

# Entrenar el modelo con la búsqueda de hiperparámetros
grid_search_rf.fit(X_train, y_train)

# Imprimir los mejores parámetros encontrados
print(f"Mejores hiperparámetros para Random Forest: {grid_search_rf.best_params_}")

# Evaluar el mejor modelo
best_rf = grid_search_rf.best_estimator_
y_pred_rf = best_rf.predict(X_test)
precision_rf = accuracy_score(y_test, y_pred_rf)
matriz_confusion_rf = confusion_matrix(y_test, y_pred_rf)

print(f"Precisión del mejor Random Forest: {precision_rf}")
print("Matriz de confusión del mejor Random Forest:")
print(matriz_confusion_rf)

# Visualizar la importancia de las variables del mejor modelo
importancia_variables = best_rf.feature_importances_
columnas = X.columns

plt.figure(figsize=(8,6))
sns.barplot(x=importancia_variables, y=columnas)
plt.title('Importancia de las Variables en el Mejor Modelo Random Forest')
plt.xlabel('Importancia')
plt.ylabel('Variables')
plt.show()