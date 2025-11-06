"""
Basic keyword search implementation for Project A.
This module exposes a SearchEngine class that does simple keyword matching.
"""
from typing import List, Dict

class SearchEngine:
    def __init__(self, items: List[Dict]):
        # items: list of dict with keys: id, name, description, tags
        self.items = items

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        q = query.strip().lower()
        if q == "":
            return []

        results = []
        for item in self.items:
            text = " ".join([str(item.get('name','')), str(item.get('description','')), " ".join(item.get('tags',[]))]).lower()
            if q in text:
                results.append({"item": item, "score": 1.0})

        # no ranking beyond binary match
        return results[:max_results]
