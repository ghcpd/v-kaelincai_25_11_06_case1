"""
Enhanced search implementation for Project B.
Features:
- Relevance scoring using token overlap and fuzzy matching (rapidfuzz).
- Autocomplete suggestions from popular terms.
- Related product recommendations based on tag co-occurrence.
"""
from typing import List, Dict, Tuple
from rapidfuzz import fuzz
import heapq

class EnhancedSearch:
    def __init__(self, items: List[Dict]):
        self.items = items
        # build simple vocabulary and suggestions
        self.terms = set()
        for it in items:
            for token in (it.get('name','') + ' ' + it.get('description','')).lower().split():
                self.terms.add(token.strip('.,'))

    def score_item(self, query: str, item: Dict) -> float:
        q = query.lower()
        text = (item.get('name','') + ' ' + item.get('description','') + ' ' + ' '.join(item.get('tags',[]))).lower()
        # fuzzy partial ratio
        fscore = fuzz.ratio(q, text) / 100.0
        # token overlap
        qtokens = set(q.split())
        ttokens = set(text.split())
        overlap = len(qtokens & ttokens) / (len(qtokens) + 1)
        # combine
        return 0.6 * fscore + 0.4 * overlap

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        if not isinstance(query, str):
            raise TypeError('query must be a string')
        q = query.strip()
        if q == '':
            return []

        heap = []
        for item in self.items:
            sc = self.score_item(q, item)
            if sc > 0.05:
                heapq.heappush(heap, (-sc, {"item": item, "score": sc}))

        results = []
        while heap and len(results) < max_results:
            results.append(heapq.heappop(heap)[1])

        return results

    def suggest(self, prefix: str, max_suggestions: int = 5) -> List[str]:
        p = prefix.lower()
        if not p:
            return []
        suggestions = [t for t in self.terms if t.startswith(p)]
        # return sorted by length then alphabetic
        suggestions.sort(key=lambda x: (len(x), x))
        return suggestions[:max_suggestions]

    def recommend_related(self, item_id: str, max_recs: int = 5) -> List[Dict]:
        base = None
        for it in self.items:
            if it.get('id') == item_id:
                base = it
                break
        if base is None:
            return []
        tags = set(base.get('tags',[]))
        scored = []
        for it in self.items:
            if it.get('id') == item_id:
                continue
            score = len(tags & set(it.get('tags',[])))
            if score>0:
                scored.append(( -score, it))
        scored.sort()
        return [it for _,it in scored[:max_recs]]
