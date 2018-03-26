import os
import pandas as pd


DIR_PATH = os.path.dirname(os.path.abspath(__file__))
SINCE_PATH = os.path.join(DIR_PATH, 'data/since.txt')
ARTICLES_PATH = os.path.join(DIR_PATH, 'data/articles.csv')


def record_data_pull_time(timestamp):
    with open(SINCE_PATH, 'a+') as f:
        f.write('{}\n'.format(timestamp))


def read_times_api_queried():
    try:
        with open(SINCE_PATH, 'r+') as f:
            sinces = f.readlines()
            return [s.split('\n')[0] for s in sinces]
    except:
        return []


def get_most_recent_since():
    sinces = read_times_api_queried()
    if len(sinces) == 0:
        return None
    return sinces[-1]


def save_articles(articles_new):
    try:
        articles_prev = pd.read_csv(ARTICLES_PATH)
        articles = pd.concat([articles_prev, articles_new])
        articles_deduped = articles.drop_duplicates(subset=['resolved_id'])
        articles_deduped.to_csv(ARTICLES_PATH, index=False, encoding='utf8')
    except:
        articles_new.to_csv(ARTICLES_PATH, index=False, encoding='utf8')
