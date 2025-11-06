"""
Project B: Enhanced Search Implementation
- Intelligent keyword matching with relevance scoring
- Fuzzy matching for typos and misspellings
- Related product recommendations based on tags and categories
- Auto-completion and search suggestions
- Advanced ranking algorithm
"""
import json
from typing import List, Dict, Any, Tuple
import time
from difflib import SequenceMatcher
from collections import Counter


class EnhancedSearchEngine:
    """
    Enhanced search engine with intelligent features:
    - Relevance scoring
    - Fuzzy matching
    - Related product recommendations
    - Search suggestions
    """

    def __init__(self, data_file: str):
        """
        Initialize the enhanced search engine.
        
        Args:
            data_file: Path to JSON file containing product data
        """
        self.products = []
        self.product_index = {}  # For quick lookup
        self.tag_index = {}  # Index for tags to products
        self.category_index = {}  # Index for categories
        self.load_products(data_file)
        self.search_history = []
        self._build_indices()

    def load_products(self, data_file: str) -> None:
        """Load products from JSON file."""
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                self.products = data.get('products', [])
                for product in self.products:
                    self.product_index[product['id']] = product
        except FileNotFoundError:
            print(f"Error: Data file '{data_file}' not found.")
            self.products = []

    def _build_indices(self) -> None:
        """Build indices for fast lookups."""
        for product in self.products:
            # Build tag index
            for tag in product.get('tags', []):
                if tag not in self.tag_index:
                    self.tag_index[tag] = []
                self.tag_index[tag].append(product['id'])
            
            # Build category index
            category = product.get('category', '')
            if category not in self.category_index:
                self.category_index[category] = []
            self.category_index[category].append(product['id'])

    def _fuzzy_match(self, query: str, text: str, threshold: float = 0.6) -> Tuple[bool, float]:
        """
        Perform fuzzy matching using sequence matching.
        
        Args:
            query: Search query
            text: Text to match against
            threshold: Matching threshold (0-1)
            
        Returns:
            Tuple of (matched: bool, similarity_score: float)
        """
        similarity = SequenceMatcher(None, query.lower(), text.lower()).ratio()
        return similarity >= threshold, similarity

    def _calculate_relevance_score(self, query: str, product: Dict) -> float:
        """
        Calculate relevance score for a product given a query.
        Uses multiple factors:
        - Exact name match (highest weight)
        - Tag matches
        - Description matches
        - Fuzzy matching for typos
        
        Args:
            query: Search query
            product: Product dictionary
            
        Returns:
            Relevance score (0-100)
        """
        score = 0.0
        query_lower = query.lower().strip()
        query_words = query_lower.split()
        
        product_name = product.get('name', '').lower()
        product_desc = product.get('description', '').lower()
        product_tags = [tag.lower() for tag in product.get('tags', [])]
        
        # Exact name match (30 points)
        if query_lower == product_name:
            score += 30
        elif query_lower in product_name:
            score += 25
        
        # Word matches in name (15 points per match)
        for word in query_words:
            if word in product_name:
                score += 15
        
        # Tag matches (10 points per match)
        for word in query_words:
            if word in product_tags:
                score += 10
        
        # Description matches (5 points per match)
        for word in query_words:
            if word in product_desc:
                score += 5
        
        # Fuzzy matching (up to 20 points)
        matched, similarity = self._fuzzy_match(query_lower, product_name, 0.7)
        if matched:
            score += similarity * 20
        
        # Fuzzy match on tags
        for tag in product_tags:
            matched, similarity = self._fuzzy_match(query_lower, tag, 0.6)
            if matched:
                score += similarity * 10
                break  # Count only best tag match
        
        # Normalize to 0-100
        return min(score, 100)

    def search(self, query: str) -> Dict[str, Any]:
        """
        Perform enhanced search with relevance scoring.
        
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
                'suggestions': self.get_suggestions(''),
                'total_results': 0,
                'response_time_ms': (time.time() - start_time) * 1000,
                'method': 'enhanced_search'
            }
        
        results = []
        
        # Search with relevance scoring
        for product in self.products:
            relevance_score = self._calculate_relevance_score(query_lower, product)
            
            # Include products with score > 0 (basic match or fuzzy match)
            if relevance_score > 0:
                # Get related products
                related = self.get_related_products(product['id'])
                
                results.append({
                    'id': product['id'],
                    'name': product['name'],
                    'category': product['category'],
                    'price': product['price'],
                    'description': product['description'],
                    'relevance_score': round(relevance_score, 2),
                    'match_type': 'enhanced_match',
                    'related_products': [{'id': r['id'], 'name': r['name']} for r in related[:3]]
                })
        
        # Sort by relevance score (highest first)
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
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
            'suggestions': self.get_suggestions(query),
            'total_results': len(results),
            'response_time_ms': response_time,
            'method': 'enhanced_search'
        }

    def get_suggestions(self, partial_query: str) -> List[str]:
        """
        Get search suggestions based on partial query.
        Returns product names and tags that match the partial query.
        
        Args:
            partial_query: Partial search query
            
        Returns:
            List of suggestion strings
        """
        if not partial_query or len(partial_query) < 2:
            return []
        
        partial_lower = partial_query.lower().strip()
        suggestions = set()
        
        # Suggestions from product names
        for product in self.products:
            name_lower = product['name'].lower()
            if partial_lower in name_lower:
                # Extract the word containing the partial query
                words = product['name'].split()
                for word in words:
                    if partial_lower in word.lower():
                        suggestions.add(product['name'])
                        break
        
        # Suggestions from tags
        for tag in self.tag_index.keys():
            if partial_lower in tag.lower():
                suggestions.add(tag)
        
        # Suggestions from categories
        for category in self.category_index.keys():
            if partial_lower in category.lower():
                suggestions.add(category)
        
        return sorted(list(suggestions))[:10]  # Return top 10 suggestions

    def get_related_products(self, product_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Get related products based on:
        - Shared tags
        - Same category
        - Similar product characteristics
        
        Args:
            product_id: Product ID to find related products for
            limit: Maximum number of related products to return
            
        Returns:
            List of related product dictionaries
        """
        if product_id not in self.product_index:
            return []
        
        source_product = self.product_index[product_id]
        source_tags = set(source_product.get('tags', []))
        source_category = source_product.get('category', '')
        
        related = []
        
        # Calculate similarity with other products
        for other_product in self.products:
            if other_product['id'] == product_id:
                continue
            
            other_tags = set(other_product.get('tags', []))
            other_category = other_product.get('category', '')
            
            # Calculate similarity score
            score = 0
            
            # Tag overlap (40% weight)
            tag_overlap = len(source_tags & other_tags)
            score += tag_overlap * 15
            
            # Category match (30% weight)
            if source_category == other_category:
                score += 30
            
            # Price proximity (20% weight)
            price_diff = abs(source_product['price'] - other_product['price'])
            if price_diff < 50:
                score += (50 - price_diff)
            
            if score > 0:
                related.append({
                    'product': other_product,
                    'score': score
                })
        
        # Sort by score and return top N
        related.sort(key=lambda x: x['score'], reverse=True)
        return [item['product'] for item in related[:limit]]

    def get_search_history(self) -> List[Dict[str, Any]]:
        """Get search history."""
        return self.search_history

    def clear_history(self) -> None:
        """Clear search history."""
        self.search_history = []

    def batch_search(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Perform batch search for multiple queries.
        
        Args:
            queries: List of search queries
            
        Returns:
            List of search results
        """
        results = []
        for query in queries:
            result = self.search(query)
            results.append(result)
        return results
