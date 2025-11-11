@echo off
REM Test execution script for Project B - Post-Feature Enhanced Search (Windows)

echo Running tests for Project B - Post-Feature Enhanced Search...

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Create directories if they don't exist
if not exist "results" mkdir results
if not exist "logs" mkdir logs

REM Run tests and capture output
echo Executing test suite...
python tests\test_post_feature.py > logs\log_post.txt 2>&1
set TEST_EXIT_CODE=%ERRORLEVEL%

REM Display log output
echo.
echo Test execution log:
type logs\log_post.txt

REM Check if tests passed
if %TEST_EXIT_CODE% EQU 0 (
    echo.
    echo All tests passed!
) else (
    echo.
    echo Some tests failed. Check logs\log_post.txt for details.
)

exit /b %TEST_EXIT_CODE%

