#!/usr/bin/env bash
# Start server in background
python server/run_server.py &
SERVER_PID=$!
sleep 1
python -u tests/test_pre_feature.py | tee results/results_pre.json
kill $SERVER_PID || true
