from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import fuzz

keywords = pd.read_csv('formatch.csv')
api_client = KinopoiskApiClient("...")
films = []

try:
    for i in tqdm(keywords.iterrows()):
        request = SearchByKeywordRequest(str(i[1].title))
        response = api_client.films.send_search_by_keyword_request(request)

        try:
            film_id1 = response.films[0].film_id
            films.append((film_id1, str(i[1].title)))
        except Exception:
            pass
finally:
    filns = pd.DataFrame(films)
    filns.to_csv('matchednew.csv')
    # keywords['film_id'] = pd.Series(films)
    # keywords.to_csv('matchednew.csv')
