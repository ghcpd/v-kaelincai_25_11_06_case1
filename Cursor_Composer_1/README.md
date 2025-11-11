# Search Feature Enhancement Evaluation

This repository contains two complete Python projects demonstrating the enhancement of a basic search feature with intelligent recommendations and search suggestions.

## Project Overview

### Project A - Pre-Feature (Basic Search)
A basic search implementation that supports only simple keyword matching without any intelligence or suggestions. This represents the original, limited search functionality.

**Features:**
- Simple keyword matching (case-insensitive)
- Basic result filtering
- No recommendations or suggestions

### Project B - Post-Feature (Enhanced Search)
An enhanced search implementation that intelligently recommends related products and provides search suggestions. This demonstrates the improved search functionality.

**Features:**
- Fuzzy matching for typo tolerance
- Relevance scoring for intelligent ranking
- Search suggestions for better UX
- Related product recommendations
- Multi-keyword matching with weighted scoring

## Project Structure

```
.
├── Project_A_PreFeature_Search/
│   ├── src/
│   │   ├── search_engine.py      # Basic search implementation
│   │   └── server.py              # HTTP server for Project A
│   ├── data/
│   │   └── products.json         # Product catalog
│   ├── tests/
│   │   └── test_pre_feature.py   # Test suite for Project A
│   ├── results/                  # Test results (generated)
│   ├── logs/                     # Execution logs (generated)
│   ├── requirements.txt          # Python dependencies
│   ├── setup.sh                  # Setup script
│   └── run_tests.sh              # Test execution script
│
├── Project_B_PostFeature_Search/
│   ├── src/
│   │   ├── search_engine.py      # Enhanced search implementation
│   │   └── server.py             # HTTP server for Project B
│   ├── data/
│   │   └── products.json         # Product catalog
│   ├── tests/
│   │   └── test_post_feature.py  # Test suite for Project B
│   ├── results/                  # Test results (generated)
│   ├── logs/                     # Execution logs (generated)
│   ├── requirements.txt          # Python dependencies
│   ├── setup.sh                  # Setup script
│   └── run_tests.sh              # Test execution script
│
├── test_data.json                # Canonical test cases
├── generate_comparison_report.py # Report generation script
├── run_all.sh                    # Master test execution script
├── compare_report.md             # Comparison report (generated)
└── README.md                     # This file
```

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- bash (for shell scripts; on Windows, use Git Bash or WSL)

### Setup and Run All Tests

1. **Run the master script** (executes both projects and generates comparison):
   ```bash
   bash run_all.sh
   ```

   This will:
   - Set up both projects
   - Run all test cases
   - Generate comparison report

### Individual Project Setup

#### Project A Setup
```bash
cd Project_A_PreFeature_Search
bash setup.sh
source venv/bin/activate  # On Windows: venv\Scripts\activate
bash run_tests.sh
```

#### Project B Setup
```bash
cd Project_B_PostFeature_Search
bash setup.sh
source venv/bin/activate  # On Windows: venv\Scripts\activate
bash run_tests.sh
```

### Manual Setup (Alternative)

If the shell scripts don't work on your system:

1. **Create virtual environments:**
   ```bash
   cd Project_A_PreFeature_Search
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   cd ../Project_B_PostFeature_Search
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run tests:**
   ```bash
   # Project A
   cd Project_A_PreFeature_Search
   python tests/test_pre_feature.py
   
   # Project B
   cd Project_B_PostFeature_Search
   python tests/test_post_feature.py
   ```

3. **Generate comparison report:**
   ```bash
   python generate_comparison_report.py
   ```

## Test Data

The `test_data.json` file contains 15 comprehensive test cases covering:

- **Normal cases:** Valid keyword searches
- **Edge cases:** Complex queries, typos, ambiguous terms
- **Invalid cases:** Empty queries, non-string inputs
- **Complex cases:** Multi-criteria searches, brand searches

Each test case includes:
- Test ID and description
- Input query
- Expected results (min/max counts, required product IDs)
- Pass/fail criteria

## Understanding the Results

### Test Output Format

Each project generates a JSON results file with:
- Total test count
- Passed/failed counts
- Success rate percentage
- Average response time
- Individual test results with:
  - Query executed
  - Result count
  - Response time
  - Pass/fail status
  - Failure reasons (if any)

### Comparison Report

The `compare_report.md` file provides:
- Executive summary
- Overall metrics comparison
- Feature comparison table
- Detailed test-by-test results
- Performance analysis
- Accuracy improvements
- Limitations and recommendations

## Key Improvements in Project B

1. **Fuzzy Matching:** Handles typos and partial matches (e.g., "hedphones" → "headphones")
2. **Relevance Scoring:** Results ranked by relevance, not just keyword presence
3. **Search Suggestions:** Provides query suggestions for better user experience
4. **Related Products:** Recommends similar products based on category, brand, and tags
5. **Intelligent Ranking:** Multi-factor scoring considers name matches, descriptions, categories, brands, and tags

## API Usage

### Project A - Basic Search

```python
from search_engine import BasicSearchEngine

engine = BasicSearchEngine('data/products.json')
result = engine.search('headphones')
print(result)
```

### Project B - Enhanced Search

```python
from search_engine import EnhancedSearchEngine

engine = EnhancedSearchEngine('data/products.json')
result = engine.search('headphones')
print(result)
# Includes: results, suggestions, related_products, relevance_scores
```

### HTTP Server

Start the servers:
```bash
# Project A (port 5000)
cd Project_A_PreFeature_Search
python src/server.py

# Project B (port 5001)
cd Project_B_PostFeature_Search
python src/server.py
```

Query examples:
```bash
# GET request
curl "http://localhost:5000/search?q=headphones"

# POST request
curl -X POST http://localhost:5001/search \
  -H "Content-Type: application/json" \
  -d '{"query": "wireless mouse"}'
```

## Evaluation Metrics

The test suite evaluates:
- **Correctness:** Both implementations return expected results
- **Relevance:** Project B provides more relevant, better-ranked results
- **Response Time:** Performance comparison between implementations
- **Edge Case Handling:** Malformed queries, invalid inputs, large datasets
- **Feature Completeness:** Enhanced features work as expected

## Limitations

1. **Dataset Size:** Optimized for small to medium catalogs (< 10,000 products)
2. **Language:** Currently optimized for English queries
3. **Performance:** Enhanced features add computational overhead
4. **Relevance Tuning:** Scoring weights may need domain-specific adjustment

## Recommendations for Production

1. **Caching:** Implement query result caching for frequent searches
2. **Indexing:** Use dedicated search engines (Elasticsearch, Solr) for large-scale deployment
3. **Machine Learning:** Add ML-based ranking for personalized results
4. **User Feedback:** Implement feedback mechanism to improve relevance
5. **A/B Testing:** Test different relevance weight configurations

## Troubleshooting

### Common Issues

1. **Import errors:** Make sure virtual environment is activated and dependencies are installed
2. **File not found:** Ensure you're running scripts from the correct directory
3. **Permission errors:** On Linux/Mac, make scripts executable: `chmod +x *.sh`
4. **Python version:** Requires Python 3.7+

### Windows-Specific Notes

- Use `python` instead of `python3` if `python3` is not available
- Use Git Bash or WSL for shell scripts, or run Python scripts directly
- Virtual environment activation: `venv\Scripts\activate` (not `venv/bin/activate`)

## License

This project is provided for evaluation purposes.

## Contact

For questions or issues, please refer to the test logs in each project's `logs/` directory.

