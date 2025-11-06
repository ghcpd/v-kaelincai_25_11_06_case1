@echo off
set LOGFILE=logs\log_post.txt
set RESULTFILE=results\results_post.json
if not exist logs mkdir logs
if not exist results mkdir results

echo Starting Project B server...
start /B cmd /C "python server\server.py > %LOGFILE% 2>&1"
timeout /t 1 >nul

echo Running pytest...
.venv\Scripts\pytest.exe -q > %LOGFILE% 2>&1

echo Collecting results (simple probe)
python - <<PY
import requests, json
try:
    r = requests.get('http://127.0.0.1:8002/search', params={'q':'shirt'}, timeout=2).json()
except Exception as e:
    r = {'error': str(e)}
with open(r'%RESULTFILE%','w',encoding='utf-8') as f:
    json.dump(r,f,indent=2)
print('Wrote', r'%RESULTFILE%')
PY

echo Done. See %LOGFILE% and %RESULTFILE%
