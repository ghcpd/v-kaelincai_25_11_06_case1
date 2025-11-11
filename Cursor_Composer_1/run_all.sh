#!/bin/bash

# Master script to run all tests and generate comparison report

echo "=========================================="
echo "Running Complete Test Suite"
echo "=========================================="
echo ""

# Create results directory
mkdir -p results

# Track overall success
OVERALL_SUCCESS=0

# Run Project A tests
echo "----------------------------------------"
echo "Running Project A - Pre-Feature Tests"
echo "----------------------------------------"
cd Project_A_PreFeature_Search
if [ -f "run_tests.sh" ]; then
    bash run_tests.sh
    PROJECT_A_EXIT=$?
else
    echo "Error: run_tests.sh not found in Project A"
    PROJECT_A_EXIT=1
fi
cd ..

if [ $PROJECT_A_EXIT -ne 0 ]; then
    OVERALL_SUCCESS=1
fi

echo ""
echo "----------------------------------------"
echo "Running Project B - Post-Feature Tests"
echo "----------------------------------------"
cd Project_B_PostFeature_Search
if [ -f "run_tests.sh" ]; then
    bash run_tests.sh
    PROJECT_B_EXIT=$?
else
    echo "Error: run_tests.sh not found in Project B"
    PROJECT_B_EXIT=1
fi
cd ..

if [ $PROJECT_B_EXIT -ne 0 ]; then
    OVERALL_SUCCESS=1
fi

echo ""
echo "----------------------------------------"
echo "Generating Comparison Report"
echo "----------------------------------------"

# Generate comparison report
python3 generate_comparison_report.py

echo ""
echo "=========================================="
echo "Test Suite Complete"
echo "=========================================="
echo ""
echo "Results saved in:"
echo "  - Project_A_PreFeature_Search/results/results_pre.json"
echo "  - Project_B_PostFeature_Search/results/results_post.json"
echo "  - compare_report.md"
echo ""

if [ $OVERALL_SUCCESS -eq 0 ]; then
    echo "✓ All tests completed successfully!"
else
    echo "✗ Some tests failed. Check individual project logs for details."
fi

exit $OVERALL_SUCCESS

