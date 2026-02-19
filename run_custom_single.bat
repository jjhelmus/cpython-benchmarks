@echo off

REM Run a single set of pyperformance benchmarks
REM Requires 'python' to be the interpreter that will be benchmarked
REM cwd must be writable

if "%~1"=="" (
    echo Usage: %~nx0 ^<identifier^>
    exit /b 1
)

set "RUN_ARGS=--rigorous --warmups 2"
REM the next line is useful for testing, it runs quick
REM set "RUN_ARGS=--fast --benchmarks python_startup"

REM Create temporary directory
set "WORK_DIR=temp_%RANDOM%_%RANDOM%"
mkdir "%WORK_DIR%"
pushd "%WORK_DIR%"

REM create the venv with pyperformance
python -m venv bench_env
call bench_env\Scripts\activate.bat
python -m pip install pyperformance

REM run benchmarks
pyperformance run --manifest ..\custom\MANIFEST %RUN_ARGS% --output results.json > bench.log 2>&1
python -c "import sys; print(sys.version)" >> bench.log

REM copy results and log
set "result_dir=..\results\%~1"
if not exist "%result_dir%" mkdir "%result_dir%"

REM Get timestamp in format YYYY-MM-DDTHHMMSS
for /f %%i in ('powershell -c "get-date -format yyyy-MM-dd\THHmmss"') do @set TIMESTAMP=%%i

copy results.json "%result_dir%\custom_results-%TIMESTAMP%.json"
copy bench.log "%result_dir%\custom_log-%TIMESTAMP%.txt"

popd
rmdir /s /q "%WORK_DIR%"