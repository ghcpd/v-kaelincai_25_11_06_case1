from flask import Flask, request, jsonify
import json
from src.search_simple import SearchEngine
import time

app = Flask(__name__)

with open('data/items.json','r',encoding='utf-8') as f:
    ITEMS = json.load(f)

ENGINE = SearchEngine(ITEMS)

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

if __name__ == '__main__':
    app.run(port=8001)
