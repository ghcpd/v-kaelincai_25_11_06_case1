from flask import Flask, request, jsonify, send_from_directory
import json
import os
import time
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__, static_folder='../src', static_url_path='')

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/products.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    PRODUCTS = json.load(f)

# Build TF-IDF index on start
corpus = [p['name'] + ' ' + p.get('description', '') for p in PRODUCTS]
vectorizer = TfidfVectorizer().fit(corpus)
idf_matrix = vectorizer.transform(corpus)

def compute_scores(query):
    """
    Combine TF-IDF cosine similarity and fuzzy matching scores.
    """
    q_vec = vectorizer.transform([query])
    cos_sim = linear_kernel(q_vec, idf_matrix).flatten()
    scores = []
    for i, p in enumerate(PRODUCTS):
        fuzzy = fuzz.token_set_ratio(query, p['name'])/100.0
        combined = 0.6*cos_sim[i] + 0.4*fuzzy
        scores.append({'id': p['id'], 'name': p['name'], 'score': float(combined)})
    scores = [s for s in scores if s['score'] > 0]
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores

@app.route('/search')
def search():
    q = request.args.get('q', '')
    start = time.time()
    if not isinstance(q, str) or q.strip() == '':
        return jsonify({ 'results': [], 'query': q, 'time_ms': int((time.time()-start)*1000) })
    scores = compute_scores(q)
    # Add recommendations: for top result, find products with shared tags or category
    recommendations = []
    if scores:
        top_id = scores[0]['id']
        top_product = next((p for p in PRODUCTS if p['id'] == top_id), None)
        if top_product:
            def related_score(p):
                # tag overlap
                overlap = len(set(top_product.get('tags', [])) & set(p.get('tags', [])))
                same_cat = 1 if top_product.get('category') == p.get('category') else 0
                return overlap + same_cat*0.5
            related = [(p, related_score(p)) for p in PRODUCTS if p['id'] != top_id]
            related = [r for r in related if r[1] > 0]
            related.sort(key=lambda x: x[1], reverse=True)
            recommendations = [{'id': r[0]['id'], 'name': r[0]['name'], 'score': r[1]} for r in related[:3]]
    latency_ms = int((time.time()-start)*1000)
    return jsonify({'results': scores, 'recommendations': recommendations, 'query': q, 'time_ms': latency_ms})

@app.route('/suggest')
def suggest():
    q = request.args.get('q', '')
    # Suggest product name completions and common terms
    if not isinstance(q, str) or len(q.strip()) < 1:
        return jsonify({'suggestions': []})
    ql = q.lower()
    suggestions = []
    for p in PRODUCTS:
        name_low = p['name'].lower()
        if name_low.startswith(ql):
            suggestions.append({'id': p['id'], 'name': p['name']})
        elif ql in name_low:
            # include partial but not prefix
            suggestions.append({'id': p['id'], 'name': p['name']})
    # Limit and unique
    seen = set()
    out = []
    for s in suggestions:
        if s['id'] not in seen:
            seen.add(s['id'])
            out.append(s)
        if len(out) >= 5:
            break
    return jsonify({'suggestions': out})

@app.route('/')
def index():
    return send_from_directory('../src', 'index.html')

if __name__ == '__main__':
    app.run(port=5001)
