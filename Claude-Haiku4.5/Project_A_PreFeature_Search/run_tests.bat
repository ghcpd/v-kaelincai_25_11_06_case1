@echo off
REM Test execution script for Project A
echo Running Project A Tests - Basic Search Implementation
echo.

cd /d "%~dp0"

echo Installing dependencies if needed...
pip install -r requirements.txt >nul 2>&1

echo.
echo Starting test execution...
python tests/test_pre_feature.py

if errorlevel 1 (
    echo.
    echo Tests completed with errors!
    exit /b 1
) else (
    echo.
    echo Tests completed successfully!
)
