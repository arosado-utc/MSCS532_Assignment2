"""
MSCS 532 - Assignment 2
Analyzing and Implementing Divide-and-Conquer Algorithms

By: Alfredo Rosado
Date: 11-01-26

Two divide-and-conquer sorting algorithms:

  1. Merge Sort - split, sort each half, merge the sorted halves.
  2. Quick Sort - pick a pivot, partition around it, sort the parts.

Based on Chapter 7 of Cormen, Leiserson, Rivest & Stein,
"Introduction to Algorithms" (4th ed., 2022).

TODO: implement both algorithms.
"""


def merge_sort(arr):
    """Sort a list of comparable elements in increasing order.

    TODO: implement the divide-and-conquer merge sort (split the
    list in half, recursively sort each half, then merge the two
    sorted halves).
    """
    # Placeholder - the algorithm is not implemented yet.
    return arr


def quick_sort(arr):
    """Sort a list of comparable elements in place, in increasing order.

    TODO: implement the divide-and-conquer quick sort (pick a pivot,
    partition the list around it, then sort the two parts).
    """
    # Placeholder - the algorithm is not implemented yet.
    return arr


def main():
    # A few sample lists to demonstrate the sorts
    sample_arrays = [
        [12, 11, 13, 5, 6],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [4, 4, 2, 4, 1],
        [-3, 0, -7, 4, -1],
    ]

    for sample in sample_arrays:
        original = list(sample)
        merged = merge_sort(sample)
        quick_sort(sample)
        print(f"Before:     {original}")
        print(f"merge:      {merged}")
        print(f"quick (in-place): {sample}")
        print()


if __name__ == "__main__":
    main()
