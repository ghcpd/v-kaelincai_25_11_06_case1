import requests
import json
import time
import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(BASE, 'data', 'test_data.json')
RESULTS_PATH = os.path.join(BASE, 'results', 'results_post.json')
LOG_PATH = os.path.join(BASE, 'logs', 'log_post.txt')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    cases = json.load(f)

results = []

for case in cases:
    test_id = case['test_id']
    q = case['query']
    start = time.time()
    try:
        if isinstance(q, str):
            res = requests.get(f'http://127.0.0.1:5001/search', params={'q': q}, timeout=5)
            latency_ms = int((time.time()-start)*1000)
            data = res.json()
            returned_ids = [r['id'] for r in data.get('results', [])]
            # Post-feature acceptance: expected in top 3
            expected = case.get('expected', [])
            ok = any(e in returned_ids[:3] for e in expected) if expected else (returned_ids == [])
            # Also test suggestions for non-empty queries
            suggestions = []
            if isinstance(q, str) and q.strip():
                s = requests.get(f'http://127.0.0.1:5001/suggest', params={'q': q[:3]}, timeout=5)
                suggestions = s.json().get('suggestions', [])
            results.append({'test_id': test_id, 'query': q, 'latency_ms': latency_ms, 'returned_ids': returned_ids, 'expected': expected, 'pass': ok, 'suggestions': suggestions})
        else:
            res = requests.get(f'http://127.0.0.1:5001/search', params={'q': q}, timeout=5)
            latency_ms = int((time.time()-start)*1000)
            data = res.json()
            returned_ids = [r['id'] for r in data.get('results', [])]
            ok = returned_ids == []
            results.append({'test_id': test_id, 'query': q, 'latency_ms': latency_ms, 'returned_ids': returned_ids, 'expected': [], 'pass': ok})
    except Exception as e:
        results.append({'test_id': test_id, 'query': q, 'latency_ms': None, 'returned_ids': [], 'expected': case.get('expected', []), 'pass': False, 'error': str(e)})

# Save results
os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

# Write logs
with open(LOG_PATH, 'w', encoding='utf-8') as f:
    for r in results:
        f.write(json.dumps(r) + '\n')

# Print summary
passed = sum(1 for r in results if r['pass'])
print(f'Post-feature tests: {passed}/{len(results)} passed')

