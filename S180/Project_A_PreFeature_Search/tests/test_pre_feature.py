import requests
import time

BASE='http://127.0.0.1:8000/search'

TESTS=[
    {'id':'A1', 'q':'red t-shirt', 'expect_ids':[1]},
    {'id':'A2', 'q':'wireless mouse', 'expect_ids':[3]},
    {'id':'A3', 'q':'jeans', 'expect_ids':[2]},
    {'id':'A4', 'q':'', 'expect_ids':[]},
]

if __name__=='__main__':
    results=[]
    for t in TESTS:
        start=time.time()
        r=requests.get(BASE, params={'q':t['q']})
        latency=time.time()-start
        data=r.json()
        ids=[res['product']['id'] for res in data['results']]
        ok = ids==t['expect_ids']
        results.append({'id':t['id'],'q':t['q'],'ok':ok,'latency':latency,'ids':ids})
    print(results)
