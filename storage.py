import pandas as pd


def record_data_pull_time(timestamp):
    with open('data/since.txt', 'a+') as f:
        f.write('{}\n'.format(timestamp))


def read_times_api_queried():
    try:
        with open('data/since.txt', 'r+') as f:
            sinces = f.readlines()
            return [s.split('\n')[0] for s in sinces]
    except FileNotFoundError:
        return []


def get_most_recent_since():
    sinces = read_times_api_queried()
    if len(sinces) == 0:
        return None
    return sinces[-1]


def save_articles(articles_new):
    try:
        articles_prev = pd.read_csv('data/articles.csv')
        articles = pd.concat([articles_prev, articles_new])
        articles_deduped = articles.drop_duplicates(subset=['resolved_id'])
        articles_deduped.to_csv('data/articles.csv', index=False)
    except FileNotFoundError:
        articles_new.to_csv('data/articles.csv', index=False)
