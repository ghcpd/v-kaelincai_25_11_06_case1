import requests
import time
import os

BASE = 'http://127.0.0.1:8002'

def call(endpoint, params=None):
    params = params or {}
    t0 = time.time()
    r = requests.get(BASE+endpoint, params=params, timeout=5)
    return time.time()-t0, r.json()

def test_search_returns_results():
    dt, res = call('/search', {'q':'shirt'})
    assert 'results' in res

def test_suggest():
    dt, res = call('/suggest', {'p':'cof'})
    assert 'suggestions' in res

def test_recommend():
    dt, res = call('/recommend', {'id':'p1'})
    assert 'recs' in res
