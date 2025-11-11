@echo off
REM Master script to run all tests and generate comparison report (Windows)

echo ==========================================
echo Running Complete Test Suite
echo ==========================================
echo.

REM Create results directory
if not exist "results" mkdir results

REM Track overall success
set OVERALL_SUCCESS=0

REM Run Project A tests
echo ----------------------------------------
echo Running Project A - Pre-Feature Tests
echo ----------------------------------------
cd Project_A_PreFeature_Search
if exist "run_tests.bat" (
    call run_tests.bat
    set PROJECT_A_EXIT=%ERRORLEVEL%
) else (
    echo Error: run_tests.bat not found in Project A
    set PROJECT_A_EXIT=1
)
cd ..

if not %PROJECT_A_EXIT% EQU 0 (
    set OVERALL_SUCCESS=1
)

echo.
echo ----------------------------------------
echo Running Project B - Post-Feature Tests
echo ----------------------------------------
cd Project_B_PostFeature_Search
if exist "run_tests.bat" (
    call run_tests.bat
    set PROJECT_B_EXIT=%ERRORLEVEL%
) else (
    echo Error: run_tests.bat not found in Project B
    set PROJECT_B_EXIT=1
)
cd ..

if not %PROJECT_B_EXIT% EQU 0 (
    set OVERALL_SUCCESS=1
)

echo.
echo ----------------------------------------
echo Generating Comparison Report
echo ----------------------------------------

REM Generate comparison report
python generate_comparison_report.py

echo.
echo ==========================================
echo Test Suite Complete
echo ==========================================
echo.
echo Results saved in:
echo   - Project_A_PreFeature_Search\results\results_pre.json
echo   - Project_B_PostFeature_Search\results\results_post.json
echo   - compare_report.md
echo.

if %OVERALL_SUCCESS% EQU 0 (
    echo All tests completed successfully!
) else (
    echo Some tests failed. Check individual project logs for details.
)

exit /b %OVERALL_SUCCESS%

