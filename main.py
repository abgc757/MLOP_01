import pandas as pd
import json
import numpy as np
from fastapi import FastAPI

app = FastAPI()

#Función Similitud de coseno
def similarityCosine(vector1, vector2):
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    if norm1 == 0 or norm2 == 0:
        return 0 
    else:
        return np.dot(vector1, vector2) / (norm1 * norm2)
    
# Función normalizacion de generos
def get_genre(genre_input: str):
    # Lista de géneros
    genres = ["Action", "Indie", "Adventure", "RPG", "Strategy", "Free to Play", 
              "Simulation", "Casual", "Massively Multiplayer", "Early Access", 
              "Sports", "Racing", "Utilities", "Design & Illustration", 
              "Animation & Modeling", "Video Production", "Web Publishing", 
              "Education", "Software Training", "Audio Production", "Photo Editing"]

    # Convierte el género de entrada y los géneros de la lista a minúsculas para la comparación
    genre_input_lower = genre_input.lower()
    genres_lower = [genre.lower() for genre in genres]

    # Comprueba si el género de entrada está en la lista de géneros
    if genre_input_lower in genres_lower:
        # Si está en la lista, devuelve el género tal cual aparece en la lista original
        return genres[genres_lower.index(genre_input_lower)]
    else:
        return None


@app.get("/")
def index():
    return {'Mensaje': 'Sistema de recomendacion'}

@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero : str):
    genero = get_genre(genero)
    if genero == None:
        return {"Error": "El género no existe"}
    else:
        ranking_genre = pd.read_parquet('dataset/ranking_genre.parquet')
        filtro = ranking_genre[ranking_genre['genres'] == genero]
        del ranking_genre
        return {f"Año de lanzamiento con más horas jugadas para Género {genero}" : int(filtro['year'].iloc[0])}

@app.get("/UserForGenre/{genero}")
def UserForGenre(genero : str):
    genero = get_genre(genero)
    if genero == None:
        return {"Error": "El género no existe"}
    else:
        usersXgenre = pd.read_parquet('dataset/user_genre.parquet')
        filtro = usersXgenre[usersXgenre['genres'] == genero]
        filtro_usuario = filtro.groupby('user_id')['playtime_forever'].sum().sort_values(ascending=False)
        resultado = filtro[filtro['user_id'] == filtro_usuario.index[0]].sort_values('year', ascending=False)
        i = 0
        lista = []
        while i < len(resultado):
            lista.append({f"Año:{int(resultado['year'].iloc[i])}, Horas:{int(resultado['playtime_forever'].iloc[i])}"})
            i += 1
        del usersXgenre
        return {f"Usuario con más horas jugadas para Género {resultado['genres'].iloc[0]}: {resultado['user_id'].iloc[0]},{lista}"}

@app.get("/UsersRecommend/{anio}")
def UsersRecommend(anio : int):
    recommend = pd.read_parquet('dataset/recommend.parquet')
    filtro = recommend[recommend['year'] == anio].sort_values(by=['count'], ascending=False).head(3)
    # del recommend
    if len(filtro) == 0:
        return {f"No hay juegos recomendados para el año {anio}"}
    else:
        i = 0
        lista = []
        while i < len(filtro):
            lista.append({f"Puesto {i+1}" : filtro['title'].iloc[i]})
            i += 1
        return lista

@app.get("/UsersNotRecommend/{anio}")
def UsersNotRecommend( anio : int ):
    notrecommend = pd.read_parquet('dataset/notrecommend.parquet')
    filtro = notrecommend[notrecommend['year'] == anio].sort_values(by=['year'], ascending=False).head(3)
    del notrecommend
    if len(filtro) == 0:
        return {f"No hay registros de juegos con peores recomendaciones para el año {anio}"}
    else:
        lista = []
        for i in range(0,3):
            lista.append({f"Puesto {i+1}" : filtro['title'].iloc[i]})
        return lista
    
@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis( anio : int ):
    sentiments  = pd.read_parquet('dataset\sentiments.parquet')
    filtro = sentiments[sentiments['release_date'].dt.year == anio]
    filtro['sentiment_analysis'] = filtro['sentiment_analysis'].astype(int)
    filtro['release_date'] = filtro['release_date'].astype('int64').astype('int32')
    resumen = filtro.groupby(filtro['sentiment_analysis'])['release_date'].count().to_dict()
    resultado = f"Negative={resumen.get(0, 0)}, Neutral={resumen.get(1, 0)}, Positive={resumen.get(2, 0)}"
    del sentiments
    return {resultado}

@app.get("/recomendacion_juego/{id}")
def recomendacion_juego(id : int):
    reviews  = pd.read_parquet('dataset/reviews_per_item.parquet')
    filtro = reviews[reviews['id'] == id]
    try:
        fila1 = filtro.iloc[0]
    except IndexError:
        return {"error": "No se encontraron datos para el ID del juego dado."}   
    fila1 = filtro.iloc[0]
    lista = []
    i = 0
    while i < len(reviews):
        fila2 = reviews.iloc[i]
        lista.append(similarityCosine(fila1,fila2))
        i += 1
    reviews['similarity_cosine'] = lista
    recomendacion =reviews[['id','similarity_cosine']].sort_values(by=['similarity_cosine'], ascending=False).head(10)
    del reviews
    rec = []
    j = 0
    while j < 6:
        if recomendacion['id'].iloc[j] != id:
            rec.append(recomendacion['id'].iloc[j])
        j+=1
    return {f"Los juegos recomendados para {id} son: {rec}"}