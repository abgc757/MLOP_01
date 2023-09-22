# <h1 align=center> **Sistema de Recomendación**</h1>
# <h2> **Proyecto individual Nº1**</h1>
# `Machine Learning Operations (MLOps)`
## **Henry's Labs**
### *Por Abraham Gómez DataPT01*

El objetivo principal del proyecto es crear un sistema de recomendación de videojuegos utilizando técnicas de aprendizaje automático (Machine Learning). El proyecto se divide en diferentes etapas:

1. Extracción, transformación y carga (ETL): Se realiza la extracción de datos del conjunto de datos "dataset\australian_user_reviews.json", "dataset\australian_users_items.json" y "dataset/output_steam_games.json". Se aplican transformaciones para estandarizar los archivos ya que el formato JSON no se encuentra estandarizado, es por ello que deben de tranformarse y almacenarse en archivos parquet de modo que se limite el espacio en memoria, ademas se desanidan los items, recomendaciones y se transforma las recomendaciones en una variable discreta "Sentiment_analisys", ademas es necesario eliminar algunos registros nulos que no aportan información relevante.

2. Desarrollo de API: Se crean funciones en el archivo "funciones.ipynb" que proporcionan diferentes consultas y funcionalidades para integrarlas en el código y utilizarlas en FastAPI. Las funciones disponibles userdata( User_id : str ), countreviews( YYYY-MM-DD y YYYY-MM-DD : str ), genre( género : str ), userforgenre( género : str ), developer( desarrollador : str ), etc.

3. Análisis exploratorio de los datos (EDA): Se realiza un análisis exploratorio de los datos para comprender mejor la información a la que se tiene acceso. Se exploran valores atípicos, se analiza el tiempo de juego para varios videojuegos, se obtienen los top 10 de videojuegos más jugados, los videojuegos mas jugado entre el 2010 y 2013 y el top 10 desarrolladores que recaudaron.

4. Sistema de recomendación: Se implementa un sistema de recomendación dado el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado

## Tabla de contenidos

- [ETL (Extracción, Transformación y Carga)](#etl-extracción-transformación-y-carga)
- [Desarrollo de API](#desarrollo-de-api)
- [Análisis Exploratorio de los Datos (EDA)](#análisis-exploratorio-de-los-datos-eda)
- [Sistema de Recomendación](#sistema-de-recomendación)
- [Referencias](#referencias)

## ETL (Extracción, Transformación y Carga)

1. Lectura y Procesamiento de Datos:

- Lee los datos de varios archivos JSON y los convierte en DataFrames de Pandas. Estos DataFrames contienen información sobre reseñas de usuarios, juegos de Steam y géneros de juegos.
- Realiza algunas limpiezas de datos, como eliminar registros duplicados y reemplazar valores nulos.

2. Análisis de Sentimiento:

- Utiliza la biblioteca NLTK para realizar un análisis de sentimiento de las reseñas de los usuarios. Asigna un valor de sentimiento (positivo, neutral o negativo) a cada reseña.

3. Generación de Estadísticas:

- Calcula estadísticas como el gasto promedio de los usuarios, el porcentaje de recomendación en base a las reseñas y la cantidad de ítems de cada usuario.

4. Ranking de Géneros de Juegos:

- Calcula un ranking de géneros de juegos basado en el tiempo de juego acumulado de los usuarios en cada género.


## Desarrollo de API

En esta sección se detalla el desarrollo de la API que permite interactuar con el sistema de recomendación y acceder a diferentes funciones y servicios.

### Funciones disponibles

Las siguientes funciones están disponibles a través de la API:

1. **`userdata(User_id: str)`**
   - Descripción: Esta función toma un identificador de usuario de Steam como entrada y devuelve información sobre el usuario, incluido el gasto total en juegos, el porcentaje de recomendación basado en las reseñas y la cantidad de ítems en su posesión.
   - Uso: `userdata('kimjongadam')`

2. **`countreviews(start_date: str, end_date: str)`**
   - Descripción: Esta función cuenta el número de reseñas de usuarios y calcula el porcentaje de recomendaciones positivas dentro de un rango de fechas específico.
   - Uso: `countreviews('2010-10-15', '2010-12-20')`

3. **`genre(genre: str)`**
   - Descripción: Esta función muestra la posición de un género de juego en el ranking de géneros, basado en el tiempo total de juego acumulado por los usuarios en ese género.
   - Uso: `genre('RPG')`

4. **`userforgenre(genre: str)`**
   - Descripción: Proporciona una lista de los 5 usuarios con más horas de juego en un género de juego específico, incluyendo sus identificadores de usuario y URL de perfil.
   - Uso: `userforgenre('RPG')`

5. **`developer(developer: str)`**
   - Descripción: Calcula la cantidad de contenido gratuito lanzado por un desarrollador de juegos en cada año y muestra el porcentaje de contenido gratuito en relación con el total.
   - Uso: `developer('SmiteWorks USA, LLC')`

6. **`sentiment_analysis(year: int)`**
   - Descripción: Realiza un análisis de sentimiento de las reseñas de juegos lanzados en un año específico y devuelve la cantidad de reseñas clasificadas como negativas, neutrales y positivas.
   - Uso: `sentiment_analysis(2011)`

7. **`recomendacion_juego(game_id: int)`**
   - Descripción: Proporciona una lista de 5 juegos recomendados que son similares al juego especificado por su identificador de producto (game_id). La recomendación se basa en etiquetas (tags) asociadas a los juegos.
   - Uso: `recomendacion_juego(570)`

8. **`recomendacion_juego_ml(game_id: int)`**
   - Descripción: Esta función proporciona una lista de 5 juegos recomendados similares al juego especificado por su identificador de producto (game_id) utilizando un modelo de recomendación de aprendizaje automático basado en similitud de etiquetas (tags).
   - Uso: `recomendacion_juego_ml(570)`


### Integración en FastAPI

El desarrollo de la API se ha realizado utilizando el framework FastAPI. El archivo `main.py` contiene la implementación de las funciones descritas anteriormente. Estas funciones se han basado en el notebook `funciones.ipynb` donde se realizaron los primeros desarrollos y pruebas.

Para integrar estas funciones en FastAPI y hacer que estén disponibles a través de la API, se ha implementado el archivo `main.py`. Este archivo define las rutas y los endpoints correspondientes a cada función. Además, se han establecido las validaciones necesarias para los parámetros de entrada y se han definido las respuestas esperadas.
.


## Análisis Exploratorio de los Datos (EDA)

Se llevó a cabo un análisis exploratorio de los datos con el objetivo de comprender la estructura y características del conjunto de datos de películas. A continuación, se presentan algunos aspectos destacados del análisis:

### Distribución de datos en playtime_forever

Se identificaron y analizaron los valores atípicos. Esto permitió comprender mejor la distribución de los datos y detectar posibles errores o discrepancias.

![Distribucion playtime_forever](/images/dist_playtime_forever.png)

### Top 10 videojuegos mas jugados

Se procesaron los datos y se identificaron aquellos juegop que mas jugaron los usuarios.

![Top 10 Videojuegos](/images/top_ten.png)

### Videojuegio más jugado entre el 2010 al 2013

Se determina cúal es el videojuego mas demandado por año
![Mejor Videojuego](/images/top_videogame.png)

### Ventas por desarrollador

Se identifican los 10 desarroladores con más ventas 

![Ventas por desarrollador](/images/Top10dev.png)


### deploy
visita el deploy en 
https://https-6cp6.onrender.com/

Video Youtube
https://youtu.be/tnmoQ9l_NzI