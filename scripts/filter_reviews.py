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


def filter_reviews(reviews: pd.DataFrame):
    filtered = reviews.copy(deep=True)
    url_regex = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    filtered["description"] = filtered["description"].str.replace(url_regex, "", regex=True)
    filtered["description"] = filtered["description"].str.replace("([…:!\.\?]?) *(?:[\r\n])+", func, regex=True)
    filtered["description"] = replace_repeated_html_tags(filtered["description"])
    filtered["description"] = filtered["description"].str.replace("<\/?[\w\d\. =':\/]+>", "", regex=True)
    filtered["description"] = filtered["description"].str.replace("[\u0301\u200b\u2122\ufeff]", "", regex=True)
    filtered["description"] = filtered["description"].str.replace(" *\t *", " ", regex=True)
    filtered["description"] = filtered["description"].str.replace("\u2028", ", ")
    filtered["description"] = filtered["description"].str.replace("\u00E9", "e")
    return filtered


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    
    filename = args.filename
    reviews = pd.read_csv(filename)
    filtered = filter_reviews(reviews)

    filtered.to_csv(f"{filename[:-4]}_filtered.csv", index=False)


if __name__ == "__main__":
    main()
