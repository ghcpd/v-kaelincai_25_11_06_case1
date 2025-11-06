import json
import time
import os
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server.server_post import app

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEST_DATA = os.path.join(ROOT, 'test_data.json')
RESULT_FILE = os.path.join(ROOT, 'Project_B_PostFeature_Search', 'results', 'results_post.json')
LOG_FILE = os.path.join(ROOT, 'Project_B_PostFeature_Search', 'logs', 'log_post.txt')


def run_tests():
    with open(TEST_DATA, 'r', encoding='utf-8') as f:
        tests = json.load(f)

    client = app.test_client()
    reports = []
    start_all = time.time()
    for tc in tests:
        tc_start = time.time()
        q = tc['query']
        try:
            if not isinstance(q, str):
                res = client.get(f'/search?query=')
            else:
                res = client.get(f'/search?query={q}')
        except Exception as e:
            res = None

        elapsed = time.time() - tc_start
        ids = []
        ok = False
        if res is not None and res.status_code == 200:
            body = res.get_json()
            ids = [r['id'] for r in body.get('results', [])]
            expected = tc.get('expected_post_ids', [])
            # We accept if expected subset is present at top
            ok = all(e in ids[:len(expected)+1] for e in expected)

        reports.append({'id': tc['id'], 'query': q, 'ids': ids, 'expected': tc.get('expected_post_ids', []), 'success': ok, 'time': elapsed})

    total_time = time.time() - start_all
    with open(RESULT_FILE, 'w', encoding='utf-8') as rf:
        json.dump(reports, rf, indent=2)
    with open(LOG_FILE, 'w', encoding='utf-8') as lf:
        lf.write(f'Total test time: {total_time}\n')
        lf.write(json.dumps(reports, indent=2))

    successes = len([r for r in reports if r['success']])
    print(f'Project B: {successes}/{len(reports)} tests passed')

if __name__ == '__main__':
    run_tests()