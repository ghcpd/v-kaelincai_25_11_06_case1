"""
Project A: Basic Search Implementation
- Keyword matching only
- No intelligent recommendations
- No search suggestions
- Simple text-based matching
"""
import json
from typing import List, Dict, Any
import time


class BasicSearchEngine:
    """
    Basic search engine with simple keyword matching.
    This is the pre-feature implementation with limited functionality.
    """

    def __init__(self, data_file: str):
        """
        Initialize the search engine with product data.
        
        Args:
            data_file: Path to JSON file containing product data
        """
        self.products = []
        self.load_products(data_file)
        self.search_history = []

    def load_products(self, data_file: str) -> None:
        """Load products from JSON file."""
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                self.products = data.get('products', [])
        except FileNotFoundError:
            print(f"Error: Data file '{data_file}' not found.")
            self.products = []

    def search(self, query: str) -> Dict[str, Any]:
        """
        Perform basic keyword search.
        Only matches keywords in product name and description.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary containing search results and metadata
        """
        start_time = time.time()
        query_lower = query.lower().strip()
        
        # Empty query handling
        if not query_lower:
            return {
                'query': query,
                'results': [],
                'total_results': 0,
                'response_time_ms': (time.time() - start_time) * 1000,
                'method': 'keyword_matching'
            }
        
        results = []
        query_words = query_lower.split()
        
        # Simple keyword matching in name and description
        for product in self.products:
            product_name = product.get('name', '').lower()
            product_description = product.get('description', '').lower()
            product_tags = [tag.lower() for tag in product.get('tags', [])]
            
            # Check if any query word appears in name, description, or tags
            matched = False
            for word in query_words:
                if (word in product_name or 
                    word in product_description or 
                    word in product_tags):
                    matched = True
                    break
            
            if matched:
                results.append({
                    'id': product['id'],
                    'name': product['name'],
                    'category': product['category'],
                    'price': product['price'],
                    'description': product['description'],
                    'relevance_score': 1.0,  # Basic: all matches have same score
                    'match_type': 'keyword_match'
                })
        
        response_time = (time.time() - start_time) * 1000
        
        # Log search
        self.search_history.append({
            'query': query,
            'results_count': len(results),
            'response_time_ms': response_time
        })
        
        return {
            'query': query,
            'results': results,
            'total_results': len(results),
            'response_time_ms': response_time,
            'method': 'keyword_matching'
        }

    def get_suggestions(self, partial_query: str) -> List[str]:
        """
        Get search suggestions (limited functionality in pre-feature).
        Returns empty list as this is basic implementation.
        
        Args:
            partial_query: Partial search query
            
        Returns:
            Empty list (no suggestions in basic version)
        """
        return []

    def get_related_products(self, product_id: str) -> List[Dict[str, Any]]:
        """
        Get related products (limited functionality in pre-feature).
        Returns empty list as this is basic implementation.
        
        Args:
            product_id: Product ID to find related products for
            
        Returns:
            Empty list (no recommendations in basic version)
        """
        return []

    def get_search_history(self) -> List[Dict[str, Any]]:
        """Get search history."""
        return self.search_history

    def clear_history(self) -> None:
        """Clear search history."""
        self.search_history = []
