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
    def __call__(self, df: pd.DataFrame, query: str):
        raise NotImplementedError()


class ComplexHandler(Handler):
    def __init__(self, field_name, column_name, pred, cast_to_type=str, **kwargs):
        super().__init__(column_name, cast_to_type)
        pattern = regex_for_query_without_quotes(field_name, **kwargs)
        pattern_with_quotes = regex_for_query_with_quotes(field_name, **kwargs)
        self.regex = re.compile(pattern)
        self.regex_with_quotes = re.compile(pattern_with_quotes)
        self.pred = pred
    def __call__(self, df: pd.DataFrame, query: str):
        search_match = self.regex.search(query)
        search_match_with_quotes = self.regex_with_quotes.search(query)
        if search_match is None and search_match_with_quotes is None: 
            return df, query
        column = df[self.column_name]
        correct_match = search_match if search_match is not None else search_match_with_quotes
        filtered_query = query.replace(correct_match.group(), "")
        first_result: str = correct_match.group(1)
        first_result = first_result.split(',')
        result = pd.Series([True for _ in range(column.size)], index=column.index)
        try:
            for value in first_result:
                value = self.value_type(value)
                result &= self.pred(column, value)
        except:
            return df, filtered_query
        return df[result], filtered_query


class Pipeline:
    def __init__(self, handlers: List[Handler]):
        self.handlers = handlers
    def __call__(self, df, query):
        for handler in self.handlers:
            df, query = handler(df, query)
        return df, query


def val_in_column(column: pd.Series, value: str):
    return column.str.contains(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', metavar="query")
    args = parser.parse_args()
    query = args.query

    year_handler     = ComplexHandler("год",      "Year",      lambda c, v: c == v, int)
    director_handler = ComplexHandler("режиссер", "Director",  val_in_column)
    genre_handler    = ComplexHandler("жанр",     "Genres",    val_in_column)
    actor_handler    = ComplexHandler("актер",    "Actors",    val_in_column)
    country_handler  = ComplexHandler("страна",   "Countries", val_in_column)
    rating_handler   = ComplexHandler("рейтинг",  "Rating",    lambda c, v: c >= v, float)

    pipeline = Pipeline([
        rating_handler, year_handler, director_handler, 
        genre_handler, actor_handler, country_handler
    ])

    df = pd.read_csv("top250.csv")
    df, query = pipeline(df, query)
    print(df)
    print(query)


if __name__ == "__main__":
    main()
