import pandas as pd
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.reviews.reviews_request import ReviewsRequest
from tqdm import tqdm

api_client = KinopoiskApiClient("...")
df = pd.read_csv('cleanfilms.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
df.columns = ['film_id', 'title']
df = df[df['film_id'].notnull()]
df = df[df['film_id'] != 0]
df['film_id'] = df['film_id'].apply(lambda x: int(x))
df.drop_duplicates(subset=['film_id'], inplace=True)

reviews = []
try:
    for i in tqdm(df.iterrows()):
        try:
            request = ReviewsRequest(i[1].film_id)
            response = api_client.reviews.send_reviews_request(request)

            rev = response.reviews
            reviews.append((rev, i[1].film_id))
        except Exception:
            pass
finally:
    filns = pd.DataFrame(reviews)
    filns.to_csv('matchedreviews.csv')
