#!/usr/bin/env bash

# Only run 3.14 benchmarks

#docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-312 ./run_single.sh pbs-312
#docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-313 ./run_single.sh pbs-313
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-pbs-314 ./run_single.sh pbs-314

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-conda-forge conda run --prefix /bench_env --live-stream ./run_single.sh conda-forge

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-python ./run_single.sh python-docker

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-fedora ./run_single.sh fedora
#docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-rocky ./run_single.sh rocky

#docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-debian ./run_single.sh debian
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-debian-forky ./run_single.sh debian-forky
#docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-ubuntu ./run_single.sh ubuntu
docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-ubuntu-lts ./run_single.sh ubuntu-lts
