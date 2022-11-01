import re
import pandas as pd
from tabulate import tabulate


def main():
    df1 = pd.read_csv('iddiract.csv', index_col='FilmId')
    df2 = pd.read_csv('moreinfo.csv', index_col='FilmId')
    dfx = pd.concat([df2, df1], axis=1)
    dfx['Countries'] = dfx['Countries'].apply(lambda x: ', '.join(str(y) for y in re.findall(r'[А-я]+', x)))
    dfx['Genres'] = dfx['Genres'].apply(lambda x: ', '.join(str(y) for y in re.findall(r'[А-я]+', x)))
    dfx['Countries'] = dfx['Countries'].str.replace("Новая, Зеландия", "Новая Зеландия")
    print(tabulate(dfx, headers='keys'))
    dfx.to_csv('top250.csv')


if __name__ == "__main__":
    main()
