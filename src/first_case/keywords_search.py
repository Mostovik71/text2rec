import re
import argparse
import pandas as pd
from typing import List


def regex_for_query_without_quotes(name, suffix = "ы"):
    if suffix != "": suffix += "?"
    return f"{name}{suffix}:([\w,.]+)"


def regex_for_query_with_quotes(name, suffix = "ы"):
    if suffix != "": suffix += "?"
    return f"{name}{suffix}:'([\w,. ]+)'"


class Handler:
    def __init__(self, column_name, value_type=str):
        self.column_name = column_name
        self.value_type = value_type
    def __call__(self, query: str, df: pd.DataFrame):
        raise NotImplementedError()


class ComplexHandler(Handler):
    def __init__(self, field_name, column_name, pred, cast_to_type=str, **kwargs):
        super().__init__(column_name, cast_to_type)
        pattern = regex_for_query_without_quotes(field_name, **kwargs)
        pattern_with_quotes = regex_for_query_with_quotes(field_name, **kwargs)
        self.regex = re.compile(pattern)
        self.regex_with_quotes = re.compile(pattern_with_quotes)
        self.pred = pred
    def __call__(self, query: str, df: pd.DataFrame):
        search_result = self.regex.findall(query)
        search_result_with_quotes = self.regex_with_quotes.findall(query)
        if not len(search_result) and not len(search_result_with_quotes): 
            return df
        column = df[self.column_name]
        first_result: str = search_result[0] if len(search_result) else search_result_with_quotes[0]
        first_result = first_result.split(',')
        result = pd.Series([True for _ in range(column.size)], index=column.index)
        try:
            for value in first_result:
                value = self.value_type(value)
                result &= self.pred(column, value)
        except:
            return df
        return df[result]


class Pipeline:
    def __init__(self, handlers: List[Handler]):
        self.handlers = handlers
    def __call__(self, query, df):
        for handler in self.handlers:
            df = handler(query, df)
        return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', metavar="query")
    args = parser.parse_args()
    query = args.query

    year_handler = ComplexHandler("год", "Year", lambda s, r: s == r, int)
    director_handler = ComplexHandler("режиссер", "Director", lambda s, r: s.str.contains(r))
    genre_handler = ComplexHandler("жанр", "Genres", lambda s, r: s.str.contains(r))
    actor_handler = ComplexHandler("актер", "Actors", lambda s, r: s.str.contains(r))
    country_handler = ComplexHandler("страна", "Countries", lambda s, r: s.str.contains(r))
    rating_handler = ComplexHandler("рейтинг", "Rating", lambda s, r: s >= r, float)

    pipeline = Pipeline([
        rating_handler, year_handler, director_handler, 
        genre_handler, actor_handler, country_handler
    ])

    df = pd.read_csv("top250.csv")
    df = pipeline(query, df)
    print(df)


if __name__ == "__main__":
    main()
