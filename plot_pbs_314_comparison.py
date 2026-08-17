#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.10",
#     "numpy>=2.0",
# ]
# ///

"""Plot Linux, macOS, and Windows pyperformance mean ratios against PBS 3.14.6."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
DEFAULT_RESULTS = {
    "pbs": ROOT / "results/pbs-314/results-2026-07-14T003400.json",
    "Docker Python 3.14": ROOT
    / "results/python-docker/results-2026-07-14T071250.json",
    "conda-forge": ROOT / "results/conda-forge/results-2026-07-14T034045.json",
    "Fedora 44": ROOT / "results/fedora/results-2026-07-14T102916.json",
    "Debian Forky": ROOT
    / "results/debian-forky/results-2026-07-14T133433.json",
    "macOS PBS": ROOT
    / "results/macos-pbs/results-2026-07-15T232756.json",
    "macOS Python.org": ROOT
    / "results/macos-python-org/results-2026-07-16T030402.json",
    "macOS conda-forge": ROOT
    / "results/macos-conda-forge/results-2026-07-16T081106.json",
    "macOS Homebrew": ROOT
    / "results/macos-homebrew/results-2026-07-16T011743.json",
    "Windows PBS": ROOT / "results/win-pbs/results-2026-07-10T182734.json",
    "Windows Python.org": ROOT
    / "results/win-python-org/results-2026-07-11T042428.json",
    "Windows conda-forge": ROOT
    / "results/win-conda-forge/results-2026-07-10T232842.json",
}
EXCLUDED_BENCHMARKS = {"bench_mp_pool"}


def load_timings(filename: Path) -> dict[str, np.ndarray]:
    """Return the measured (non-warmup) timings keyed by benchmark name."""
    with filename.open(encoding="utf-8") as file:
        suite = json.load(file)

    timings = {}
    for benchmark in suite["benchmarks"]:
        name = benchmark["metadata"]["name"]
        if name in timings:
            raise ValueError(f"duplicate benchmark {name!r} in {filename}")

        values = np.asarray(
            [value for run in benchmark["runs"] for value in run.get("values", ())],
            dtype=float,
        )
        if not len(values):
            continue
        if not np.isfinite(values).all() or np.any(values <= 0):
            raise ValueError(f"invalid timing values for {name!r} in {filename}")
        timings[name] = values

    return timings


def plot_comparison(
    comparisons: dict[
        str, tuple[dict[str, np.ndarray], dict[str, np.ndarray]]
    ],
    output: Path,
    dpi: int,
) -> None:
    # Each violin has exactly one observation per benchmark: the provider's
    # mean runtime divided by the corresponding PBS mean runtime.
    distributions = []
    geometric_means = []
    benchmark_counts = []
    for label, (pbs, timings) in comparisons.items():
        names = sorted((set(pbs) & set(timings)) - EXCLUDED_BENCHMARKS)
        if not names:
            raise ValueError(f"{label} has no benchmarks in common with PBS")
        ratios = np.asarray(
            [np.mean(timings[name]) / np.mean(pbs[name]) for name in names]
        )
        # Plotting logarithms makes reciprocal runtime ratios visually symmetric.
        distributions.append(np.log2(ratios))
        geometric_means.append(float(np.exp(np.mean(np.log(ratios)))))
        benchmark_counts.append(len(names))

    if len(set(benchmark_counts)) == 1:
        count_label = str(benchmark_counts[0])
    else:
        count_label = f"{min(benchmark_counts)}-{max(benchmark_counts)}"

    positions = np.arange(len(comparisons))
    figure, ax = plt.subplots(figsize=(10, 9.5), layout="constrained")
    violins = ax.violinplot(
        distributions,
        positions=positions,
        orientation="horizontal",
        widths=0.78,
        showmeans=False,
        showmedians=False,
        showextrema=False,
    )

    provider_colors = {
        "Docker python:3.14": "#397a9a",
        "conda-forge": "#4e8b70",
        "Fedora 44": "#b9773e",
        "Debian Forky": "#865d9c",
        "Python.org": "#397a9a",
        "Homebrew": "#b85b58",
    }
    colors = tuple(
        provider_colors[label.split(" (", 1)[0]] for label in comparisons
    )
    hatches = ("", "", "", "", "///", "///", "///", "xx", "xx")
    for body, color, hatch in zip(
        violins["bodies"], colors, hatches, strict=True
    ):
        body.set_facecolor(color)
        body.set_edgecolor(color)
        body.set_alpha(0.65)
        body.set_linewidth(1)
        body.set_hatch(hatch)
    ax.vlines(
        np.log2(geometric_means),
        positions - 0.24,
        positions + 0.24,
        color="#22262a",
        linewidth=1.8,
        zorder=3,
    )

    low, high = np.log2((0.65, 1.65))
    ax.set_xlim(low, high)

    ratio_ticks = np.asarray([0.2, 0.25, 0.33, 0.5, 0.75, 1, 1.25, 1.5, 2])
    tick_positions = np.log2(ratio_ticks)
    visible = (tick_positions >= low) & (tick_positions <= high)
    ax.set_xticks(tick_positions[visible])
    ax.set_xticklabels([f"{value:g}x" for value in ratio_ticks[visible]])
    ax.set_yticks(
        positions,
        [
            f"{label.split(' (', 1)[0]}\n{mean - 1:+.0%}"
            for label, mean in zip(comparisons, geometric_means, strict=True)
        ],
    )
    ax.set_ylim(-0.65, len(comparisons) - 0.35)
    ax.invert_yaxis()
    for position, label in (
        (-0.5, "Linux x86-64"),
        (3.5, "macOS arm64"),
        (6.5, "Windows x86-64"),
    ):
        ax.axhline(position, color="#9aa2a9", linewidth=1, zorder=0)
        ax.text(
            0.99,
            position,
            label,
            transform=ax.get_yaxis_transform(),
            ha="right",
            va="center",
            color="#515960",
            fontsize=9,
            fontweight="bold",
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.8},
        )
    ax.grid(axis="x", color="#d4d8dc", linewidth=0.75, zorder=0)
    ax.axvline(0, color="#858e96", linewidth=1.35, zorder=0)
    ax.tick_params(axis="x", top=True, labeltop=True)
    ax.text(
        0.01,
        1.035,
        "← alternative faster",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        color="#515960",
        fontsize=10,
    )
    ax.text(
        0.99,
        1.035,
        "python-build-standalone faster →",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color="#515960",
        fontsize=10,
    )
    ax.set_title(
        "CPython 3.14.6 performance: python-build-standalone vs alternatives",
        fontsize=14,
        fontweight="bold",
        pad=40,
    )
    ax.set_xlabel(
        "Mean runtime ratio (alternative / python-build-standalone, log scale)"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close(figure)
    print(
        f"wrote {output} ({len(comparisons)} violins, "
        f"{count_label} benchmarks each)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pbs", type=Path, default=DEFAULT_RESULTS["pbs"])
    parser.add_argument(
        "--docker", type=Path, default=DEFAULT_RESULTS["Docker Python 3.14"]
    )
    parser.add_argument(
        "--conda-forge", type=Path, default=DEFAULT_RESULTS["conda-forge"]
    )
    parser.add_argument("--fedora", type=Path, default=DEFAULT_RESULTS["Fedora 44"])
    parser.add_argument(
        "--debian-forky", type=Path, default=DEFAULT_RESULTS["Debian Forky"]
    )
    parser.add_argument(
        "--macos-pbs", type=Path, default=DEFAULT_RESULTS["macOS PBS"]
    )
    parser.add_argument(
        "--macos-python-org",
        type=Path,
        default=DEFAULT_RESULTS["macOS Python.org"],
    )
    parser.add_argument(
        "--macos-conda-forge",
        type=Path,
        default=DEFAULT_RESULTS["macOS conda-forge"],
    )
    parser.add_argument(
        "--macos-homebrew", type=Path, default=DEFAULT_RESULTS["macOS Homebrew"]
    )
    parser.add_argument(
        "--windows-pbs", type=Path, default=DEFAULT_RESULTS["Windows PBS"]
    )
    parser.add_argument(
        "--windows-python-org",
        type=Path,
        default=DEFAULT_RESULTS["Windows Python.org"],
    )
    parser.add_argument(
        "--windows-conda-forge",
        type=Path,
        default=DEFAULT_RESULTS["Windows conda-forge"],
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / "pbs-314-comparison.png"
    )
    parser.add_argument(
        "--dpi", type=int, default=180, help="output DPI (default: %(default)s)"
    )
    args = parser.parse_args()
    if args.dpi < 1:
        parser.error("--dpi must be positive")

    linux_pbs = load_timings(args.pbs)
    macos_pbs = load_timings(args.macos_pbs)
    windows_pbs = load_timings(args.windows_pbs)
    comparisons = {
        "Docker python:3.14": (
            linux_pbs,
            load_timings(args.docker),
        ),
        "conda-forge": (
            linux_pbs,
            load_timings(args.conda_forge),
        ),
        "Fedora 44": (linux_pbs, load_timings(args.fedora)),
        "Debian Forky": (
            linux_pbs,
            load_timings(args.debian_forky),
        ),
        "Python.org (macOS)": (
            macos_pbs,
            load_timings(args.macos_python_org),
        ),
        "conda-forge (macOS)": (
            macos_pbs,
            load_timings(args.macos_conda_forge),
        ),
        "Homebrew": (
            macos_pbs,
            load_timings(args.macos_homebrew),
        ),
        "Python.org (Windows)": (
            windows_pbs,
            load_timings(args.windows_python_org),
        ),
        "conda-forge (Windows)": (
            windows_pbs,
            load_timings(args.windows_conda_forge),
        ),
    }
    plot_comparison(comparisons, args.output, args.dpi)


if __name__ == "__main__":
    main()
