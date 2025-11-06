#!/usr/bin/env bash
# Run both projects and aggregate
cd Project_A_PreFeature_Search
bash run_tests.sh
cd ..
cd Project_B_PostFeature_Search
bash run_tests.sh
cd ..
# Aggregate basic results into results/
mkdir -p results
cp Project_A_PreFeature_Search/results/results_pre.json results/results_pre.json || true
cp Project_B_PostFeature_Search/results/results_post.json results/results_post.json || true
python aggregate_results.py | tee results/aggregation.txt
