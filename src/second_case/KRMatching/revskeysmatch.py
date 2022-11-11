import pandas as pd
import re
import kinopoisk_unofficial
from tabulate import tabulate

df = pd.read_csv('matchedreviews.csv')
#df.drop('Unnamed: 0', inplace=True, axis=1)
df = df[df['review'].notnull()]
revsdata = pd.DataFrame()
try:
    for i, o in zip(df.review, df.film_id):

        rews = []
        lst = i.split('Review')
        for k in range(0, len(lst), 2):
            nums = re.findall(r'\b\d+\b', lst[k])
            if nums == [] or len(nums) == 1:
                continue
            else:
                rews.append((lst[k], int(nums[6])))
        vals = sorted(rews, key=lambda x: x[1], reverse=True)
        vals = vals[0:3] if len(vals) > 1 else vals  # Берем 3 рецензии с максимальным рейтингом
        try:
            rev = pd.Series([x[0].split('review_description=')[1] for x in vals])
        except Exception:
            rev = pd.Series([0, 0, 0])
        revsdata = revsdata.append(pd.concat([pd.Series(int(o)), rev], axis=0, ignore_index=True), ignore_index=True)

finally:
    revsdata.columns = ['film_id', 'review1', 'review2', 'review3']
    # print(revsdata)
    # revsdata = revsdata[revsdata]

    revsdata.to_csv('revsdata.csv')
