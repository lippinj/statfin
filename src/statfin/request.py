import requests


class RequestError(Exception):
    def __init__(self, code, text, url):
        self.code = code
        self.text = text
        self.url = url


def get_json(url, *args, **kwargs):
    r = requests.get(url, *args, **kwargs, timeout=60)
    return _as_json(r)


def post_json(url, *args, **kwargs):
    r = requests.post(url, *args, **kwargs, timeout=60)
    return _as_json(r)


def _as_json(r):
    if r.status_code != 200:
        raise RequestError(r.status_code, r.text, r.url)
    return r.json()
