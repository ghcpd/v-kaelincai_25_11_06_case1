# Enhanced Search Evaluation

Two projects included: Project_A_PreFeature_Search and Project_B_PostFeature_Search.

1. Setup: run setup.sh in both project folders to create venv and install deps.
2. Run tests: from each folder run run_tests.sh. Or run run_all.sh at repo root to run both and aggregate results.

Project B adds fuzzy matching, search suggestions, and recommendations as improvements.

See compare_report.md for summary.

## Test Scenario & Acceptance Criteria
- Input/Output: All APIs accept query string parameter `q`. Responses are JSON with `results` (array of {product,score}), and optional `suggestions` and `recommendations` in Project B.
- Acceptance: Project B must return improved relevance and suggestions for fuzzy/misspelled queries and provide recommendations related to matched categories.

## How to run
1. In each project folder run `setup.sh` then `bash run_tests.sh`.
2. Or from repo root run `bash run_all.sh` to execute all tests and aggregate.

## Test Data
Canonical test cases are in `test_data.json` at repo root.
