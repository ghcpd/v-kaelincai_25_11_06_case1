from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    PRODUCTS = json.load(f)

# Basic keyword matching: case-insensitive substring match in name or description
@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not isinstance(query, str):
        return jsonify({'error': 'query must be a string', 'results': []}), 400
    q = query.strip().lower()
    if q == '':
        return jsonify({'results': []})

    results = []
    for p in PRODUCTS:
        if q in p['name'].lower() or q in p['description'].lower() or q in ' '.join(p.get('tags', [])).lower():
            results.append({'id': p['id'], 'name': p['name'], 'score': 1.0})

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(port=5001)
