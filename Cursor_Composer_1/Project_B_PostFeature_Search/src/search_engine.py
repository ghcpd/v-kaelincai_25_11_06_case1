"""
Enhanced Search Engine - Post-Feature Implementation
Supports fuzzy matching, relevance scoring, and intelligent product recommendations.
"""

import json
import re
from typing import List, Dict, Any, Tuple
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict


class EnhancedSearchEngine:
    """Enhanced search engine with intelligent matching and recommendations."""
    
    def __init__(self, products_file: str = None):
        """
        Initialize the enhanced search engine with a product catalog.
        
        Args:
            products_file: Path to JSON file containing products
        """
        self.products = []
        self.product_index = {}  # For fast lookups
        self.category_index = defaultdict(list)  # Category-based index
        self.brand_index = defaultdict(list)  # Brand-based index
        if products_file:
            self.load_products(products_file)
            self._build_indexes()
    
    def load_products(self, file_path: str):
        """Load products from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
        except FileNotFoundError:
            self.products = []
        except json.JSONDecodeError:
            self.products = []
    
    def _build_indexes(self):
        """Build indexes for faster searching."""
        self.product_index = {p.get('id'): p for p in self.products}
        self.category_index = defaultdict(list)
        self.brand_index = defaultdict(list)
        
        for product in self.products:
            category = product.get('category', '').lower()
            brand = product.get('brand', '').lower()
            self.category_index[category].append(product)
            self.brand_index[brand].append(product)
    
    def _fuzzy_match_score(self, text1: str, text2: str) -> float:
        """
        Calculate fuzzy matching score between two strings.
        
        Args:
            text1: First string
            text2: Second string
            
        Returns:
            Similarity score between 0 and 1
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _calculate_relevance_score(self, product: Dict[str, Any], query: str, 
                                   query_keywords: List[str]) -> float:
        """
        Calculate relevance score for a product based on query.
        
        Args:
            product: Product dictionary
            query: Original query string
            query_keywords: List of keywords from query
            
        Returns:
            Relevance score (higher is better)
        """
        score = 0.0
        query_lower = query.lower()
        
        name = product.get('name', '').lower()
        description = product.get('description', '').lower()
        category = product.get('category', '').lower()
        brand = product.get('brand', '').lower()
        tags = [t.lower() for t in product.get('tags', [])]
        
        # Exact name match gets highest score
        if query_lower == name:
            score += 100.0
        elif query_lower in name:
            score += 50.0
        
        # Keyword matching with weights
        for keyword in query_keywords:
            # Name matches (highest weight)
            if keyword in name:
                score += 20.0
            # Exact name match bonus
            if name.startswith(keyword) or name.endswith(keyword):
                score += 10.0
            
            # Description matches
            if keyword in description:
                score += 5.0
            
            # Category matches
            if keyword in category:
                score += 8.0
            
            # Brand matches
            if keyword in brand:
                score += 7.0
            
            # Tag matches
            for tag in tags:
                if keyword in tag:
                    score += 6.0
        
        # Fuzzy matching bonus
        name_fuzzy = self._fuzzy_match_score(query, name)
        if name_fuzzy > 0.7:
            score += name_fuzzy * 15.0
        
        # Multi-keyword bonus (more keywords matched = higher score)
        matched_keywords = sum(1 for kw in query_keywords 
                              if kw in name or kw in description or kw in category)
        if matched_keywords > 1:
            score += matched_keywords * 3.0
        
        return score
    
    def _get_related_products(self, product: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Get related products based on category, brand, or tags.
        
        Args:
            product: Reference product
            limit: Maximum number of related products to return
            
        Returns:
            List of related products
        """
        related = []
        product_id = product.get('id')
        category = product.get('category', '').lower()
        brand = product.get('brand', '').lower()
        tags = [t.lower() for t in product.get('tags', [])]
        
        # Find products in same category
        for p in self.category_index.get(category, []):
            if p.get('id') != product_id:
                related.append(p)
        
        # Find products with same brand
        for p in self.brand_index.get(brand, []):
            if p.get('id') != product_id and p not in related:
                related.append(p)
        
        # Find products with similar tags
        for p in self.products:
            if p.get('id') != product_id and p not in related:
                p_tags = [t.lower() for t in p.get('tags', [])]
                common_tags = set(tags) & set(p_tags)
                if common_tags:
                    related.append(p)
        
        return related[:limit]
    
    def _get_search_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """
        Generate search suggestions based on query.
        
        Args:
            query: Search query
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested queries
        """
        suggestions = []
        query_lower = query.lower()
        query_keywords = query_lower.split()
        
        # Collect potential suggestions from product names, categories, brands
        potential_suggestions = []
        
        for product in self.products:
            name = product.get('name', '')
            name_lower = name.lower()
            category = product.get('category', '')
            category_lower = category.lower()
            brand = product.get('brand', '')
            brand_lower = brand.lower()
            
            # If query matches part of name, suggest full name
            if query_lower in name_lower and len(name_lower) > len(query_lower):
                fuzzy_score = self._fuzzy_match_score(query_lower, name_lower)
                potential_suggestions.append((fuzzy_score, name))
            
            # Suggest category if query is similar (fuzzy match)
            category_fuzzy = self._fuzzy_match_score(query_lower, category_lower)
            if category_fuzzy > 0.5:
                potential_suggestions.append((category_fuzzy, category))
            
            # Suggest brand if query is similar (fuzzy match)
            brand_fuzzy = self._fuzzy_match_score(query_lower, brand_lower)
            if brand_fuzzy > 0.5:
                potential_suggestions.append((brand_fuzzy, brand))
            
            # Fuzzy match product names for typos
            name_fuzzy = self._fuzzy_match_score(query_lower, name_lower)
            if name_fuzzy > 0.6 and name_fuzzy < 1.0:  # Similar but not exact
                potential_suggestions.append((name_fuzzy, name))
            
            # Check individual words in product names
            name_words = name_lower.split()
            for word in name_words:
                word_fuzzy = self._fuzzy_match_score(query_lower, word)
                if word_fuzzy > 0.6:
                    potential_suggestions.append((word_fuzzy, name))
        
        # Add common search patterns for single keywords
        if len(query_keywords) == 1:
            keyword = query_keywords[0]
            for product in self.products:
                name = product.get('name', '')
                name_words = name.lower().split()
                if keyword in name_words and len(name_words) > 1:
                    potential_suggestions.append((0.8, name))
        
        # Remove duplicates and sort by relevance
        seen = set()
        unique_suggestions = []
        for score, suggestion in potential_suggestions:
            if suggestion not in seen and suggestion:
                seen.add(suggestion)
                unique_suggestions.append((score, suggestion))
        
        # Sort by score (descending) and take top suggestions
        unique_suggestions.sort(key=lambda x: x[0], reverse=True)
        suggestions = [sug for _, sug in unique_suggestions[:limit]]
        
        # If no suggestions found and query seems like a typo or non-existent term,
        # suggest popular categories or product names
        if not suggestions and len(query_lower) > 2:
            # Suggest popular categories
            categories = set(p.get('category') for p in self.products if p.get('category'))
            suggestions = list(categories)[:limit]
        
        return suggestions
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Perform an enhanced search with relevance scoring and recommendations.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary containing search results, recommendations, and suggestions
        """
        start_time = datetime.now()
        
        # Validate input
        if not isinstance(query, str):
            return {
                'results': [],
                'query': query,
                'total_results': 0,
                'response_time_ms': 0,
                'suggestions': [],
                'error': 'Invalid input: query must be a string'
            }
        
        query = query.strip()
        if not query:
            return {
                'results': [],
                'query': query,
                'total_results': 0,
                'response_time_ms': 0,
                'suggestions': [],
                'error': 'Empty query'
            }
        
        # Tokenize query
        query_keywords = re.findall(r'\b\w+\b', query.lower())
        
        # Score all products
        scored_products = []
        for product in self.products:
            score = self._calculate_relevance_score(product, query, query_keywords)
            if score > 0:  # Only include products with some relevance
                scored_products.append((score, product))
        
        # Sort by relevance score (descending)
        scored_products.sort(key=lambda x: x[0], reverse=True)
        
        # Extract top results (limit to top 20)
        results = [product for _, product in scored_products[:20]]
        
        # Get search suggestions
        suggestions = self._get_search_suggestions(query, limit=5)
        
        # Get related products for top result (if available)
        related_products = []
        if results:
            related_products = self._get_related_products(results[0], limit=3)
        
        # Calculate response time
        end_time = datetime.now()
        response_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            'results': results,
            'query': query,
            'total_results': len(results),
            'response_time_ms': round(response_time_ms, 2),
            'suggestions': suggestions,
            'related_products': related_products,
            'relevance_scores': {p.get('id'): round(score, 2) 
                               for score, p in scored_products[:len(results)]},
            'timestamp': start_time.isoformat()
        }
    
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Get a product by its ID."""
        return self.product_index.get(product_id)

