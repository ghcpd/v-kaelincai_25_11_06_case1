"""
Basic Search Engine - Pre-Feature Implementation
Supports only simple keyword matching without intelligence or suggestions.
"""

import json
import re
from typing import List, Dict, Any
from datetime import datetime


class BasicSearchEngine:
    """Basic search engine that performs simple keyword matching."""
    
    def __init__(self, products_file: str = None):
        """
        Initialize the search engine with a product catalog.
        
        Args:
            products_file: Path to JSON file containing products
        """
        self.products = []
        if products_file:
            self.load_products(products_file)
    
    def load_products(self, file_path: str):
        """Load products from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
        except FileNotFoundError:
            self.products = []
        except json.JSONDecodeError:
            self.products = []
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Perform a basic keyword search.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary containing search results and metadata
        """
        start_time = datetime.now()
        
        # Validate input
        if not isinstance(query, str):
            return {
                'results': [],
                'query': query,
                'total_results': 0,
                'response_time_ms': 0,
                'error': 'Invalid input: query must be a string'
            }
        
        query = query.strip()
        if not query:
            return {
                'results': [],
                'query': query,
                'total_results': 0,
                'response_time_ms': 0,
                'error': 'Empty query'
            }
        
        # Simple keyword matching (case-insensitive)
        query_lower = query.lower()
        query_keywords = query_lower.split()
        
        results = []
        for product in self.products:
            # Check if any keyword matches in name or description
            name_lower = product.get('name', '').lower()
            description_lower = product.get('description', '').lower()
            category_lower = product.get('category', '').lower()
            
            # Simple keyword matching
            matches = False
            for keyword in query_keywords:
                if (keyword in name_lower or 
                    keyword in description_lower or 
                    keyword in category_lower):
                    matches = True
                    break
            
            if matches:
                results.append(product)
        
        # Calculate response time
        end_time = datetime.now()
        response_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            'results': results,
            'query': query,
            'total_results': len(results),
            'response_time_ms': round(response_time_ms, 2),
            'timestamp': start_time.isoformat()
        }
    
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Get a product by its ID."""
        for product in self.products:
            if product.get('id') == product_id:
                return product
        return None

