@echo off
REM Setup script for Project A - Basic Search
echo Setting up Project A - Basic Search Implementation
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To run tests, use: run_tests.bat
echo To start the server, use: python server/app.py
