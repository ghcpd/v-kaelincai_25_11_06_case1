from flask import Flask, request, jsonify
import json
import os
from rapidfuzz import fuzz

app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    PRODUCTS = json.load(f)


def tokenize(s):
    return [t for t in s.lower().split() if t]


def score_product(query, p):
    q = query.lower()
    name = p['name'].lower()
    desc = p['description'].lower()
    tags = ' '.join(p.get('tags', [])).lower()

    # Base overlaps
    tokens = tokenize(q)
    overlap = sum(1 for t in tokens if t in name or t in desc or t in tags)
    overlap_score = overlap / max(1, len(tokens))

    # Fuzzy match on name and description
    fuzz_name = fuzz.partial_ratio(q, name)/100.0
    fuzz_desc = fuzz.partial_ratio(q, desc)/100.0

    # Category boost
    cat_boost = 0.1 if q in p['category'] else 0.0

    # Weighted combination
    score = 0.5 * overlap_score + 0.35 * max(fuzz_name, fuzz_desc) + cat_boost
    return round(score, 4)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not isinstance(query, str):
        return jsonify({'error': 'query must be a string', 'results': []}), 400
    q = query.strip()
    if q == '':
        return jsonify({'results': []})

    scored = []
    for p in PRODUCTS:
        s = score_product(q, p)
        if s > 0.0:
            scored.append({'id': p['id'], 'name': p['name'], 'score': s, 'category': p['category'], 'related': p.get('related', [])})

    # sort by decreasing score
    scored.sort(key=lambda x: x['score'], reverse=True)

    # Add related recommendations (top related ids from best match)
    if scored:
        top = scored[0]
        related = []
        for rid in top.get('related', []):
            rp = next((pp for pp in PRODUCTS if pp['id'] == rid), None)
            if rp:
                related.append({'id': rp['id'], 'name': rp['name']})
        scored[0]['recommendations'] = related

    return jsonify({'results': scored})

@app.route('/suggest')
def suggest():
    q = request.args.get('q', '').strip().lower()
    if not q:
        return jsonify({'suggestions': []})
    suggestions = set()
    for p in PRODUCTS:
        if p['name'].lower().startswith(q):
            suggestions.add(p['name'])
        for t in p.get('tags', []):
            if t.lower().startswith(q):
                suggestions.add(t)
    return jsonify({'suggestions': list(suggestions)[:10]})

if __name__ == '__main__':
    app.run(port=5002)
