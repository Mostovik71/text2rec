import pandas as pd
from tabulate import tabulate
df1 = pd.read_csv('revsdata.csv')
df2 = pd.read_csv('cleanfilms.csv')
df3 = pd.read_csv('formatch.csv')

df1.drop('Unnamed: 0', inplace=True, axis=1)
df2.drop('Unnamed: 0', inplace=True, axis=1)
df2.columns = ['film_id', 'title']
dfx = pd.merge(df2, df3, on='title')
dfx.drop_duplicates(subset='film_id', inplace=True)
dfx.reset_index(drop=True, inplace=True)
dfy = pd.merge(dfx, df1, on='film_id')
dfy.to_csv('reviews.csv')


