### **Enfoque Completo para Responder RQ3**  
**RQ3: ¿Es posible predecir el nivel de vulnerabilidad-proneness de una app usando información contextual?**  

Este enfoque busca determinar si los datos disponibles en Google Play pueden utilizarse para predecir la propensión de una app a contener vulnerabilidades sin necesidad de analizar su código fuente.

---

## **Paso 1: Definición del Problema de Clasificación**  
Se plantea un problema de **clasificación binaria**, donde el objetivo es predecir si una app tiene **baja** o **alta** vulnerabilidad-proneness.  

Para establecer la etiqueta (`ground truth`), se usa el número de vulnerabilidades detectadas mediante análisis estático. Se definen dos clases:  
- **Baja propensión:** Apps con vulnerabilidades menores o iguales a la mediana del dataset.  
- **Alta propensión:** Apps con vulnerabilidades mayores a la mediana.  

Se utiliza la **mediana en lugar del promedio** para evitar que valores extremos afecten la clasificación y garantizar que las clases sean balanceadas, lo que mejora la estabilidad de los modelos de Machine Learning.

---

## **Paso 2: Selección y Extracción de Características**  
Se recopilan tres tipos de características para entrenar modelos de Machine Learning.

### **1. Métricas del Mercado (Market Metrics)**  
Estas métricas provienen de Google Play y representan información que los usuarios pueden consultar antes de descargar una app:  
- **Categoría de la app**  
- **Tamaño del APK**  
- **Número de permisos requeridos**  
- **Número de descargas e instalaciones**  
- **Presencia de anuncios y compras dentro de la app**  

Las variables numéricas se normalizan para evitar que una característica tenga un peso desproporcionado en el modelo.

### **2. Características Textuales (Textual Features)**  
Se extraen del **nombre y descripción de la app** en Google Play y se procesan mediante:  
- **Eliminación de stopwords** (palabras vacías).  
- **Stemming** (reducción de palabras a su raíz).  
- **Extracción de n-grams** (2 a 4 palabras consecutivas).  
- **Ponderación con TF-IDF** (frecuencia de palabras ajustada por su importancia).  

Solo se utilizan las palabras más relevantes según TF-IDF para reducir ruido y mejorar la eficiencia del modelo.

### **3. Métricas de Análisis Estático (Static Analysis Metrics)**  
Se extraen del código fuente de las apps:  
- **API mínima y API objetivo.**  
- **Número de clases, interfaces y paquetes.**  
- **Uso de librerías de terceros.**  

Estas métricas sirven como punto de comparación con las Market Metrics para evaluar si es posible predecir vulnerabilidades sin necesidad de inspeccionar el código.

---

## **Paso 3: Entrenamiento de Modelos de Machine Learning**  
Se prueban tres modelos de clasificación:  
- **Naive Bayes**  
- **J48 (Árbol de decisión)**  
- **Random Forest**  

Los modelos se entrenan con cinco combinaciones de características:  
1. **Market metrics + Textual features**  
2. **Solo Market metrics**  
3. **Solo Static analysis metrics**  
4. **Market metrics + Textual features + Static analysis metrics**  
5. **Market metrics + Static analysis metrics**  

Se usa **validación cruzada de 10 iteraciones (10-fold cross-validation)** para evaluar la estabilidad del modelo y evitar sobreajuste.  

Se monitorean los resultados en conjuntos de entrenamiento y prueba para asegurarse de que los modelos no se ajusten demasiado a los datos de entrenamiento.

---

## **Paso 4: Evaluación de los Modelos**  
Los modelos se evalúan utilizando **Precisión, Recall y F1-score**.  

### **Resultados clave:**  
- **Random Forest fue el mejor modelo**, con un **F1-score de 0.751** cuando se usaron **Market Metrics + Static Analysis Metrics**.  

Se prioriza **F1-score** en lugar de Accuracy, ya que este último puede dar una impresión errónea del desempeño en datasets desbalanceados.

---

## **Paso 5: Análisis de Importancia de Características (Feature Importance)**  
Se usa **Information Gain** para determinar qué características son más relevantes en la predicción.  

**Principales características predictivas:**  
1. **Tamaño del APK (Size)** – Predictor más relevante.  
2. **Número de permisos solicitados (Permissions).**  
3. **Número de calificadores (Raters).**  
4. **Presencia de anuncios y compras dentro de la app.**  

El análisis confirma que **Market Metrics por sí solas pueden predecir vulnerabilidades**, sin necesidad de analizar el código fuente de las apps.

---

## **Conclusiones Finales del Enfoque de RQ3**  
1. **Random Forest fue el mejor modelo**, con **F1-score de 0.751**.  
2. **El tamaño del APK y los permisos solicitados son los factores más predictivos.**  
3. **La información del mercado es suficiente para predecir vulnerabilidades sin necesidad de análisis de código.**  
4. **El análisis textual no mejoró la predicción.**  
5. **Google Play podría implementar un sistema de advertencias de seguridad basado en estas predicciones.**