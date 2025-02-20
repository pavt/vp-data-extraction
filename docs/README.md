# vp-data-extraction



github_dependency_analyzer/
│── src/
│   ├── __init__.py
│   ├── github_api.py
│   ├── dependency_analyzer.py
│   ├── batch_processor.py
│   ├── transform_data.py
│── data/
│   ├── github_repo_metrics_final.csv
│   ├── repos_dependencies_matrix.csv
│── main.py
│── requirements.txt
│── .gitignore
│── README.md


| Categoría                           | Feature                             | Tipo de Dato  | Técnicas de Feature Engineering |
|--------------------------------------|-------------------------------------|--------------|--------------------------------|
| **Identificadores**                  | repo_owner                          | Categórica   | Codificación One-Hot / Hashing de Características |
|                                      | repo_name                           | Categórica   | Codificación One-Hot / Hashing de Características |
| **Métricas del Repositorio**         | Category                            | Categórica   | Codificación One-Hot / Codificación de Frecuencia |
|                                      | Number of Components                | Numérica     | Normalización Min-Max / Transformación Logarítmica |
|                                      | commits                             | Numérica     | Normalización Z-score / Eliminación de valores atípicos |
|                                      | branches                            | Numérica     | Normalización Z-score / Cuantización en bins |
|                                      | releases                            | Numérica     | Normalización Min-Max / Cuantización en bins |
|                                      | forks                               | Numérica     | Transformación Logarítmica / Cuantización en bins |
|                                      | watchers                            | Numérica     | Normalización Z-score / Cuantización en bins |
|                                      | stargazers                          | Numérica     | Transformación Logarítmica / Normalización Min-Max |
|                                      | contributors                        | Numérica     | Normalización Z-score / Cuantización en bins |
|                                      | size                                | Numérica     | Transformación Logarítmica / Eliminación de valores atípicos |
| **Métricas de Issues y Pull Requests** | totalIssues                         | Numérica     | Normalización Z-score / Eliminación de valores atípicos |
|                                      | openIssues                          | Numérica     | Normalización Z-score / Cuantización en bins |
|                                      | totalPullRequests                   | Numérica     | Normalización Min-Max / Transformación Logarítmica |
|                                      | openPullRequests                    | Numérica     | Normalización Min-Max / Cuantización en bins |
|                                      | codeLines                           | Numérica     | Transformación Logarítmica / Eliminación de valores atípicos |
| **Lenguajes de Programación y Seguridad** | primary_language                  | Categórica   | Codificación One-Hot / Hashing de Características |
|                                      | license_name                        | Categórica   | Codificación One-Hot / Hashing de Características |
|                                      | security_policy_enabled             | Booleano     | Conversión a Numérico (0,1) |
|                                      | vulnerability_alerts_enabled        | Booleano     | Conversión a Numérico (0,1) |
| **Métricas de Popularidad y Colaboración** | stargazers_count                  | Numérica     | Transformación Logarítmica / Normalización Min-Max |
|                                      | network_count                       | Numérica     | Normalización Z-score / Eliminación de valores atípicos |
|                                      | subscribers_count                   | Numérica     | Normalización Z-score / Cuantización en bins |
| **Lenguajes Usados en el Repositorio** | languages                          | Categórica (Múltiples) | Codificación One-Hot con múltiples categorías |
| **Dependencias y Librerías**         | dependencies_json                    | Texto / JSON | Extracción de características con NLP / TF-IDF |
|                                      | dep_count                           | Numérica     | Transformación Logarítmica / Cuantización en bins |
|                                      | dep_error                           | Categórica   | Codificación One-Hot / Etiquetado de Errores |
| **Dependencias Específicas**         | dep_lodash.template                 | Categórica (Presencia de dependencia) | Conversión a Numérico (0,1) |
|                                      | dep_octokit                         | Categórica (Presencia de dependencia) | Conversión a Numérico (0,1) |
|                                      | dep_typescript                      | Categórica (Presencia de dependencia) | Conversión a Numérico (0,1) |
|                                      | dep_react                           | Categórica (Presencia de dependencia) | Conversión a Numérico (0,1) |
|                                      | dep_vue                             | Categórica (Presencia de dependencia) | Conversión a Numérico (0,1) |
