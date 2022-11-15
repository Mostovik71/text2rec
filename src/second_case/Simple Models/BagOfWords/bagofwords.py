import pandas as pd
from tabulate import tabulate
from nltk import word_tokenize
import nltk
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv('dfforbow.csv')
df.fillna('string', inplace=True)
df.keywords = df.keywords.apply(lambda x: word_tokenize(x))
df.keywords = df.keywords.apply(lambda x: nltk.Text(x))
df.keywords = df.keywords.apply(lambda x: FreqDist(x).most_common())

df.review1 = df.review1.apply(lambda x: word_tokenize(x))
df.review1 = df.review1.apply(lambda x: nltk.Text(x))
df.review1 = df.review1.apply(lambda x: FreqDist(x).most_common())
df.review2 = df.review2.apply(lambda x: word_tokenize(x))
df.review2 = df.review2.apply(lambda x: nltk.Text(x))
df.review2 = df.review2.apply(lambda x: FreqDist(x).most_common())
df.review3 = df.review3.apply(lambda x: word_tokenize(x))
df.review3 = df.review3.apply(lambda x: nltk.Text(x))
df.review3 = df.review3.apply(lambda x: FreqDist(x).most_common())

text = df.sample(1)
kwrds = ' '.join([i[0] for i in text.keywords.item()])
review1 = ' '.join([i[0] for i in text.review1.item()][:len(kwrds)])
review2 = ' '.join([i[0] for i in text.review2.item()][:len(kwrds)])
review3 = ' '.join([i[0] for i in text.review3.item()][:len(kwrds)])

fig, axs = plt.subplots(2, 2)
axs[0, 0].imshow(WordCloud().generate(kwrds))
axs[0, 0].set_title('keywords')
axs[0, 1].imshow(WordCloud().generate(review1))
axs[0, 1].set_title('review1')
axs[1, 0].imshow(WordCloud().generate(review2))
axs[1, 0].set_title('review2')
axs[1, 1].imshow(WordCloud().generate(review3))
axs[1, 1].set_title('review3')
plt.show()
