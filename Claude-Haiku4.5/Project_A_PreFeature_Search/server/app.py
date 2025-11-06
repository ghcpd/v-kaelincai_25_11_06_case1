"""
Project A: Basic Server
Simple Flask server for basic search functionality
"""
from flask import Flask, request, jsonify
from search_engine import BasicSearchEngine
import os
import json
from datetime import datetime

app = Flask(__name__)

# Initialize search engine
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_file = os.path.join(parent_dir, 'data', 'products.json')

engine = BasicSearchEngine(data_file)


@app.route('/', methods=['GET'])
def home():
    """Serve home page"""
    return jsonify({
        'message': 'Project A - Basic Search Engine',
        'version': '1.0',
        'endpoints': [
            '/api/search?q=query',
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
        'products_loaded': len(engine.products)
    })


@app.route('/api/search', methods=['GET'])
def search():
    """Search endpoint"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'error': 'Query parameter "q" is required',
            'example': '/api/search?q=headphones'
        }), 400
    
    result = engine.search(query)
    return jsonify(result)


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
    app.run(debug=False, host='127.0.0.1', port=5000)
