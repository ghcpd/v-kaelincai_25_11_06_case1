#!/usr/bin/env bash
python server/run_server.py &
SERVER_PID=$!
sleep 1
python -u tests/test_post_feature.py | tee results/results_post.json
kill $SERVER_PID || true
