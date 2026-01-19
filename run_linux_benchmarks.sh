#!/usr/bin/env bash

docker run --rm -v ${PWD}:/io --workdir /io local-benchmarks-fedora ./run_single.sh fedora