# Reddddit-Submissions-Analisis
Este repositorio contiene el código y los recursos necesarios para implementar un sistema de filtrado y análisis de datos provenientes de Reddit y la base de datos CVE. El objetivo principal del proyecto es crear una base de datos limpia y relevante para usarse en modelos de predicción
Este repositorio contiene el código y los recursos necesarios para implementar un sistema de filtrado y análisis de datos provenientes de Reddit y la base de datos CVE. El objetivo principal del proyecto es crear una base de datos limpia y relevante que pueda ser utilizada para predecir ciberataques y mejorar la capacidad de anticiparse y mitigar amenazas cibernéticas.

# Contenidos del Repositorio
## 1. Extracción de Datos
scripts/extract_reddit_data.py: Script para la extracción de datos de Reddit utilizando la API de Reddit y Academic Torrents.
scripts/extract_cve_data.py: Script para la extracción de datos de vulnerabilidades desde la base de datos CVE.
## 2. Filtrado Inicial
notebooks/initial_filtering.ipynb: Jupyter Notebook que implementa el primer filtro utilizando un diccionario de palabras clave específicas de ciberseguridad para reducir la cantidad de datos irrelevantes.
## 3. Marcado Manual y Análisis de Frecuencia
notebooks/manual_marking_and_frequency_analysis.ipynb: Jupyter Notebook que guía el proceso de revisión manual de registros y el análisis de frecuencia para identificar las palabras más comunes en los registros relevantes.
## 4. Refinamiento del Filtrado
notebooks/refinement_filtering.ipynb: Jupyter Notebook que aplica el segundo filtro basado en la cantidad de palabras clave contenidas en cada registro, utilizando el diccionario refinado.
## 5. Evaluación de Eficacia
notebooks/evaluation_of_effectiveness.ipynb: Jupyter Notebook para evaluar la eficacia del filtrado mediante la inclusión de registros de ruido y el ajuste iterativo del número mínimo de palabras clave.
## 6. Pruebas y Resultados
notebooks/testing_and_results.ipynb: Jupyter Notebook que documenta las pruebas realizadas y los resultados obtenidos, validando la precisión del proceso de filtrado y la relevancia de los datos seleccionados.

Contacto: s.rodriguez63@uniandes.edu.co
