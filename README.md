# MSCS532 Assignment 2: Divide-and-Conquer Sorting

Python implementations of **merge sort** and **quick sort**, two classic
divide-and-conquer sorting algorithms from Chapter 7 of Cormen, Leiserson,
Rivest & Stein, *Introduction to Algorithms* (4th ed., 2022). Both are
implemented in Python and benchmarked against each other on sorted,
reverse-sorted, and random inputs, measuring execution time and peak
memory.

## Requirements

- Python 3.8 or higher
- matplotlib (optional, only for the comparison plots)

## Files

| File                     | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| `main.py`                | Merge sort and quick sort + small demo                   |
| `benchmark.py`           | Benchmark harness (time + peak memory, CSV + plots)      |
| `tests.py`               | Test suite that verifies both sorts behave correctly     |
| `results/`               | `benchmark_results.csv` — the measured data              |
| `plots/`                 | Log-log comparison plots generated from the CSV          |

## How to run

Run the demo:

```bash
python3 main.py
```

Run the tests:

```bash
python3 tests.py
```

Run the benchmark (writes `results/benchmark_results.csv` and `plots/`):

```bash
python3 benchmark.py
```

## How it works

**Merge sort** is functional: it splits the list into two halves,
recursively sorts each half, and merges the sorted halves with a
two-pointer pass. The merge takes the left element first on ties, which
makes the sort stable. It returns a new list and never touches the input.

**Quick sort** sorts in place using the Lomuto partition scheme with the
last element as the pivot, which reproduces
the textbook O(n^2) worst case on already-ordered input, which the
benchmark then measures.

```python
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

## Complexity

- **Merge sort:** O(n log n) time in all cases, O(n) extra space, stable
- **Quick sort:** O(n log n) average, O(n^2) worst case (ordered input
  with the last-element pivot), O(log n) stack space on average, not stable

## Benchmark notes

- Random data runs from 1,024 to 32,768 elements; the ordered inputs
  stop at 8,192, because the quadratic worst case makes each doubling
  cost 4x more, and four doublings are enough to show the trend.
- Time is wall time around the sort call; memory is the peak of Python
  allocations tracked by `tracemalloc`.
- The ordered-input plots show quick sort's time quadrupling with each
  doubling of n — the O(n^2) signature — while merge sort keeps growing
  roughly as n log n.

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).
  *Introduction to Algorithms* (4th ed.). MIT Press.
- Peters, O. (2021). Pattern-defeating Quicksort [Preprint]. arXiv.
  https://arxiv.org/abs/2106.05123
