#!/bin/bash
set -e
# Run Project B tests
pushd "$(dirname "$0")" >/dev/null
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Start server
python server/app.py &
PID=$!
sleep 2
python tests/test_post_feature.py
kill $PID || true
popd >/dev/null
