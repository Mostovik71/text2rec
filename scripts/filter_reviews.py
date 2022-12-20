import re
import argparse
import pandas as pd


def func(match: re.Match):
    group = match.group(1)
    if group == "":
        return ". "
    return f"{group[0]} "


def tags(match: re.Match):
    return match.group(1)


def replace_repeated_html_tags(series: pd.Series):
    new = series
    while True:
        old = new
        new = old.str.replace("<\w+>([^<>]*)<\/\w+>", tags, regex=True)
        if (old == new).all():
            break
    return new


def filter_reviews(reviews: pd.DataFrame, column_name):
    filtered = reviews.copy(deep=True)
    url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    filtered[column_name] = filtered[column_name].str.replace(url_regex, "", regex=True)
    filtered[column_name] = filtered[column_name].str.replace("([…:!\.\?]?) *(?:[\r\n])+", func, regex=True)
    filtered[column_name] = replace_repeated_html_tags(filtered[column_name])
    filtered[column_name] = filtered[column_name].str.replace("<\/?[\w\d\. =':\/]+>", "", regex=True)
    filtered[column_name] = filtered[column_name].str.replace("[\u0301\u200b\u2122\ufeff]", "", regex=True)
    filtered[column_name] = filtered[column_name].str.replace(" *\t *", " ", regex=True)
    filtered[column_name] = filtered[column_name].str.replace("\u2028", ", ")
    filtered[column_name] = filtered[column_name].str.replace("\u00E9", "e")
    return filtered


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("column_name", nargs="?", default="description")
    args = parser.parse_args()
    
    filename = args.filename
    column_name = args.column_name
    reviews = pd.read_csv(filename)
    filtered = filter_reviews(reviews, column_name)

    filtered.to_csv(f"{filename[:-4]}_filtered.csv", index=False)


if __name__ == "__main__":
    main()
