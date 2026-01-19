#!/usr/bin/env bash

docker build containers/pbs-312 --tag 'local-benchmarks-pbs-312'
docker build containers/pbs-313 --tag 'local-benchmarks-pbs-313'
docker build containers/pbs-314 --tag 'local-benchmarks-pbs-314'

docker build containers/conda-forge --tag 'local-benchmarks-conda-forge'

docker build containers/fedora --tag 'local-benchmarks-fedora'
docker build containers/rocky --tag 'local-benchmarks-rocky'

docker build containers/debian --tag 'local-benchmarks-debian'
docker build containers/ubuntu --tag 'local-benchmarks-ubuntu'
docker build containers/ubuntu --tag 'local-benchmarks-ubuntu-lts'
