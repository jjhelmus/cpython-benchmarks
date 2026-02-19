#!/usr/bin/env bash

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-312 ./run_custom_single.sh pbs-312
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-313 ./run_custom_single.sh pbs-313
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-314 ./run_custom_single.sh pbs-314

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-conda-forge conda run --prefix /bench_env --live-stream ./run_custom_single.sh conda-forge

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-fedora ./run_custom_single.sh fedora
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-rocky ./run_custom_single.sh rocky

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-debian ./run_custom_single.sh debian
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-ubuntu ./run_custom_single.sh ubuntu
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-ubuntu-lts ./run_custom_single.sh ubuntu-lts
