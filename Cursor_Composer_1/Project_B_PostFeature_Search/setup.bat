@echo off
REM Setup script for Project B - Post-Feature Enhanced Search (Windows)

echo Setting up Project B - Post-Feature Enhanced Search...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist "results" mkdir results
if not exist "logs" mkdir logs
if not exist "data" mkdir data

echo Setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate.bat

