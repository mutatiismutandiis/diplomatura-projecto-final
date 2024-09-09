import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix

# Cargar el archivo Excel
archivo = 'conjunto_datos_completo.xlsx'
df = pd.read_excel(archivo)

# Generar variables binarias para parcial_1 y parcial_2 (Aprobado = 1, No Aprobado = 0)
df['parcial_1_aprobado'] = df['parcial_1'].apply(lambda x: 1 if pd.notnull(x) and x >= 6 else 0)
df['parcial_2_aprobado'] = df['parcial_2'].apply(lambda x: 1 if pd.notnull(x) and x >= 6 else 0)

# Seleccionar las variables explicativas y la variable respuesta
X = df[['genero', 'parcial_1_aprobado', 'parcial_2_aprobado', 'nro_insuficientes']]
y = df['aprobacion']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo SVM
modelo_svm = SVC(kernel='linear')  # Puedes cambiar el kernel si lo deseas, por ejemplo 'rbf'

# Entrenar el modelo
modelo_svm.fit(X_train, y_train)

# Hacer predicciones
y_pred = modelo_svm.predict(X_test)

# Evaluar el modelo: precisión y matriz de confusión
precision = accuracy_score(y_test, y_pred)
matriz_confusion = confusion_matrix(y_test, y_pred)

print(f"Precisión del modelo SVM: {precision}")
print("Matriz de confusión del SVM:")
print(matriz_confusion)

# Mostrar los vectores de soporte si es relevante
print(f"Vectores de soporte:\n {modelo_svm.support_vectors_}")

# Evaluar el modelo con k-fold cross-validation
scores = cross_val_score(modelo_svm, X, y, cv=5, scoring='accuracy')

print(f"Precisión del modelo SVM: {scores.mean()} (± {scores.std()})")