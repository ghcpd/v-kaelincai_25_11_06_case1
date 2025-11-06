@echo off
echo Setting up Project B virtual environment and installing dependencies
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
echo Setup complete
