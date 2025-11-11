#!/bin/bash

# Test execution script for Project A - Pre-Feature Search

echo "Running tests for Project A - Pre-Feature Search..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Create directories if they don't exist
mkdir -p results
mkdir -p logs

# Run tests and capture output
echo "Executing test suite..."
python tests/test_pre_feature.py > logs/log_pre.txt 2>&1
TEST_EXIT_CODE=$?

# Display log output
echo ""
echo "Test execution log:"
cat logs/log_pre.txt

# Check if tests passed
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✓ All tests passed!"
else
    echo ""
    echo "✗ Some tests failed. Check logs/log_pre.txt for details."
fi

exit $TEST_EXIT_CODE

