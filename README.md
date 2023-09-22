# <h1 align=center> **Sistema de Recomendación**</h1>
# <h2> **Proyecto individual Nº1**</h1>
# `Machine Learning Operations (MLOps)`
## **Henry's Labs**
### *Por Abraham Gómez DataPT01*

El objetivo principal del proyecto es crear un sistema de recomendación de películas utilizando técnicas de aprendizaje automático (Machine Learning). El proyecto se divide en diferentes etapas:

1. Extracción, transformación y carga (ETL): Se realiza la extracción de datos del conjunto de datos "movies_dataset.csv" y "credits.csv". Se aplican transformaciones para obtener información relevante, como los nombres de los campos de pertenencia a una colección, géneros, compañías de producción, países de producción, idiomas hablados, elenco y equipo de producción. Los datos transformados se cargan en un nuevo conjunto de datos.

2. Desarrollo de API: Se crean funciones en el archivo "funciones.ipynb" que proporcionan diferentes consultas y funcionalidades para integrarlas en el código y utilizarlas en FastAPI. Las funciones disponibles incluyen la cantidad de filmaciones por mes y por día, información de puntuación y votos de una película, éxito de un actor o director, y recomendación de películas similares.

3. Análisis exploratorio de los datos (EDA): Se realiza un análisis exploratorio de los datos para comprender mejor la información a la que se tiene acceso. Se exploran valores atípicos, se crea una matriz de correlación para identificar relaciones entre variables, se analiza la proporción de películas producidas por décadas, se obtienen los top 10 de películas de mayor recaudación e inversión, y se genera una nube de palabras con los términos más frecuentes en los títulos de las películas.

4. Sistema de recomendación: Se implementa un sistema de recomendación de películas basado en películas similares. Se calcula la similitud de puntuación entre una película ingresada y el resto de películas, se ordenan según el puntaje de similaridad y se devuelve una lista de las 5 películas más similares. Esta función adicional se integra en la API previamente desarrollada.

## Tabla de contenidos

- [ETL (Extracción, Transformación y Carga)](#etl-extracción-transformación-y-carga)
- [Desarrollo de API](#desarrollo-de-api)
- [Análisis Exploratorio de los Datos (EDA)](#análisis-exploratorio-de-los-datos-eda)
- [Sistema de Recomendación](#sistema-de-recomendación)
- [Referencias](#referencias)

## ETL (Extracción, Transformación y Carga)

En esta sección se detallan las transformaciones realizadas en los datos y los archivos utilizados durante el proceso de extracción, transformación y carga.

### Transformaciones realizadas

Durante el proceso ETL, se llevaron a cabo las siguientes transformaciones en los datos del dataset:

- Extracción de los nombres de los campos `belong_to_collection`, `genres`, `production_companies`, `production_countries` y `spoken_languages` del archivo `movies_dataset.csv`.
- Extracción de los nombres de `cast`, `crew` y del nombre del director de `crew` del archivo `credits.csv`.
- Agregación de la columna con el nombre del director al dataset `movies_dataset.csv`.

Estas transformaciones permitieron obtener un conjunto de datos enriquecido con información adicional necesaria para el análisis y la implementación del sistema de recomendación. Los resultados de estas transformaciones se reflejan en los archivos `movies.csv` y `credits.csv`, los cuales se encuentran alojados en el directorio `data` del proyecto. Estos archivos contienen los registros transformados y son útiles para ser consumidos por el usuario final.

### Archivos utilizados

Durante el proceso ETL, se utilizaron los siguientes archivos:

- `movies_dataset.csv`: Contiene información sobre las películas, incluyendo títulos, géneros, compañías de producción, países de producción y otros campos relevantes.
- `credits.csv`: Contiene información sobre el elenco y el equipo de producción de las películas, incluyendo nombres de actores, nombres de miembros del equipo y otros datos relacionados.

Estos archivos fueron fundamentales para realizar las transformaciones y obtener un dataset completo y preparado para su posterior análisis y uso en el sistema de recomendación.

### Notebook ETL.ipynb

El proceso ETL fue llevado a cabo en el notebook `ETL.ipynb`. En este notebook se encuentran detalladas todas las etapas del proceso, incluyendo la carga de los datos, las transformaciones realizadas y la generación del nuevo dataset enriquecido. Además, se proporciona la explicación paso a paso de cada una de las operaciones realizadas.

El notebook `ETL.ipynb` es una herramienta fundamental para comprender y reproducir el proceso ETL realizado en este proyecto.


## Desarrollo de API

En esta sección se detalla el desarrollo de la API que permite interactuar con el sistema de recomendación y acceder a diferentes funciones y servicios.

### Funciones disponibles

Las siguientes funciones están disponibles a través de la API:

- `cantidad_filmaciones_mes(Mes)`: Se ingresa un mes en idioma Español y devuelve la cantidad de películas que fueron estrenadas en ese mes en el dataset completo.

- `cantidad_filmaciones_dia(Dia)`: Se ingresa un día en idioma Español y devuelve la cantidad de películas que fueron estrenadas en ese día en el dataset completo.

- `score_titulo(titulo_de_la_filmación)`: Se ingresa el título de una filmación y devuelve el título, el año de estreno y el score.

- `votos_titulo(titulo_de_la_filmación)`: Se ingresa el título de una filmación y devuelve el título, la cantidad de votos y el valor promedio de las votaciones. Esta función solo devuelve resultados si la filmación tiene al menos 2000 valoraciones; de lo contrario, muestra un mensaje indicando que no cumple esta condición y no devuelve ningún valor.

- `get_actor(nombre_actor)`: Se ingresa el nombre de un actor presente en el dataset y devuelve el éxito del actor medido a través del retorno, la cantidad de películas en las que ha participado y el promedio de retorno. Esta función no considera a los directores.

- `get_director(nombre_director)`: Se ingresa el nombre de un director presente en el dataset y devuelve el éxito del director medido a través del retorno, además de devolver el nombre de cada película dirigida por ese director, junto con la fecha de lanzamiento, el retorno individual, el costo y la ganancia de cada película.

- `recomendacion(titulo)`: Se ingresa el nombre de una película y devuelve una lista con 5 películas similares recomendadas.

### Integración en FastAPI

El desarrollo de la API se ha realizado utilizando el framework FastAPI. El archivo `main.py` contiene la implementación de las funciones descritas anteriormente. Estas funciones se han basado en el notebook `funciones.ipynb` donde se realizaron los primeros desarrollos y pruebas.

Para integrar estas funciones en FastAPI y hacer que estén disponibles a través de la API, se ha implementado el archivo `main.py`. Este archivo define las rutas y los endpoints correspondientes a cada función. Además, se han establecido las validaciones necesarias para los parámetros de entrada y se han definido las respuestas esperadas.

Para obtener más detalles sobre cómo utilizar las funciones de la API y cómo implementar el proyecto en diferentes entornos, consulte la documentación proporcionada en el archivo `API.md`.


## Análisis Exploratorio de los Datos (EDA)

Se llevó a cabo un análisis exploratorio de los datos con el objetivo de comprender la estructura y características del conjunto de datos de películas. A continuación, se presentan algunos aspectos destacados del análisis:

### Análisis de valores atípicos

Se identificaron y analizaron los valores atípicos en las variables numéricas clave del conjunto de datos. Esto permitió comprender mejor la distribución de los datos y detectar posibles errores o discrepancias.

![Gráfico de Valores Atípicos](/images/valores_atipicos.png)

### Matriz de correlación

Se construyó una matriz de correlación para examinar las relaciones entre las variables numéricas del conjunto de datos. Esta matriz ayudó a identificar posibles correlaciones y patrones entre las características de las películas.

![Matriz de Correlación](/images/matriz_correlacion.png)

### Gráficas de Dispersión

A continuación se muestra una imagen con las siguientes gráficas de dispersión:

- Gráfico de revenue vs budget
- Gráfico de vote_count vs budget
- Gráfico de revenue vs vote_count

![Gráficas de Dispersión](/images/graficas_dispercion.png)

### Proporción de películas por décadas

Se realizó un análisis de la proporción de películas por décadas para comprender cómo ha evolucionado la producción cinematográfica a lo largo del tiempo. Se visualizó esta información en forma de gráfico de barras.

![Gráfico de Proporción de Películas por Décadas](/images/proporcion_decadas.png)

### Top 10 de películas de mayor recaudación

Se identificaron las 10 películas con mayor recaudación en el conjunto de datos y se presentaron en forma de tabla o gráfico para resaltar las películas más exitosas en términos de ingresos.

![Top 10 de Películas de Mayor Recaudación](/images/top_recaudacion.png)

### Top 10 de películas de mayor inversión

Se identificaron las 10 películas con mayor inversión en el conjunto de datos y se presentaron en forma de tabla o gráfico para resaltar las películas que requirieron una mayor inversión económica.

![Top 10 de Películas de Mayor Inversión](/images/top_inversion.png)

### Nube de palabras en los títulos de películas

Se generó una nube de palabras utilizando los títulos de las películas para visualizar las palabras más frecuentes y relevantes en el conjunto de datos. Esta visualización ayudó a obtener una idea rápida de los temas y géneros más comunes en las películas.

![Nube de Palabras en Títulos de Películas](/images/nube_palabras.png)

## Sistema de Recomendación

El sistema de recomendación implementado en este proyecto utiliza el algoritmo de similitud de puntuación para proporcionar recomendaciones de películas similares. El código de la función `recomendacion()` se encarga de realizar este cálculo y devolver los resultados en un formato adecuado.

### Principios Matemáticos

El cálculo de similitud de puntuación se basa en el algoritmo TF-IDF (Term Frequency-Inverse Document Frequency) y la medida de similitud del coseno. Estos principios matemáticos permiten comparar la similitud entre dos documentos, en este caso, los títulos de las películas.

La medida de similitud del coseno se define como:

\[
\text{{similarity}}(x, y) = \frac{{\text{{dot\_product}}(x, y)}}{{\|\|x\|\| \cdot \|\|y\|\|}}
\]

donde:
- \(\text{{dot\_product}}(x, y)\) representa el producto punto entre \(x\) y \(y\).
- \(\|\|x\|\|\) y \(\|\|y\|\|\) representan las normas de \(x\) y \(y\) respectivamente.

Donde `x` y `y` representan dos vectores de características (en este caso, vectores TF-IDF de los títulos de las películas), `dot_product` es el producto punto entre los dos vectores y `norm` es la norma euclidiana de un vector.

La matriz TF-IDF se genera mediante los siguientes pasos:

1. Calcular la frecuencia de término (TF, Term Frequency) de cada término en cada documento. La frecuencia de término es la cantidad de veces que un término específico aparece en un documento.

2. Calcular el factor de inverso de documento (IDF, Inverse Document Frequency) para cada término. El IDF mide la importancia relativa de un término en el conjunto de documentos. Se calcula como el logaritmo del cociente entre el número total de documentos y el número de documentos que contienen el término específico.

3. Multiplicar la frecuencia de término (TF) de cada término en cada documento por el factor de inverso de documento (IDF) correspondiente.

### Modo de Uso

Para utilizar la función `recomendacion()` en la API, se debe llamar pasando como argumento el título de la película para la cual se desean obtener recomendaciones. Por ejemplo:

   ```bash
    recomendacion("The Matrix")
```

### Aplicación en la API
La función recomendacion() se integra en la API para proporcionar recomendaciones de películas similares a los usuarios. Al llamar a esta función a través de la API, se obtiene un resultado en formato JSON que contiene una lista de los nombres de las películas recomendadas.

La API permite a los usuarios acceder a esta función y obtener recomendaciones personalizadas según sus preferencias. Pueden ingresar un título de película y recibir una lista de películas similares recomendadas.

Asegúrate de importar las bibliotecas necesarias, tener los datos del conjunto de películas cargados correctamente y configurar la API correctamente para poder utilizar esta función de manera adecuada.

Recuerda que la función recomendacion() es solo una parte del sistema de recomendación, y existen otros componentes y algoritmos que trabajan en conjunto para proporcionar resultados precisos y relevantes a los usuarios.

## Referencias
- Pandas Documentation
- Matplotlib Documentation
- WordCloud Documentation
- scikit-learn TfidfVectorizer Documentation
- scikit-learn cosine_similarity Documentation
- FastAPI Documentation
- Seaborn Documentation
