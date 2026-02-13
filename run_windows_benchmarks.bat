@echo on

REM Run all Windows benchmarks
REM Requires
REM uv : update before running with uv self update
REM conda : Install miniforge3 to default location or adjust line below
REM Python.org : Download/run Windows x86-64 installed from python.org/downloads

REM location of miniforge install
set "CONDA=C:\Users\%username%\miniforge3\condabin\conda.bat"

rmdir /s /q local_envs

REM Create environments
mkdir local_envs

REM pbs  
uv venv local_envs\pbs_env --python 3.14 --managed-python
REM conda-forge
call "%CONDA%" create --prefix local_envs\cforge_env python=3.14 pip --channel conda-forge --yes
REM Python.org
py -m venv local_envs\org_env

REM Run benchmarks

call local_envs\pbs_env\Scripts\activate.bat
call run_single.bat win-pbs
call local_envs\pbs_env\Scripts\deactivate.bat

call "%CONDA%" run --prefix local_envs\cforge_env --live-stream run_single.bat win-conda-forge

call local_envs\org_env\Scripts\activate
call run_single.bat win-python-org
call local_envs\org_env\Scripts\deactivate.bat