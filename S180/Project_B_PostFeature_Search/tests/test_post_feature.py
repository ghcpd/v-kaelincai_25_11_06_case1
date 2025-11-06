import requests
import time

BASE='http://127.0.0.1:8001/search'

TESTS=[
    {'id':'B1','q':'red t-shirt','expect_ids':[1]},
    {'id':'B2','q':'wirless mouse','expect_ids':[3]},
    {'id':'B3','q':'gaming','expect_ids':[4]},
    {'id':'B4','q':'mug','expect_ids':[5]},
]

if __name__=='__main__':
    results=[]
    for t in TESTS:
        start=time.time()
        r=requests.get(BASE, params={'q':t['q']})
        latency=time.time()-start
        data=r.json()
        ids=[res['product']['id'] for res in data['results']]
        ok = any(pid in ids for pid in t['expect_ids'])
        results.append({'id':t['id'],'q':t['q'],'ok':ok,'latency':latency,'ids':ids,'suggestions':data.get('suggestions',[]),'recommendations':[p['id'] for p in data.get('recommendations',[])]})
    print(results)
