import pandas as pd
from tabulate import tabulate
import nltk
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import pycountry

df = pd.read_csv('reviews.csv')
df.drop('Unnamed: 0', inplace=True, axis=1)
patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
for i in df.iterrows():
    i[1].keywords = ' '.join([word for word in i[1].keywords.split(', ') if word not in i[1].title.split(' ')][2:])
    # print(i[1].keywords)
df.keywords = df.keywords.apply((lambda x: x.replace('/', ',')))
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()
keywords = []
for i in df.iterrows():
    keywords.append(' '.join([word for word in i[1].keywords.split(', ') if word not in i[1].title.split(' ')][2:]))
df.keywords = pd.Series(keywords)

def lemmakwrds(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split(' '):

        if token and token not in stopwords_ru:
            token = token.strip()

            token = morph.normal_forms(token)[0]
            tokens.append(token)

    return ' '.join(tokens)


df.keywords = df.keywords.apply(lemmakwrds)

df.to_csv('kwrdsimprvd.csv', index=False)
