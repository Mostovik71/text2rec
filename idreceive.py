from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_top_request import FilmTopRequest
from kinopoisk_unofficial.model.dictonary.top_type import TopType
import pandas as pd
df = pd.read_csv('ids.csv')
api_client = KinopoiskApiClient("f35b97c8-0485-4c4c-be05-ffd04d1ddfa2")
request = FilmTopRequest(TopType.TOP_250_BEST_FILMS)
response = api_client.films.send_film_top_request(request)
ids = [i.film_id for i in response.films]

dfx = df['ids'].append(pd.Series(ids, name='ids'), ignore_index=True)
dfx.to_csv('ids.csv', index=False)

