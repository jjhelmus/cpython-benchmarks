# Bechmarking various CPython Builds

## Running benchmarks

### Linux

Setup:
```
./build_containers.sh
```

Run benchmarks:
```
./run_linux_benchmarks.sh
```

Results are stored in the `results` directory with subdirectories for each build.

### macOS

Run benchmarks (does setup):
```
./run_macos_benchmarks.sh
```

This will run the pyperformance benchmark suite for
* python-build-standalone
* conda-forge
* Python.org
* Homebrew

Results are stored in the `results` directory with subdirectories for each build.


## Examining results

`pyperf` can be used to examine and compare the results. This can be run using
`uvx pyperf`. There are various sub-commands and options.

One way to compare results is with the `compare_to` command, for example:

```
uvx pyperf compare_to --table --group-by-speed results/macos-homebrew/results-2026-01-19T155537.json results/macos-pbs/results-2026-01-19T123436.json
```

