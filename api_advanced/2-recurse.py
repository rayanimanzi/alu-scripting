#!/usr/bin/python3
"""Module that recursively collects the titles of all hot posts."""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Return a list of the titles of all hot posts for a subreddit.

    Returns None if the subreddit is invalid or has no results.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting.api_advanced:v1.0"}
    params = {"limit": 100}
    if after:
        params["after"] = after
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
    except Exception:
        return None
    if response.status_code != 200:
        return None
    data = response.json().get("data", {})
    titles = [post.get("data", {}).get("title")
              for post in data.get("children", [])]
    hot_list = hot_list + titles
    after = data.get("after")
    if after is None:
        return hot_list if len(hot_list) > 0 else None
    return recurse(subreddit, hot_list, after)
