# Project B — Post-Feature Enhanced Search

Features:
- Relevance scoring using token overlap and fuzzy matching (rapidfuzz)
- Search suggestions via prefix matching
- Related product recommendations (based on explicit 'related' field)

Setup & run tests:
1. cd Project_B_PostFeature_Search
2. ./setup.sh
3. ./run_tests.sh

Output:
- results/results_post.json
- logs/log_post.txt

Improvements over Project A:
- Handles typos (fuzzy match)
- Provides suggestions and related product recommendations
- Improved relevance ranking
