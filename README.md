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

Use `./run_linux_aarch64_benchmarks.sh` for a limited set of aarch64 targets.

Custom benchmarks for compression and sqlite can be run with

```
./run_linux_custom_benchmarks.sh
```

Results are stored in the `results` directory with subdirectories for each build.

### macOS

Run benchmarks (does setup):
```
./run_macos_benchmarks.sh
```

Custom benchmarks for compression and sqlite can be run with

```
./run_macos_custom_benchmarks.sh
```

This will run the pyperformance benchmark suite for
* python-build-standalone
* conda-forge
* Python.org
* Homebrew

Results are stored in the `results` directory with subdirectories for each build.


### Windows

Run benchmarks (does setup)

```
call run_windows_benchmarks.bat
```

Or custom:

```
call run_windows_custome_benchmarks.bat
```

## Examining results

`pyperf` can be used to examine and compare the results. This can be run using
`uvx pyperf`. There are various sub-commands and options.

One way to compare results is with the `compare_to` command, for example:

```
uvx pyperf compare_to --table --group-by-speed results/macos-homebrew/results-2026-01-19T155537.json results/macos-pbs/results-2026-01-19T123436.json
```

A plot comparing two results can be generated using

```
./plot_benchmark_comparison.py <ref.json> <head.json>
```

The `plot_pbs_314_comparison.py` script was used to create `pbs-314-comparison.png` which compares the performance of the
Python 3.14.6 in the [20260623 release](https://github.com/astral-sh/python-build-standalone/releases#release-20260623),
of python-build-standalone against alternative CPython distribution. The raw
data from used in this figure is included in this repository.
