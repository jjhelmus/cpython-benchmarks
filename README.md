## Bechmarking various CPython Builds


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