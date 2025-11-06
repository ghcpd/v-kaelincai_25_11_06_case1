# Search Feature Comparison Report

This report compares the Pre-Feature (Project A) and Post-Feature (Project B) search implementations.

## Evaluation Metrics
- Accuracy: percentage of tests where expected results are present in top results.
- Relevance: measured by relevance score (Project B includes numeric scores).
- Latency: response time per query.

## High-level findings
- Project A: Basic keyword substring matching. Good for exact phrases, fails with typos or semantic relatedness.
- Project B: Uses fuzzy matching, token overlap, and suggestions to produce better results and add recommendations.

## How to interpret the generated outputs
- `s_shared_artifacts/results/compare_summary.json` contains a map of test ids to pre/post results.
- `Project_A_PreFeature_Search/results/results_pre.json` and `Project_B_PostFeature_Search/results/results_post.json` contain per-test results and timings.

## Acceptance Criteria
Project B is considered an improvement if:
- It matches at least as many test cases as Project A (by success count).
- It includes recommendations for relevant top results.
- It shows improved accuracy on typo and complex queries (tc3, tc4).

## Limitations
- Dataset is small and synthetic — results may vary with larger/real datasets.
- Suggestions are based on prefix matching; more sophisticated auto-complete could use trie or ML models.
- Scoring uses heuristics; real systems may use TF-IDF, BM25, or learning-to-rank models.

## Next steps & Recommendations
- Add indexing for faster search on large datasets (e.g., Elasticsearch, Whoosh).
- Collect user feedback to train ranking models.
- Add A/B testing and evaluation on production traffic.

