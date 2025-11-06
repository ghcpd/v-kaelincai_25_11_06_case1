#!/bin/bash
set -e
# Run Project A tests
pushd "$(dirname "$0")" >/dev/null
# Create and activate venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Start server in background
python server/app.py &
PID=$!
sleep 2
# Run tests
python -m pip install requests
python tests/test_pre_feature.py
# Stop server
kill $PID || true
popd >/dev/null
