from flask import Flask, request, jsonify
import json
from difflib import SequenceMatcher

app = Flask(__name__)

with open('..\\data\\products.json') as f:
    PRODUCTS = json.load(f)

# simple fuzzy ratio
def fuzzy_score(a,b):
    return int(SequenceMatcher(None,a,b).ratio()*100)

# generate search suggestions from product names
def suggestions(prefix):
    prefix = prefix.lower()
    s = set()
    for p in PRODUCTS:
        if p['name'].lower().startswith(prefix):
            s.add(p['name'])
    return sorted(list(s))[:5]

# recommend related products by category
def recommend(product_ids):
    cats = set()
    for pid in product_ids:
        for p in PRODUCTS:
            if p['id']==pid:
                cats.add(p['category'])
    recs=[]
    for p in PRODUCTS:
        if p['category'] in cats and p['id'] not in product_ids:
            recs.append(p)
    return recs[:5]

@app.route('/search')
def search():
    q = request.args.get('q','')
    if not isinstance(q, str):
        return jsonify({'error':'query must be string'}),400
    q = q.strip().lower()
    if q=='':
        return jsonify({'results':[],'suggestions':[],'recommendations':[]})
    tokens = q.split()
    results=[]
    for p in PRODUCTS:
        text = (p['name'] + ' ' + p['description']).lower()
        # relevance: fuzzy on name + token matches
        name_score = max(fuzzy_score(q, p['name'].lower()),0)
        token_score = sum(5 for t in tokens if t in text)
        score = name_score + token_score
        if score>20:
            results.append({'product':p,'score':score})
    results.sort(key=lambda r: r['score'], reverse=True)
    matched_ids=[r['product']['id'] for r in results]
    return jsonify({
        'results':results,
        'suggestions':suggestions(q),
        'recommendations':recommend(matched_ids),
        'query':q
    })

if __name__=='__main__':
    app.run(port=8001)
