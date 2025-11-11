"""
Simple HTTP server for Project B - Enhanced Search
"""

from flask import Flask, request, jsonify
from search_engine import EnhancedSearchEngine
import os

app = Flask(__name__)

# Initialize search engine
products_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
search_engine = EnhancedSearchEngine(products_file)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search endpoint."""
    if request.method == 'GET':
        query = request.args.get('q', '')
    else:
        data = request.get_json() or {}
        query = data.get('query', '')
    
    result = search_engine.search(query)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok', 
        'total_products': len(search_engine.products),
        'features': ['fuzzy_matching', 'relevance_scoring', 'recommendations', 'suggestions']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)

