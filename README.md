# text2rec
## Описание проекта
Проект **text2rec** представляет собой сервис рекомендаций фильмов по текстовому запросу пользователя. Запрос может быть как в свободной форме (например: "экшн с неожиданной концовкой"), так и более конкретный с использованием ключевых слов.
## Структура проекта
С функциональной точки зрения **text2rec** опирается на **два** сценария работы:

1. В запросе присутствуют ключевые слова. Реализация поиска по ключевым словам находится в директории **first_case**.
2. В запросе отсутствуют ключевые слова, запрос в свободной форме. В таком случае происходит векторизация запроса и осуществляется поиск наиболее похожих векторов фильмов. Реализация в директории **second_case**.

```
📦 text2rec
├─ src
│  ├─ first_case                <- Поиск по ключевым словам (regex + FuzzyWuzzy)
│  │  ├─ keywords_search.py
│  │  └─ simple_search.py
│  └─ second_case               <- Поиск с использованием DNN (bert, sentence-bert, etc.)
├─ data                         <- Данные фильмов и запросов пользователей для валидации
│  ├─ merging.py
│  ├─ text_queries_yandex.csv
│  ├─ test_queries.csv
│  └─ top250.csv
├─ demos                        <- Демо-версии графического интерфейса
│  └─ demo_text2rec.ipynb
├─ .gitignore
├─ README.md
└─ requirements.txt
```
## Установка зависимостей
Перед использованием или развертыванием сервиса необходимо установить зависимости проекта. Для этого в командной строке введите следующую команду:
```
pip install -r requirements.txt
```
## Лицензия
[MIT](https://choosealicense.com/licenses/mit/)
## Пример работы бейзлайна (BERT)
Ниже приведен пример работы модели BERT, которая обучалась обнаруживать соответствия между ключевыми словами и описанием фильма.
![image](https://user-images.githubusercontent.com/56130198/199210072-516ab705-9694-4502-ad99-f0a3e3b311b2.png)

