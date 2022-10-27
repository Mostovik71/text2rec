import pandas as pd
from tqdm import tqdm
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest

api_client = KinopoiskApiClient("f35b97c8-0485-4c4c-be05-ffd04d1ddfa2")
ids = pd.read_csv('ids.csv')
df = pd.DataFrame([])


def info(id):
    request = FilmRequest(id)
    response = api_client.films.send_film_request(request)
    resp = response.film
    return resp.kinopoisk_id, resp.name_ru, resp.rating_kinopoisk, resp.year, resp.film_length, resp.countries, resp.genres, resp.short_description

kek = info(507)
print(kek)
for i in tqdm(ids['ids']):
    kek = info(i)
    df = df.append(pd.DataFrame(kek).T, ignore_index=True)

df.columns = ['FilmId', 'Title', 'Rating', 'Year', 'Duration', 'Countries', 'Genres', 'ShortDescription']
df.to_csv('moreinfo.csv', index=False)
