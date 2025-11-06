#!/bin/bash
set -e
# Run Project A
pushd Project_A_PreFeature_Search >/dev/null
bash run_tests.sh
popd >/dev/null

# Run Project B
pushd Project_B_PostFeature_Search >/dev/null
bash run_tests.sh
popd >/dev/null

# Compare results
python compare_results.py
