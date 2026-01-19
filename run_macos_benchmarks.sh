#!/usr/bin/env bash
# Run all macOS benchmarks
# Requires
# uv : update before running with "uv self update"
# conda : Install miniforge
# brew : brew install python3 python-tk
# Python.org : Download/run macOS installed from python.org/downloads
set -x

rm -rf local_envs

# Create environments 
mkdir -p local_envs

# pbs
uv venv local_envs/pbs_env --python 3.14 --managed-python
# conda-forge
conda create --prefix ./local_envs/cforge_env python=3.14 pip --channel conda-forge --yes
# Homebrew
/opt/homebrew/bin/python3 -m venv ./local_envs/brew_env
# Python.org
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m venv ./local_envs/org_env


# Run benchmarks
source ./local_envs/pbs_env/bin/activate
./run_single.sh macos-pbs
deactivate

conda run  --prefix ./local_envs/cforge_env --live-stream ./run_single.sh macos-conda-forge

source ./local_envs/brew_env/bin/activate
./run_single.sh macos-homebrew
deactivate

source ./local_envs/org_env/bin/activate
./run_single.sh macos-python-org
deactivate