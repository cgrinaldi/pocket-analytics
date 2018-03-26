#!/usr/bin/python

import requests
import pandas as pd

from config import POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN
from storage import (
    get_most_recent_since,
    record_data_pull_time,
    save_articles
)


def get_articles(since=None, count=None):
    """Pull latest articles from Pocket API:
    https://getpocket.com/developer/docs/v3/retrieve
    """
    data = {
        'consumer_key': POCKET_CONSUMER_KEY,
        'access_token': POCKET_ACCESS_TOKEN,
        'state': 'all',
        'contentType': 'article',
        'detailType': 'simple',
        'sort': 'newest',
        'since': since,
        'count': count
    }
    resp = (
        requests
        .get('https://getpocket.com/v3/get', params=data)
        .json()
    )
    # save time articles were pulled
    since = resp['since']
    record_data_pull_time(since)

    # pull out articles
    articles = resp['list']
    result = pd.DataFrame([articles[id] for id in articles])

    # only munge if actual articles present
    if len(result) != 0:
        result['url'] = (
            result['resolved_url'].combine_first(result['given_url'])
        )
        for time_col in ['time_added', 'time_updated', 'time_read']:
            result[time_col] = pd.to_datetime(result[time_col], unit='s')
            result.loc[result[time_col] == '1970-01-01', time_col] = pd.NaT
        return (
            result
            .drop_duplicates(subset=['resolved_id'])
            [['item_id', 'resolved_id', 'given_title', 'url', 'resolved_title',
              'time_added', 'time_read', 'time_updated', 'status',
              'word_count']])


def save_latest_articles():
    latest_since = get_most_recent_since()
    latest_articles = get_articles(since=latest_since)
    save_articles(latest_articles)


if __name__ == '__main__':
    save_latest_articles()
