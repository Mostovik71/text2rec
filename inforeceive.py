from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.staff.staff_request import StaffRequest
import pandas as pd
from tqdm import tqdm

api_client = KinopoiskApiClient("f35b97c8-0485-4c4c-be05-ffd04d1ddfa2")
ids = pd.read_csv('ids.csv')
df = pd.DataFrame([])


# df.columns = ['Id', 'Director', 'Actors']
def info(id):
    actors = []
    request = StaffRequest(id)
    response = api_client.staff.send_staff_request(request)
    for i in response.items:
        if i.profession_text == 'Режиссеры':
            director = i.name_ru
        if i.profession_text == 'Актеры':
            actors.append(i.name_ru)
    return id, director, ', '.join(str(x) for x in actors)


# for i in tqdm(ids['ids']):
#     kek = info(i)
#     df = df.append(pd.DataFrame(kek).T, ignore_index=True)
kek = info(507)
# df.columns = ['FilmId', 'Director', 'Actors']
# df.to_csv('iddiract.csv', index=False)
