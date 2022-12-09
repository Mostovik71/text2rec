import re
import argparse
import pandas as pd
from typing import List


def regex_for_query_without_quotes(name, suffix = "ы"):
    if suffix != "": suffix += "?"
    return f"{name}{suffix}:([\w,.]+)"


def regex_for_query_with_quotes(name, quote_type="'", suffix = "ы"):
    if suffix != "": suffix += "?"
    return f"{name}{suffix}:{quote_type}([\w,. ]+){quote_type}"


def val_in_column(column: pd.Series, value: str):
    return column.str.contains(value)


class TagSeach:
    def __init__(self, tag_name, tag_suffix="ы"):
        single_value_pattern = regex_for_query_without_quotes(tag_name, tag_suffix)
        multiple_values_patterns = [
            regex_for_query_with_quotes(tag_name, quote_type=qt, suffix=tag_suffix) 
            for qt in ["'", "\""]
        ]
        self.patterns = [single_value_pattern] + multiple_values_patterns
        self.regexps = [re.compile(p) for p in self.patterns]
    def search(self, query) -> re.Match:
        for regexp in self.regexps:
            match = regexp.search(query)
            if match:
                return match
        return None


class Handler:
    def __init__(self, column_name, value_type=str):
        self.column_name = column_name
        self.value_type = value_type
    def __call__(self, df: pd.DataFrame, query: str):
        raise NotImplementedError()


class ComplexHandler(Handler):
    def __init__(self, field_name, column_name, pred=val_in_column, cast_to_type=str, **kwargs):
        super().__init__(column_name, cast_to_type)
        self.tag_search = TagSeach(field_name, **kwargs)
        self.pred = pred
    def __call__(self, df: pd.DataFrame, query: str):
        correct_match = self.tag_search.search(query)
        if correct_match is None:
            return df, query
        column = df[self.column_name]
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', metavar="query")
    args = parser.parse_args()
    query = args.query

    year_handler = ComplexHandler("год", "Year", lambda c, v: c == v, int)
    rating_handler = ComplexHandler("рейтинг", "Rating", lambda c, v: c >= v, float)
    director_handler = ComplexHandler("режиссер", "Director")
    genre_handler = ComplexHandler("жанр", "Genres")
    actor_handler = ComplexHandler("актер", "Actors")
    country_handler = ComplexHandler("страна", "Countries")

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
