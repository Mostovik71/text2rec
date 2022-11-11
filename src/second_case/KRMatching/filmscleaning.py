import pandas as pd
from tabulate import tabulate
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from tqdm import tqdm

api_client = KinopoiskApiClient("...")
df1 = pd.read_csv('matchednew.csv')
df1.drop('Unnamed: 0', inplace=True, axis=1)
df1.columns = ['film_id', 'title']
df2 = pd.read_csv('formatch.csv')
dfx = pd.merge(df1, df2, on='title')
dfx = dfx[dfx['film_id'].notnull()]
dfx.drop_duplicates(subset='film_id', inplace=True)
films = []
try:
    for i in dfx.iterrows():
        request = FilmRequest(i[1].film_id)
        response = api_client.films.send_film_request(request)
        if i[1].title == response.film.name_ru:
            films.append((i[1].film_id, str(i[1].title)))
finally:
    filns = pd.DataFrame(films)
    filns.to_csv('cleanfilms.csv')