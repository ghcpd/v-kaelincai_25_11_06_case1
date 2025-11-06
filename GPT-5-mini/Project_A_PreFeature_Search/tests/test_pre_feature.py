import json
import time
import requests
import os

with open(os.path.join(os.path.dirname(__file__),'..','data','items.json')) as f:
    ITEMS = json.load(f)

def call_search(q):
    r = requests.get('http://127.0.0.1:8001/search', params={'q': q}, timeout=5)
    return r.json()

def test_basic_search_running():
    # requires the server to be started separately by run_tests.sh
    res = call_search('red')
    assert 'results' in res
