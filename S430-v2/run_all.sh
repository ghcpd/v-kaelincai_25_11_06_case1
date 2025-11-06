#!/usr/bin/env bash
# Run both project tests and aggregate results
set -e

# Run Project A
pushd Project_A_PreFeature_Search
python3 -m pip install -r requirements.txt
python3 tests/test_pre_feature.py
popd

# Run Project B
pushd Project_B_PostFeature_Search
python3 -m pip install -r requirements.txt
python3 tests/test_post_feature.py
popd

# Compare
python3 - <<'PY'
import json
import os
pa = 'Project_A_PreFeature_Search/results/results_pre.json'
pb = 'Project_B_PostFeature_Search/results/results_post.json'
with open(pa) as fa, open(pb) as fb:
    ra = json.load(fa)
    rb = json.load(fb)

# build map by test id
ma = {r['id']: r for r in ra}
mb = {r['id']: r for r in rb}

summary = {}
for tid in ma:
    a = ma[tid]
    b = mb.get(tid)
    summary[tid] = {
        'pre_success': a['success'],
        'post_success': b['success'] if b else None,
        'pre_results': a['ids'],
        'post_results': b['ids'] if b else []
    }

with open('s_shared_artifacts/results/compare_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

# write simple markdown compare
with open('compare_report.md', 'w') as f:
    f.write('# Search Feature Comparison\n\n')
    f.write('Comparison between basic keyword search (Project A) and enhanced search (Project B)\n\n')
    for tid, info in summary.items():
        f.write(f'## {tid}\n')
        f.write(f'- pre_success: {info["pre_success"]}\n')
        f.write(f'- post_success: {info["post_success"]}\n')
        f.write(f'- pre_results: {info["pre_results"]}\n')
        f.write(f'- post_results: {info["post_results"]}\n\n')
print('Comparison report saved to compare_report.md')
PY

# aggregate outputs
cat compare_report.md
