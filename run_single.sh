#!/usr/bin/env bash
# Run a single set of pyperformance benchmarks
# Requires 'python' to be the interpreter that will be benchmarked
# cwd must be writable

if [ "$#" -ne  1 ]; then
    echo "Usage: $0 <identifier>"
    exit 1
fi

RUN_ARGS="--rigorous --warmups 2"
# the next line is useful for testing, it runs quick
#RUN_ARGS="--fast --benchmarks python_startup"


WORK_DIR=$(mktemp -d -p .)
pushd ${WORK_DIR}

# create the venv with pyperformance
python -m venv bench_env
source bench_env/bin/activate
python -m pip install pyperformance

# run benchmarks
pyperformance run ${RUN_ARGS} --output results.json | tee bench.log
python -c "import sys; print(sys.version)" >> bench.log

# copy results and log
result_dir=../results/${1}
mkdir -p ${result_dir}
cp results.json ${result_dir}/results-$(date "+%Y-%m-%dT%H%M%S").json
cp bench.log ${result_dir}/log-$(date "+%Y-%m-%dT%H%M%S").txt

popd
rm -rf ${WORK_DIR}