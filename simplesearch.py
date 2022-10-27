import pandas as pd
from tabulate import tabulate
from fuzzywuzzy import fuzz

df = pd.read_csv('top250.csv', index_col='FilmId')
df = df[['Title', 'Director', 'Genres', 'Actors', 'ShortDescription', 'Year']]
df['Actors'] = df['Actors'].apply(lambda x: ', '.join(str(i) for i in x.split(', ')[0:5]))
df['Year'] = df['Year'].apply(lambda x: str(x))
df['all'] = df['Director'] + ', ' + df['Actors'] + ', ' + df['Year'] + ', ' + df['Genres']
df['all'] = df['all'].apply(lambda x: x.lower())

querystr = 'стивен спилберг боевик 1998 история'
# query = pd.concat([pd.Series(name='query'), df['all'], df['Title']], axis=1)
# query['query'].fillna(querystr, inplace=True)
final = pd.DataFrame([])

for i, k in zip(df['all'], df['Title']):
        final = final.append(pd.DataFrame([querystr, i, fuzz.token_set_ratio(querystr, i), k]).T)
final.columns = ['Query', 'Data', 'Similarity', 'Title']
final_df = final.sort_values('Similarity', ascending=False)
print(tabulate(final_df, headers='keys'))
