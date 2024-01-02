# <h1 align=center> **Sistema de Recomendación**</h1>
# <h2> **Proyecto individual Nº1**</h1>
# `Machine Learning Operations (MLOps)`
## **Henry's Labs**
### *Por Abraham Gómez DataPT01*

El objetivo principal del proyecto es crear un sistema de recomendación de videojuegos utilizando técnicas de aprendizaje automático (Machine Learning). El p royecto se divide en diferentes etapas:

1. Extracción, transformación y carga (ETL): Se realiza la extracción de datos del conjunto de datos "dataset\australian_user_reviews.json", "dataset\australian_users_items.json" y "dataset/output_steam_games.json". Se aplican transformaciones para estandarizar la "data" debido a que los registros JSON no contienen errores, es por ello que deben de tranformarse y con el objetivo de economizar espacio de almacenamiento se procede a archivar la data en formato parquet. En el proceso de transformación se desanidan los items, recomendaciones y se procesan las recomendaciones (reviews) en una variable discreta "Sentiment_analisys", ademas es necesario eliminar algunos registros nulos que no aportan información relevante.

2. Desarrollo de API: El desarollo de la API inicia con la creación de funciones las cuales fueron probadas en su fase inicial en el notebook `funciones.ipynb` las cuales fueron integradas posteriormente en `main.py` para su ejecución en la por medio de FastAPI. Las funcionalidades disponibles son:
- PlayTimeGenre(genero : str)
- UserForGenre(genero : str)
- UsersRecommend(año : int)
- UsersNotRecommend( año : int)
- sentiment_analysis( año : int)
- recomendacion_juego(id : int)

3. Análisis exploratorio de los datos (EDA): Se realiza un análisis exploratorio dek [dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj). Se exploran valores atípicos, se analiza el tiempo de juego para varios videojuegos, se obtienen los top 10 de videojuegos más jugados, los videojuegos mas jugado entre el 2010 y 2013 y el top 10 desarrolladores que recaudaron.

4. Sistema de recomendación: Se implementa un sistema de recomendación dado el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado

## Tabla de contenidos

- [ETL (Extracción, Transformación y Carga)](#etl-extracción-transformación-y-carga)
- [Desarrollo de API](#desarrollo-de-api)
- [Análisis Exploratorio de los Datos (EDA)](#análisis-exploratorio-de-los-datos-eda)
- [Sistema de Recomendación](#sistema-de-recomendación)

## ETL (Extracción, Transformación y Carga)

1. Lectura y Procesamiento de Datos:

- Lee los datos de varios archivos JSON y los convierte en DataFrames de Pandas. Estos DataFrames contienen información sobre reseñas de usuarios, juegos de Steam y géneros de juegos.
- Realiza algunas limpiezas de datos, como eliminar registros duplicados y reemplazar valores nulos.
- Normalizar los datos como fechas, valores enteros o decimales
2. Análisis de Sentimiento:

- Utiliza la biblioteca `NLTK` para realizar un análisis de sentimiento de las reseñas de los usuarios. Asigna un valor de sentimiento (positivo, neutral o negativo) a cada reseña.

3. Generacion de tablas segun la funcionalidad requerida para la API:

- `ranking_genre.parquet` contiene el total de horas jugadas por genero y año
- `user_genre.parquet` este dataset contiene las horas jugadas por usuario ,genero y año.
- `recommend.parquet` el dataset contiene una lista de juegos los cuales fueron recomendado y copntiene recomendaciones positivas o neutrales (`reviews.recommend` = `True` y comentarios negativos) 
- `notrecommend.parquet` contiene aquellos juegos que no fueron recomendados por los usuarios y/o contienen recomendaciones negativas (`reviews.recommend` = `False` y comentarios negativos)
- `sentiments.parquet` contiene el total de reseñas positivas (`2`), neutras (`1`) y negativas (`0`) de la columna `sentiment_analysis` por año.
- `reviews_per_item.parquet` Este dataset se obtiene realizando las siguientes acciones: **Agrupación de reseñas por ítem**: El código recorre todas las reseñas en `n_reviews` y agrupa las reseñas por `item_id`, es decir, por videojuego. Cada `item_id` se mapea a una lista de reseñas correspondientes. **Concatenación de reseñas**: Para cada videojuego, se concatenan todas sus reseñas en una sola cadena de texto. **Vectorización TF-IDF**: Se aplica la vectorización TF-IDF a las reseñas concatenadas. La vectorización TF-IDF convierte el texto en un vector numérico que puede ser utilizado para el análisis de texto y machine learning. Se seleccionan las 1000 palabras más importantes para formar el vector. **Creación de DataFrame de vectores de reseñas**: Se crea un nuevo DataFrame que contiene el `id` del videojuego y su vector de reseñas correspondiente. Este DataFrame se guarda en un archivo parquet para su uso posterior. **Preparación de datos para recomendaciones de videojuegos**: Se seleccionan las columnas `item_id` y `sentiment_analysis` de `n_reviews` para crear un nuevo DataFrame `games_recommend`. Se eliminan las filas con valores nulos y se llenan los valores nulos restantes con 0. Este DataFrame también se guarda en un archivo parquet para su uso posterior.


## Desarrollo de API

En esta sección se detalla el desarrollo de la API que permite interactuar con el sistema de recomendación y acceder a diferentes funciones y servicios.

### Funciones disponibles

Las siguientes funciones están disponibles a través de la API:

1. **def PlayTimeGenre(genero : str)**
    Esta función devuelve el año de lanzamiento con más horas jugadas para un género de videojuego específico.

    Parámetros:
    genero (str): El género del videojuego. Debe ser una cadena de texto que represente un género de videojuego válido.

    Devuelve:
    dict: Un diccionario que contiene el año de lanzamiento con más horas jugadas para el género dado. 
          La clave del diccionario es una cadena de texto que dice "Año de lanzamiento con más horas jugadas para Género {genero}", 
          y el valor es un entero que representa el año. 
          Si el género dado no existe, el diccionario devuelto tendrá la clave "Error" y el valor "El género no existe".

    Ejemplo:
    >>> PlayTimeGenre('Action')
    {'Año de lanzamiento con más horas jugadas para Género Action': 2005}
    

2. **UserForGenre(genero : str)**
    Esta función devuelve el usuario que ha jugado más horas en un género de videojuego específico.

    Parámetros:
    genero (str): El género del videojuego. Debe ser una cadena de texto que represente un género de videojuego válido.

    Devuelve:
    dict: Un diccionario que contiene el usuario que ha jugado más horas para el género dado. 
          La clave del diccionario es una cadena de texto que dice "Usuario con más horas jugadas para Género {genero}", 
          y el valor es una lista de diccionarios, donde cada diccionario representa un año y las horas jugadas en ese año por el usuario. 
          Si el género dado no existe, el diccionario devuelto tendrá la clave "Error" y el valor "El género no existe".

    Ejemplo:
    >>> UserForGenre('Action')
    {'Usuario con más horas jugadas para Género Action': 'user123', [{'Año:2005, Horas:120'}, {'Año:2006, Horas:150'}]}
    """
3. **UsersRecommend(año : int)**
    Esta función devuelve los tres juegos más recomendados para un año específico.

    Parámetros:
    año (int): El año para el cual se buscan las recomendaciones. Debe ser un entero que represente un año válido.

    Devuelve:
    list: Una lista de diccionarios que contiene los tres juegos más recomendados para el año dado. 
          Cada diccionario tiene la clave "Puesto {i+1}" y el valor es el título del juego. 
          Si no hay juegos recomendados para el año dado, se devuelve un diccionario con la clave "No hay juegos recomendados para el año {año}".

    Ejemplo:
    >>> UsersRecommend(2020)
    [{'Puesto 1' : 'Juego A'}, {'Puesto 2' : 'Juego B'}, {'Puesto 3' : 'Juego C'}]
def UsersNotRecommend(año : int):
    """
    Esta función devuelve los tres juegos con las peores recomendaciones para un año específico.

    Parámetros:
    año (int): El año para el cual se buscan las recomendaciones. Debe ser un entero que represente un año válido.

    Devuelve:
    list: Una lista de diccionarios que contiene los tres juegos con las peores recomendaciones para el año dado. 
          Cada diccionario tiene la clave "Puesto {i+1}" y el valor es el título del juego. 
          Si no hay juegos con malas recomendaciones para el año dado, se devuelve un diccionario con la clave "No hay registros de juegos con peores recomendaciones para el año {año}".

    Ejemplo:
    >>> UsersNotRecommend(2020)
    [{'Puesto 1' : 'Juego A'}, {'Puesto 2' : 'Juego B'}, {'Puesto 3' : 'Juego C'}]
4. **UsersNotRecommend(año : int)**
    Esta función devuelve los tres juegos con las peores recomendaciones para un año específico.

    Parámetros:
    año (int): El año para el cual se buscan las recomendaciones. Debe ser un entero que represente un año válido.

    Devuelve:
    list: Una lista de diccionarios que contiene los tres juegos con las peores recomendaciones para el año dado. 
          Cada diccionario tiene la clave "Puesto {i+1}" y el valor es el título del juego. 
          Si no hay juegos con malas recomendaciones para el año dado, se devuelve un diccionario con la clave "No hay registros de juegos con peores recomendaciones para el año {año}".

    Ejemplo:
    >>> UsersNotRecommend(2020)
    [{'Puesto 1' : 'Juego A'}, {'Puesto 2' : 'Juego B'}, {'Puesto 3' : 'Juego C'}]

5. **sentiment_analysis(año : int)**
    Esta función realiza un análisis de sentimientos de las reseñas de videojuegos para un año específico.

    Parámetros:
    año (int): El año para el cual se realiza el análisis de sentimientos. Debe ser un entero que represente un año válido.

    Devuelve:
    dict: Un diccionario que contiene el recuento de reseñas negativas, neutrales y positivas para el año dado. 
          La clave del diccionario es una cadena de texto que dice "Negative={n}, Neutral={n}, Positive={n}", 
          donde {n} es el número de reseñas de cada tipo. 

    Ejemplo:
    >>> sentiment_analysis(2020)
    {'Negative=500, Neutral=200, Positive=300'}

6. **recomendacion_juego(id)**
    Esta función devuelve una lista de juegos recomendados basados en la similitud de las reseñas con un juego específico.

    Parámetros:
    id (int): El ID del juego para el cual se buscan recomendaciones. Debe ser un entero que represente un ID de juego válido.

    Devuelve:
    dict: Un diccionario que contiene una lista de juegos recomendados para el juego dado. 
          La clave del diccionario es una cadena de texto que dice "Los juegos recomendados para {id} son:", 
          y el valor es una lista de IDs de los juegos recomendados. 

    Ejemplo:
    >>> recomendacion_juego(123)
    {'Los juegos recomendados para 123 son:': [456, 789, 1011, 1213, 1415]}



### Sistema de recomendación.


El sistema de recomendación funciona en dos partes principales: la función `similarityCosine` y la función `recomendacion_juego`.

1. **Función `similarityCosine`**: Esta función toma dos vectores como entrada y calcula la similitud del coseno entre ellos. La similitud del coseno es una medida de la similitud entre dos vectores en un espacio multidimensional. Se calcula como el producto escalar de los vectores dividido por el producto de sus normas (o longitudes). Si alguna de las normas es cero, la función devuelve cero. La ecuación aplicada en esta función es:

$$
\text{similitud}(a, b) = \frac{a \cdot b}{||a||_2 \cdot ||b||_2}
$$

Donde:
- `a · b` es el producto escalar de `a` y `b`.
- `||a||_2` y `||b||_2` son las normas euclidianas de `a` y `b`.

2. **Función `recomendacion_juego`**: Esta función toma un ID de juego como entrada y devuelve una lista de juegos recomendados basados en la similitud del coseno de las reseñas de los juegos.

    - Primero, la función carga un conjunto de datos de reseñas y selecciona las reseñas para el juego dado.
    - Luego, calcula la similitud del coseno entre la primera reseña del juego dado y todas las demás reseñas en el conjunto de datos.
    - Después de calcular las similitudes, la función ordena los juegos por similitud del coseno en orden descendente y selecciona los 10 primeros.
    - Finalmente, la función devuelve una lista de los IDs de los juegos recomendados, excluyendo el juego original.

### Integración en FastAPI

El desarrollo de la API se ha realizado utilizando el framework FastAPI. El archivo `main.py` contiene la implementación de las funciones descritas anteriormente. Estas funciones estan en el notebook `funciones.ipynb` donde se realizaron los primeros desarrollos y pruebas.

Para integrar estas funciones en FastAPI y hacer que estén disponibles a través de la API, se ha implementado el archivo `main.py`. Este archivo define las rutas y los endpoints correspondientes a cada función. Además, se han establecido las validaciones necesarias para los parámetros de entrada y se han definido las respuestas esperadas.
.


## Análisis Exploratorio de los Datos (EDA)

Se llevó a cabo un análisis exploratorio de los datos con el objetivo de comprender la estructura y características del conjunto de datos de películas. A continuación, se presentan algunos aspectos destacados del análisis:

Es notorio que la mayoria de las reviews registradas corresponden de finales del año 2014 hasta finales del 2015, tal como se puede visualizar en el siguente histograma.

![Distribucion de recomendaciones por año](/images/distribucion_reviews.png)

De todas las recomendaciones realizadas por usuarios entre octubre del 2010 a diciembre del 2015 se puede notar que la mayoria corresponde a reviews negativas, tal como lo ilustra el grafico circular.

![Distribucion de recomendaciones](/images/dsitribucion_porcentual_reviews.png)


### Distribución de datos en playtime_forever

Se identificaron y analizaron los valores atípicos. Esto permitió comprender mejor la distribución de los datos y detectar posibles errores o discrepancias.

![Boxplot de playtime forever](/images/valores_atipicos_playtime_forever.png)

Debido a lo anterior se retiran los valores atipicos y obtenemos la siguiente distribución

![Distribucion playtime_forever](/images/dist_playtime_forever.png)


### Top 10 videojuegos mas jugados

Se procesaron los datos y se identificaron aquellos juegop que mas jugaron los usuarios.

![Top 10 Videojuegos](/images/top_ten.png)

### Videojuegio más jugado entre el 2010 al 2013

Se determina cúal es el videojuego mas demandado por año
![Mejor Videojuego](/images/top_videogame.png)

### Precios
La mayoria de los videojuegos se encuentran en un esquema free to play o de uso gratuito como se visualiza en el siguiente gráfico

![Densidad de precios](/images/densidad_precios.png)

Dado lo anterior seria error considerar unicamnte la data comprendida por el rango intercuartil, por ello se muestra la distribución de precios en escala logaritmica

![Precios de videojuegos](/images/Precios.png)

### Deploy
Para realizar un deploy del proyecto se utilizó [render.com/](https://render.com/) como plataforma. visite el deploy en 
https://https-6cp6.onrender.com/

### Video del proyecto
Consulte el video del proyecto desde [Youtube](https://youtu.be/tnmoQ9l_NzI)

https://youtu.be/tnmoQ9l_NzI