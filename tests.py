"""
MSCS 532 - Assignment 2
Test suite for the merge sort and quick sort implementations in main.py.

Run with:  python3 tests.py

Covers correctness against Python's built-in sorted(), the functional
vs in-place contracts of the two sorts, stability, and the quadratic
worst case on ordered input.
"""

import random
import sys

from main import merge_sort, quick_sort


def test_merge_sort_matches_builtin():
    """Merge sort must agree with the built-in sorted() on random data."""
    rng = random.Random(7)
    for n in (0, 1, 2, 5, 50, 500):
        data = [rng.randint(-1000, 1000) for _ in range(n)]
        assert merge_sort(data) == sorted(data), f"n={n}"


def test_merge_sort_does_not_modify_input():
    """merge_sort is functional: it returns a NEW list and leaves the
    original list exactly as it was."""
    data = [5, 3, 8, 1]
    original = list(data)
    result = merge_sort(data)
    assert data == original, "merge_sort must not modify its input"
    assert result is not data, "merge_sort must return a new list"
    assert result == sorted(original)


def test_merge_sort_is_stable():
    """Equal elements must keep their original relative order."""
    # Tagged pairs: the value is first, the tag is second. A stable sort
    # of (value, tag) pairs must leave the tags in ascending order within
    # each value group.
    pairs = [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3)]
    out = merge_sort(pairs)
    assert out == [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]


def test_merge_sort_duplicates_and_negatives():
    """Duplicates and negative numbers must be handled correctly."""
    assert merge_sort([4, 4, 2, 4, 1]) == [1, 2, 4, 4, 4]
    assert merge_sort([-3, 0, -7, 4, -1]) == [-7, -3, -1, 0, 4]
    assert merge_sort([]) == []
    assert merge_sort([42]) == [42]


def test_quick_sort_matches_builtin():
    """Quick sort must agree with the built-in sorted() on random data."""
    rng = random.Random(99)
    for n in (0, 1, 2, 5, 50, 500):
        data = [rng.randint(-1000, 1000) for _ in range(n)]
        quick_sort(data)
        assert data == sorted(data), f"n={n}"


def test_quick_sort_is_in_place():
    """quick_sort must sort the SAME list object and return it."""
    data = [5, 3, 8, 1]
    result = quick_sort(data)
    assert result is data, "quick_sort must sort in place"
    assert data == [1, 3, 5, 8]


def test_quick_sort_worst_case_sorted():
    """Already-sorted input hits the O(n^2) worst case with the
    last-element pivot; it must still produce the right answer."""
    sys.setrecursionlimit(100_000)
    data = list(range(4096))
    quick_sort(data)
    assert data == list(range(4096))


def test_quick_sort_worst_case_reverse_sorted():
    """Reverse-sorted input is the other degenerate case."""
    sys.setrecursionlimit(100_000)
    data = list(range(4096, 0, -1))
    quick_sort(data)
    assert data == list(range(1, 4097))


def test_quick_sort_duplicates():
    """Many equal elements must not break the partition."""
    data = [3, 3, 3, 1, 3, 2, 3, 3]
    quick_sort(data)
    assert data == [1, 2, 3, 3, 3, 3, 3, 3]


def test_both_sorts_agree():
    """On the same random data the two algorithms must produce the
    same sorted result."""
    rng = random.Random(1234)
    data = [rng.randint(-500, 500) for _ in range(300)]
    assert merge_sort(data) == list(quick_sort(list(data)))


def main():
    tests = [
        test_merge_sort_matches_builtin,
        test_merge_sort_does_not_modify_input,
        test_merge_sort_is_stable,
        test_merge_sort_duplicates_and_negatives,
        test_quick_sort_matches_builtin,
        test_quick_sort_is_in_place,
        test_quick_sort_worst_case_sorted,
        test_quick_sort_worst_case_reverse_sorted,
        test_quick_sort_duplicates,
        test_both_sorts_agree,
    ]

    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL: {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR: {test.__name__}: {type(e).__name__}: {e}")

    print()
    if failed:
        print(f"{failed} of {len(tests)} test(s) FAILED.")
        raise SystemExit(1)
    print(f"All {len(tests)} tests passed.")


if __name__ == "__main__":
    main()
