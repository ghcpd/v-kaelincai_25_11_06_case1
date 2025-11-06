@echo off
echo Running setup and tests for Project A and Project B

echo === Project A setup ===
pushd Project_A_PreFeature_Search
call setup.sh
call run_tests.sh
popd

echo === Project B setup ===
pushd Project_B_PostFeature_Search
call setup.sh
call run_tests.sh
popd

echo === Aggregating results ===
if not exist results mkdir results
copy Project_A_PreFeature_Search\results\results_pre.json results\results_pre.json >nul
copy Project_B_PostFeature_Search\results\results_post.json results\results_post.json >nul

python - <<PY
import json, sys
try:
    a = json.load(open('results/results_pre.json'))
except:
    a = {'error':'missing'}
try:
    b = json.load(open('results/results_post.json'))
except:
    b = {'error':'missing'}
report = {
  'project_a_probe': a,
  'project_b_probe': b
}
open('compare_report.md','w',encoding='utf-8').write('# Compare Report\n\n' + json.dumps(report,indent=2))
print('Wrote compare_report.md')
PY

echo Done. See compare_report.md and results/
