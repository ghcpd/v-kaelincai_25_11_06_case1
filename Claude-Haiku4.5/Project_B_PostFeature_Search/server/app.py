"""
Project B: Enhanced Server
Flask server for enhanced search functionality with recommendations
"""
from flask import Flask, request, jsonify
from search_engine import EnhancedSearchEngine
import os
import json
from datetime import datetime

app = Flask(__name__)

# Initialize search engine
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_file = os.path.join(parent_dir, 'data', 'products.json')

engine = EnhancedSearchEngine(data_file)


@app.route('/', methods=['GET'])
def home():
    """Serve home page"""
    return jsonify({
        'message': 'Project B - Enhanced Search Engine',
        'version': '2.0',
        'features': [
            'Intelligent relevance scoring',
            'Fuzzy matching for typos',
            'Related product recommendations',
            'Auto-completion suggestions'
        ],
        'endpoints': [
            '/api/search?q=query',
            '/api/suggestions?q=partial_query',
            '/api/related?product_id=P001',
            '/api/history',
            '/health'
        ]
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'products_loaded': len(engine.products),
        'search_method': 'enhanced'
    })


@app.route('/api/search', methods=['GET'])
def search():
    """Enhanced search endpoint"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'error': 'Query parameter "q" is required',
            'example': '/api/search?q=headphones'
        }), 400
    
    result = engine.search(query)
    return jsonify(result)


@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    """Get search suggestions"""
    partial_query = request.args.get('q', '').strip()
    suggestions = engine.get_suggestions(partial_query)
    return jsonify({
        'partial_query': partial_query,
        'suggestions': suggestions,
        'count': len(suggestions)
    })


@app.route('/api/related', methods=['GET'])
def related_products():
    """Get related products"""
    product_id = request.args.get('product_id', '').strip()
    
    if not product_id:
        return jsonify({
            'error': 'Parameter "product_id" is required',
            'example': '/api/related?product_id=P001'
        }), 400
    
    related = engine.get_related_products(product_id)
    return jsonify({
        'product_id': product_id,
        'related_products': related,
        'count': len(related)
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get search history"""
    history = engine.get_search_history()
    return jsonify({
        'history': history,
        'total_searches': len(history)
    })


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear search history"""
    engine.clear_history()
    return jsonify({'message': 'History cleared'})


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5001)
