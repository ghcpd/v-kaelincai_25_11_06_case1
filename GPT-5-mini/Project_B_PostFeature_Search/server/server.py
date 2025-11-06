from flask import Flask, request, jsonify
import json
from src.search_enhanced import EnhancedSearch
import time

app = Flask(__name__)

with open('data/items.json','r',encoding='utf-8') as f:
    ITEMS = json.load(f)

ENGINE = EnhancedSearch(ITEMS)

@app.route('/search')
def search():
    q = request.args.get('q','')
    start = time.time()
    try:
        results = ENGINE.search(q)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    duration = time.time()-start
    return jsonify({'query': q, 't': duration, 'results': results})

@app.route('/suggest')
def suggest():
    p = request.args.get('p','')
    return jsonify({'prefix': p, 'suggestions': ENGINE.suggest(p)})

@app.route('/recommend')
def recommend():
    item_id = request.args.get('id','')
    return jsonify({'id': item_id, 'recs': ENGINE.recommend_related(item_id)})

if __name__ == '__main__':
    app.run(port=8002)
