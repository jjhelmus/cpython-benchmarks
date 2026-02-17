#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "matplotlib>=3.10.8",
#     "numpy>=2.4.2",
#     "pyperf>=2.10.0",
# ]
# ///

# Create a violin plot of Python benchmarks
# Adapted from https://github.com/faster-cpython/bench_runner
# BSD 3-Clause License

import json
from operator import itemgetter
from pathlib import Path
from argparse import ArgumentParser

import numpy as np
import pyperf
from matplotlib import pyplot as plt

CombinedData = list[tuple[str, np.ndarray | None, float]]

INTERPRETER_HEAVY = {
    "chaos",
    "coroutines",
    "deepcopy",
    "deltablue",
    "generators",
    "go",
    "hexiom",
    "logging",
    "nbody",
    "pickle_pure_python",
    "pprint",
    "raytrace",
    "richards",
    "richards_super",
    "sqlglot_parse",
    "tomli_loads",
    "unpack_sequence",
    "unpickle_pure_python",
}


def get_timing_data(filename, excluded=tuple[str]) -> dict[str, np.ndarray]:
    contents = json.loads(Path(filename).read_text())
    data = {}

    for benchmark in contents["benchmarks"]:
        name = benchmark.get("metadata", contents["metadata"])["name"]
        if name not in excluded:
            row = []
            for run in benchmark["runs"]:
                row.extend(run.get("values", []))
            data[name] = np.array(row, dtype=np.float64)

    return data


def get_combined_data(
    ref_data: dict[str, np.ndarray],
    head_data: dict[str, np.ndarray],
    excluded: tuple[str],
) -> CombinedData:
    def remove_outliers(values, m=2):
        return values[abs(values - np.mean(values)) < np.multiply(m, np.std(values))]

    def calculate_diffs(ref_values, head_values) -> tuple[np.ndarray | None, float]:
        if len(ref_values) > 3 and len(head_values) > 3:
            sig, t_score = pyperf._utils.is_significant(ref_values, head_values)
            if not sig:
                return None, 0.0
            else:
                ref_values = remove_outliers(ref_values)
                head_values = remove_outliers(head_values)
        values = np.outer(ref_values, 1.0 / head_values).flatten()
        values.sort()
        return values, float(values.mean())

    combined_data = []
    for name, ref in ref_data.items():
        if len(ref) != 0 and name in head_data and name not in excluded:
            head = head_data[name]
            if len(ref) == len(head):
                combined_data.append((name, *calculate_diffs(ref, head)))
    combined_data.sort(key=itemgetter(2))
    return combined_data


def formatter(val, pos):
    return f"{val:.02f}×"


def plot_diff_pair(ax, data):
    if not len(data):
        return []

    all_data = []
    violins = []
    colors = []

    for i, (name, values, _mean) in enumerate(data):
        if values is not None:
            idx = np.round(np.linspace(0, len(values) - 1, 100)).astype(int)
            violins.append(values[idx])
            all_data.extend(values)
            if name in INTERPRETER_HEAVY:
                colors.append("red")
            else:
                colors.append("C0")
        else:
            violins.append([1.0])
            all_data.extend([1.0])
            colors.append("C0")
            ax.text(1.01, i + 1, "insignificant")

    violins.append(all_data)

    violin = ax.violinplot(
        violins,
        vert=False,
        showmeans=True,
        showmedians=False,
        widths=1.0,
        quantiles=[[0.1, 0.9]] * len(violins),
    )

    violin["cquantiles"].set_linestyle(":")
    for body, color in zip(violin["bodies"], colors):
        body.set_facecolor(color)

    for i, values in enumerate(violins):
        if not np.all(values == [1.0]):
            mean = np.mean(values)
            ax.text(mean, i + 1.3, f"{mean:.04f}", size=8)

    return all_data


def plot_diff(
    combined_data: CombinedData,
    output_filename: str,
    title: str,
    differences: tuple[str, str],
) -> None:
    _, axs = plt.subplots(
        figsize=(8, 2 + len(combined_data) * 0.3), layout="constrained"
    )
    plt.axvline(1.0)
    plot_diff_pair(axs, combined_data)
    names = [x[0] for x in combined_data]
    names.append("ALL")
    axs.set_yticks(np.arange(len(names)) + 1, names)
    axs.set_ylim(0, len(names) + 1)
    axs.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    axs.xaxis.set_major_formatter(formatter)
    xlim = axs.get_xlim()
    if xlim[0] > 0.75 and xlim[1] < 1.25:
        axs.set_xlim(0.75, 1.25)
    axs.annotate(
        f"{differences[1]} ⟶",
        xy=(1.0, 1.0),
        xycoords=("data", "axes fraction"),
        xytext=(10, 0),
        textcoords="offset pixels",
    )
    axs.annotate(
        f"⟵ {differences[0]}",
        xy=(1.0, 1.0),
        xycoords=("data", "axes fraction"),
        xytext=(-10, 0),
        textcoords="offset pixels",
        horizontalalignment="right",
    )
    axs.grid()
    axs.set_title(title)

    plt.savefig(output_filename)


def main():
    parser = ArgumentParser("plot_benchmarks")
    parser.add_argument("ref", type=str, help="Reference benchmarks")
    parser.add_argument("head", type=str, help="Experiment(head) benchmarks")
    parser.add_argument(
        "--title", type=str, default="Benchmark Comparison", help="Title of plot"
    )
    parser.add_argument(
        "--output", type=str, default="output.svg", help="Output filename"
    )
    parser.add_argument(
        "--excluded",
        type=str,
        default="",
        help="Comma seperated list of excluded benchmarks",
    )

    args = parser.parse_args()
    excluded = args.excluded.split(",")
    ref_data = get_timing_data(args.ref, excluded)
    head_data = get_timing_data(args.head, excluded)
    combined_data = get_combined_data(ref_data, head_data, excluded)
    plot_diff(
        combined_data,
        args.output,
        args.title,
        ("slower", "faster"),
    )


if __name__ == "__main__":
    main()
