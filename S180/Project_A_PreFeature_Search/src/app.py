from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load simple product index
with open('..\\data\\products.json') as f:
    PRODUCTS = json.load(f)

# Basic keyword search: token match against name and description
@app.route('/search')
def search():
    q = request.args.get('q','')
    if not isinstance(q, str):
        return jsonify({'error':'query must be string'}),400
    q = q.strip().lower()
    if q == '':
        return jsonify({'results':[],'query':q}),200
    tokens = q.split()
    results = []
    for p in PRODUCTS:
        text = (p['name'] + ' ' + p['description']).lower()
        score = sum(1 for t in tokens if t in text)
        if score>0:
            results.append({'product':p,'score':score})
    # sort by score desc
    results.sort(key=lambda r: r['score'], reverse=True)
    return jsonify({'results':results,'query':q}),200

if __name__=='__main__':
    app.run(port=8000)
