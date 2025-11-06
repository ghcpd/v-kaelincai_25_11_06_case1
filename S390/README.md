# Evaluation of S180, S390, S430-v2, Claude Haiku 4.5, and GPT-5-mini - Enhanced Search Experiment

This repo contains two projects that implement a simple product search: a pre-feature basic keyword search (Project A) and a post-feature enhanced search (Project B) with relevance scoring, fuzzy matching, suggestions, and related product recommendations.

See `run_all.sh` to run the full experiment and generate a comparison report.

Project directories:
- Project_A_PreFeature_Search
- Project_B_PostFeature_Search

Shared artifacts:
- `test_data.json` - Canonical structured test cases
- `compare_results.py` - Aggregates and generates `compare_report.md`
- `run_all.sh` - Master script to run everything

Requirements:
- Linux, macOS, or Windows (WSL/Git Bash recommended for running bash scripts).
- Python 3.10+

Usage Steps:
1. Run all tests and generate comparison (Linux/macOS or WSL):
   - bash run_all.sh
2. Or run each project individually:
   - cd Project_A_PreFeature_Search; bash run_tests.sh
   - cd Project_B_PostFeature_Search; bash run_tests.sh

Expected Input/Output Formats:
- Input: queries are strings (type: str). Test cases are defined in `test_data.json` as JSON objects with keys: `test_id`, `query`, `expected`, `description`.
- Output: Each project returns JSON via `/search` endpoint: {"results": [{"id":"p1", "name":"...", "score": 0.85}], "recommendations": [...], "query": "...", "time_ms": 23}

Acceptance Criteria:
- Project B must return improved relevance (expected IDs appear in top 3 or improved score ranking) and better tolerance for typos.
- Tests verify correctness and performance; Post-feature should show better pass rate and equal or lower average latency.

Limitations and notes:
- This is a toy system with in-memory datasets and is for evaluation purposes.
- Project B uses TF-IDF and RapidFuzz to improve relevance and handle typos.
- Dataset is small; results may vary on large datasets.

