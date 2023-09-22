import pandas as pd
from fastapi import FastAPI
import json
import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI()

# Cargar DataFrames
'''
reviews  = pd.read_parquet('dataset/australian_user_reviews.parquet')
items =  pd.read_parquet('dataset/australian_users_items.parquet')

ranking_genre = pd.read_parquet('dataset/ranking_genre.parquet')
usersXgenre = pd.read_parquet('dataset/user_genre.parquet')
'''

@app.get("/")
def index():
    return {'Mensaje': 'Sistema de recomendacion'}

@app.get("/UserData/{User_id}")
def userdata(User_id:str):
    reviews  = pd.read_parquet('dataset/australian_user_reviews.parquet')
    games =  pd.read_parquet('dataset/output_steam_games.parquet')
    Consumo = 0
    user_data = reviews[reviews['user_id'] == User_id]
    item_count = user_data['user_id'].count()
    for i in user_data['item_id']:
        filtro = games[games['id'] == i]
        precio = filtro.iloc[0]['price'] - filtro.iloc[0]['discount_price']
        Consumo = Consumo + precio
    recomemdaciones = reviews[reviews['user_id'] == User_id]
    cierto = recomemdaciones[recomemdaciones['recommend'] == True].count()
    porcentaje = cierto[0]  / item_count
    resultado =  {"Consumo del usuario": float(Consumo), "% de recomendación": round(float(porcentaje) * 100,2), "Cantidad de items": int(item_count)}
    del reviews
    del games
    return resultado

@app.get("/countreviews/{fecha1},{fecha2}")
def countreviews(fecha1:str,fecha2:str):
    reviews  = pd.read_parquet('dataset/australian_user_reviews.parquet')
    if fecha1 > fecha2:
        return {"Error":"Ingrese correctamente las fechas"}
    else:
        filtro = reviews[(reviews['posted_date'] >= fecha1) & (reviews['posted_date'] <= fecha2) ]
        cierto = filtro[filtro['recommend'] == True].count()
        Tot_rev = filtro['recommend'].count()
        porcentaje = cierto['recommend'] / Tot_rev
    resultado = {'Cantidad de Reviews': int(filtro['recommend'].count()), '% de recomendaciones': round(float(porcentaje),2) * 100}
    del reviews
    return resultado


@app.get("/genre/{genero}")
def genre(genero:str):
    ranking_genre = pd.read_parquet('dataset/ranking_genre.parquet')
    resultado = {"Puesto numero:": int(ranking_genre[ranking_genre['genres'] == genero].index[0] + 1) }
    del ranking_genre
    return resultado

@app.get("/userforgenre/{genero}")
def userforgenre(genero:str):
    usersXgenre = pd.read_parquet('dataset/user_genre.parquet')
    filtro = usersXgenre[usersXgenre['genres'] == genero].sort_values(by='playtime_forever', ascending=False).head(5)
    lista = []
    j = 0
    for i in filtro['user_id_y']:
        filtro2 = filtro[filtro['user_id_y'] == i]
        res = {"Posicion": int(j + 1), "Usuario_Id":str(i),"Url_Usuario":str(filtro2['user_url'].iloc[0])}
        lista.append(res)
        j = j + 1
    del usersXgenre
    return lista

@app.get("/developer/{desarrollador}")
def developer(desarrollador:str):
    games =  pd.read_parquet('dataset/output_steam_games.parquet')
    filtro = games[games['developer'] == desarrollador].dropna(subset=['release_date'])
    filtro = filtro[filtro['release_date'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)]
    filtro['release_date'] = pd.to_datetime(filtro['release_date'], format="%Y-%m-%d")
    filtro_free = filtro[filtro['price'] == 0]
    total = filtro.groupby(filtro['release_date'].dt.year)['price'].count()
    free = filtro_free.groupby(filtro_free['release_date'].dt.year)['price'].count()
    resultado = pd.DataFrame({'free': total, 'total': free})
    resultado = resultado.fillna(0)
    resultado['free'] = resultado['free'].astype(int)
    resultado['total'] = resultado['total'].astype(int)
    lista = []
    
    for i in range(len(resultado)):
        a = resultado['free'].iloc[i]
        b = resultado['total'].iloc[i]
        if b == 0:
            porcentaje = None
        else:
            try:
                porcentaje = round(b * 100 / a, 2)
            except ZeroDivisionError:
                porcentaje = 0.0  # O cualquier otro valor predeterminado
            
        res = {"Año": int(resultado.index[i]), "Contenido free": int(a), "% free": porcentaje}
        lista.append(res)
    
    # Limpieza de variables intermedias
    del games
    del filtro
    del filtro_free
    return lista

@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis(anio:int):
    sentiments  = pd.read_parquet('dataset/sentiments.parquet')
    filtro = sentiments[sentiments['release_date'].dt.year == anio]
    filtro['sentiment_analysis'] = filtro['sentiment_analysis'].astype(int)
    filtro['release_date'] = filtro['release_date'].astype('int64').astype('int32')
    resumen = filtro.groupby(filtro['sentiment_analysis'])['release_date'].count().to_dict()
    resultado = {"Negative=": resumen.get(0, 0), "Neutral=": resumen.get(1, 0), "Positive=": resumen.get(2, 0)}
    del sentiments
    return resultado
