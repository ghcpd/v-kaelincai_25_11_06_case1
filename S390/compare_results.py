import json
import os

PRE_PATH = os.path.join('Project_A_PreFeature_Search', 'results', 'results_pre.json')
POST_PATH = os.path.join('Project_B_PostFeature_Search', 'results', 'results_post.json')
OUT_MD = 'compare_report.md'
OUT_JSON = os.path.join('results', 'aggregated.json')

with open(PRE_PATH, 'r', encoding='utf-8') as f:
    pre = json.load(f)
with open(POST_PATH, 'r', encoding='utf-8') as f:
    post = json.load(f)

# Align by test_id
pre_map = {r['test_id']: r for r in pre}
post_map = {r['test_id']: r for r in post}

report = []
metrics = {'pre': {'passed':0, 'total':len(pre), 'avg_latency':0}, 'post': {'passed':0, 'total':len(post), 'avg_latency':0}}

for tid in sorted(set(pre_map.keys()) | set(post_map.keys())):
    p = pre_map.get(tid)
    q = post_map.get(tid)
    pre_pass = p['pass'] if p else None
    post_pass = q['pass'] if q else None
    pre_latency = p.get('latency_ms') if p else None
    post_latency = q.get('latency_ms') if q else None
    report.append({'test_id': tid, 'pre_pass': pre_pass, 'post_pass': post_pass, 'pre_latency': pre_latency, 'post_latency': post_latency})
    if pre_pass:
        metrics['pre']['passed'] += 1
    if post_pass:
        metrics['post']['passed'] += 1
    if pre_latency:
        metrics['pre'].setdefault('latencies', []).append(pre_latency)
    if post_latency:
        metrics['post'].setdefault('latencies', []).append(post_latency)

for k in ('pre','post'):
    lats = metrics[k].get('latencies', [])
    metrics[k]['avg_latency'] = sum(lats)/len(lats) if lats else None

# Write md
with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write('# Compare Report\n\n')
    f.write('Summary of pre-feature (Project A) vs post-feature (Project B) tests.\n\n')
    f.write('## Metrics\n')
    f.write('- Pre: {}/{} passed. Avg latency: {} ms\n'.format(metrics['pre']['passed'], metrics['pre']['total'], metrics['pre']['avg_latency']))
    f.write('- Post: {}/{} passed. Avg latency: {} ms\n\n'.format(metrics['post']['passed'], metrics['post']['total'], metrics['post']['avg_latency']))
    f.write('## Test results comparison\n')
    for r in report:
        f.write('- {}: pre_pass={}, post_pass={}, pre_latency={}, post_latency={}\n'.format(r['test_id'], r['pre_pass'], r['post_pass'], r['pre_latency'], r['post_latency']))

# Save aggregated JSON
out = {'metrics': metrics, 'report': report}
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)

print('Comparison report written to', OUT_MD)
