@echo off
REM Master script to run all tests and generate comparison report
echo.
echo ==============================================================
echo EVALUATION: Enhanced Search Feature Implementation
echo Running Project A and Project B Tests
echo ==============================================================
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0

REM Run Project A tests
echo.
echo [1/3] Running Project A - Basic Search Tests...
echo ======================================================
cd /d "%SCRIPT_DIR%Project_A_PreFeature_Search"
call run_tests.bat
if errorlevel 1 (
    echo Error: Project A tests failed
    exit /b 1
)

REM Run Project B tests
echo.
echo [2/3] Running Project B - Enhanced Search Tests...
echo ======================================================
cd /d "%SCRIPT_DIR%Project_B_PostFeature_Search"
call run_tests.bat
if errorlevel 1 (
    echo Error: Project B tests failed
    exit /b 1
)

REM Generate comparison report
echo.
echo [3/3] Generating Comparison Report...
echo ======================================================
cd /d "%SCRIPT_DIR%"
python generate_comparison_report.py

echo.
echo ==============================================================
echo ALL TESTS COMPLETED SUCCESSFULLY
echo ==============================================================
echo.
echo Results available in:
echo - Project_A_PreFeature_Search\results\results_pre.json
echo - Project_B_PostFeature_Search\results\results_post.json
echo - shared_artifacts\compare_report.md
echo.
pause
