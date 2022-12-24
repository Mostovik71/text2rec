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
    service_urls = ['translate.google.com', 'translate.google.ru']
    translator = Translator(service_urls=service_urls, raise_exception=True)
    translated = reviews.copy(deep=True)
    reviews_text = reviews[column_name]
    try:
        for i, text_ru in enumerate(tqdm(reviews_text)):
            with Timer() as timer:
                try:
                    text_en = translator.translate(text_ru[:5000], src="ru", dest="en").text
                except KeyboardInterrupt:
                    raise
                except:
                    # traceback.print_exc()
                    time.sleep(60)
                    translator = Translator(service_urls=service_urls, raise_exception=True)
                    text_en = translator.translate(text_ru[:5000], src="ru", dest="en").text
                translated_reviews.append(text_en)
            time.sleep(max(0.5 - timer.elapsed, 0))
    except:
        pass
    if i + 1 != len(reviews_text):
        partial_translated = translated.iloc[:i].copy(deep=True)
        partial_translated[column_name] = translated_reviews
        return partial_translated
    translated[column_name] = translated_reviews
    return translated 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-c", "--column_name", nargs="?", default="description")
    parser.add_argument("-s", "--start_index", nargs="?", default=0)
    parser.add_argument("-e", "--end_index", nargs="?", default=-1)
    args = parser.parse_args()

    filename = args.filename
    df = pd.read_csv(filename)
    column_name = args.column_name
    start_index = int(args.start_index)
    end_index = int(args.end_index)
    end_index = len(df) if end_index == -1 else end_index
    reviews = df.iloc[start_index:end_index].copy(deep=True)
    
    print(f"Starting translating reviews from {start_index} to {end_index}")
    translated = translate_reviews(reviews, column_name)
    translated.to_csv(f"{filename[:-4]}_translated_{start_index}_{start_index+len(translated)}.csv", index=False)

if __name__ == "__main__":
    main()
