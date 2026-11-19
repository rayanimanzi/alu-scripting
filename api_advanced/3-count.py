#!/usr/bin/python3
"""Module that recursively counts keywords in the titles of hot posts."""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of the given keywords in hot post titles."""
    if counts is None:
        counts = {}
        for word in word_list:
            counts[word.lower()] = 0
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting.api_advanced:v1.0"}
    params = {"limit": 100}
    if after:
        params["after"] = after
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
    except Exception:
        return
    if response.status_code != 200:
        return
    data = response.json().get("data", {})
    for post in data.get("children", []):
        title = post.get("data", {}).get("title", "")
        for token in title.lower().split():
            if token in counts:
                counts[token] += 1
    after = data.get("after")
    if after is not None:
        return count_words(subreddit, word_list, after, counts)
    totals = {}
    for word in word_list:
        key = word.lower()
        totals[key] = totals.get(key, 0) + counts.get(key, 0)
    for word, total in sorted(totals.items(),
                              key=lambda item: (-item[1], item[0])):
        if total > 0:
            print("{}: {}".format(word, total))
