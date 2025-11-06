from flask import Flask, request, jsonify, send_from_directory
import json
import os
import time

app = Flask(__name__, static_folder='../src', static_url_path='')

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/products.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    PRODUCTS = json.load(f)

# Basic keyword matching
@app.route('/search')
def search():
    q = request.args.get('q', '')
    start = time.time()
    if not isinstance(q, str) or q.strip() == '':
        return jsonify({ 'results': [], 'query': q, 'time_ms': int((time.time()-start)*1000) })
    tokens = [t.lower() for t in q.split() if t.strip()]
    results = []
    for p in PRODUCTS:
        text = (p['name'] + ' ' + p.get('description', '')).lower()
        score = 0
        for t in tokens:
            if t in text:
                score += 1
        if score > 0:
            results.append({'id': p['id'], 'name': p['name'], 'score': float(score)})
    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'results': results, 'query': q, 'time_ms': int((time.time()-start)*1000)})

@app.route('/')
def index():
    return send_from_directory('../src', 'index.html')

if __name__ == '__main__':
    app.run(port=5000)
