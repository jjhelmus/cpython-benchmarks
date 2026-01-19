#!/usr/bin/env bash

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-312 ./run_single.sh pbs-312
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-313 ./run_single.sh pbs-313
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-314 ./run_single.sh pbs-314

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-fedora ./run_single.sh fedora
