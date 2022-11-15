import pandas as pd
from tabulate import tabulate
import nltk
import string
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

df = pd.read_csv('kwrdsimprvd.csv')
# df.drop('Unnamed: 0', inplace=True, axis=1)
patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
stopwords_ru.extend(['это', 'нею'])
morph = MorphAnalyzer()
df.fillna('string', inplace=True)


def lemma(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split(' '):

        if token and token not in stopwords_ru:
            token = token.strip()

            token = morph.normal_forms(token)[0]
            tokens.append(token)

    return ' '.join(tokens)


def split_into_words(line):
    word_regex_improved = r"(\w[\w']*\w|\w)"
    word_matcher = re.compile(word_regex_improved)
    return word_matcher.findall(line)


df.review1 = df.review1.apply(lemma)
df.review1 = df.review1.apply(lambda x: ' '.join(split_into_words(x)))
df.review2 = df.review2.apply(lemma)
df.review2 = df.review2.apply(lambda x: ' '.join(split_into_words(x)))
df.review3 = df.review3.apply(lemma)
df.review3 = df.review3.apply(lambda x: ' '.join(split_into_words(x)))
df.to_csv('dfforbow.csv', index=False)
