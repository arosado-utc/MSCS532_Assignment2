"""
MSCS 532 - Assignment 2
Performance comparison of merge sort vs quick sort.

Runs both sorts on sorted, reverse-sorted, and random inputs of
increasing size, and records execution time and peak memory usage.

Run:  python3 benchmark.py

Output:
    results/benchmark_results.csv   one row per (dataset, size, algorithm)
    plots/execution_time.png        (if matplotlib is installed)
    plots/peak_memory.png           (if matplotlib is installed)

Measurement notes:
    * Time is wall time around the sort call, averaged over the runs.
    * Memory is the peak of Python allocations tracked by tracemalloc.
    * For sizes >= 16384 only 1 run is used.
    * The ordered datasets stop at 8,192: the quadratic worst case
      would make 32,768 an hour-long run, and four doublings are
      enough to show the O(n^2) signature.
"""

import csv
import os
import random
import sys
import time
import tracemalloc

from main import merge_sort, quick_sort

# Random data stays n log n at every size, so it runs all the way up.
# Sorted and reverse-sorted inputs drive quick sort's quadratic worst
# case, where each doubling costs 4x more; 8,192 is the largest size
# that stays fast, and four doublings are plenty to show the trend.
DATASETS = {
    "random": [1024, 2048, 4096, 8192, 16384, 32768],
    "sorted": [1024, 2048, 4096, 8192],
    "reverse_sorted": [1024, 2048, 4096, 8192],
}
LARGE_SIZE = 16384  # use a single run for sizes >= this value


def make_data(kind, n, seed=42):
    """Build an n-element dataset of the requested kind."""
    rng = random.Random(seed)
    base = [rng.randint(0, n * 10) for _ in range(n)]
    if kind == "sorted":
        return sorted(base)
    if kind == "reverse_sorted":
        return sorted(base, reverse=True)
    return base


def time_and_memory(sort_fn, data, reps):
    """Measure mean wall time (s) and peak memory (MB) over the runs.

    Each run works on a fresh copy of the data, so the runs are
    independent of each other.

    Parameter: sort_fn - a sorting function applied to a list
               data    - the dataset to sort (a list of numbers)
               reps    - how many independent runs to average over
    Return:    (mean_seconds, peak_megabytes)
    """
    times = []
    peak_bytes = 0
    for _ in range(reps):
        arr = list(data)  # fresh copy so every run starts equal
        tracemalloc.start()
        start = time.perf_counter()
        sort_fn(arr)
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        times.append(elapsed)
        peak_bytes = max(peak_bytes, peak)
    return sum(times) / len(times), peak_bytes / (1024 * 1024)


def check_result(sort_name, sort_fn, data):
    """Verify one sort actually produces a sorted, complete result."""
    arr = list(data)
    if sort_name == "merge_sort":
        # merge_sort returns a NEW list; the input must be untouched
        out = sort_fn(arr)
        assert out == sorted(data), f"{sort_name} produced a wrong result"
        assert arr == data, "merge_sort must not modify its input"
    else:
        # quick_sort sorts the SAME list in place
        out = sort_fn(arr)
        assert out is arr, "quick_sort must sort in place"
        assert arr == sorted(data), f"{sort_name} produced a wrong result"


def run_benchmark():
    rows = []
    for kind, sizes in DATASETS.items():
        for n in sizes:
            data = make_data(kind, n)
            reps = 1 if n >= LARGE_SIZE else 3
            for name, fn in (("merge_sort", merge_sort),
                             ("quick_sort", quick_sort)):
                check_result(name, fn, data)
                t, mem = time_and_memory(fn, data, reps)
                rows.append((kind, n, name, t, mem))
                print(f"{kind:15s} n={n:6d} {name:11s} "
                      f"{t * 1000:12.3f} ms   peak {mem:8.3f} MB")
    return rows


def write_csv(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "n", "algorithm",
                    "time_seconds", "peak_memory_mb"])
        for kind, n, name, t, mem in rows:
            w.writerow([kind, n, name, f"{t:.6f}", f"{mem:.4f}"])


def make_plots(rows):
    """Save two comparison plots. Skipped if matplotlib is absent."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib is not installed - skipping plots.")
        return

    os.makedirs("plots", exist_ok=True)
    datasets = [("sorted", "Sorted"),
                ("reverse_sorted", "Reverse-sorted"),
                ("random", "Random")]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (key, label) in zip(axes, datasets):
        for name, color in (("merge_sort", "tab:blue"),
                            ("quick_sort", "tab:red")):
            xs = [r[1] for r in rows if r[0] == key and r[2] == name]
            ys = [r[3] * 1000 for r in rows if r[0] == key and r[2] == name]
            ax.plot(xs, ys, marker="o", label=name, color=color)
        ax.set_title(label)
        ax.set_xlabel("n")
        ax.set_ylabel("time (ms)")
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
    fig.suptitle("Execution time by dataset")
    fig.tight_layout()
    fig.savefig("plots/execution_time.png", dpi=150)

    fig2, ax = plt.subplots(figsize=(6, 4))
    for name, color in (("merge_sort", "tab:blue"),
                        ("quick_sort", "tab:red")):
        xs = [r[1] for r in rows if r[0] == "random" and r[2] == name]
        ys = [r[4] for r in rows if r[0] == "random" and r[2] == name]
        ax.plot(xs, ys, marker="o", label=name, color=color)
    ax.set_title("Peak memory, random data")
    ax.set_xlabel("n")
    ax.set_ylabel("peak memory (MB)")
    ax.set_xscale("log", base=2)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig2.tight_layout()
    fig2.savefig("plots/peak_memory.png", dpi=150)
    print("plots saved to plots/")


def main():
    # quick sort on ordered input recurses n levels deep, so raise
    # the recursion limit before the large worst-case runs
    sys.setrecursionlimit(100_000)

    rows = run_benchmark()
    write_csv(rows, "results/benchmark_results.csv")
    print("\nresults written to results/benchmark_results.csv")
    make_plots(rows)


if __name__ == "__main__":
    main()
