import time
import argparse
import traceback
import pandas as pd
from googletrans import Translator
from tqdm import tqdm


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, typ, value, traceback):
        self.elapsed = time.perf_counter() - self.start


def translate_reviews(reviews: pd.DataFrame, column_name) -> pd.DataFrame:
    translated_reviews = []
    translator = Translator()
    translated = reviews.copy(deep=True)
    reviews_text = reviews[column_name]
    for i, text_ru in enumerate(tqdm(reviews_text)):
        with Timer() as timer:
            try:
                text_en = translator.translate(text_ru[:5000], src="ru", dest="en").text
            except:
                traceback.print_exc()
                break
            translated_reviews.append(text_en)
        time.sleep(max(0.4 - timer.elapsed, 0))
    if i + 1 != len(reviews_text):
        partial_translated = translated.iloc[:i].copy(deep=True)
        partial_translated[column_name] = translated_reviews
        return partial_translated
    translated[column_name] = translated_reviews
    return translated 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("column_name", nargs="?", default="description")
    args = parser.parse_args()

    filename = args.filename
    column_name = args.column_name
    reviews = pd.read_csv(filename)
    translated = translate_reviews(reviews, column_name)

    translated.to_csv(f"{filename[:-4]}_translated.csv", index=False)

if __name__ == "__main__":
    main()
