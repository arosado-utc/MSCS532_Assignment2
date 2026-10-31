"""
MSCS 532 - Assignment 2
Analyzing and Implementing Divide-and-Conquer Algorithms

By: Alfredo Rosado
Date: 11-01-26

Two divide-and-conquer sorting algorithms:

  1. Merge Sort  - split the list in half, recursively sort each
                   half, then merge the two sorted halves.
  2. Quick Sort  - choose a pivot, partition the list around it,
                   then recursively sort the two parts.

Based on Chapter 7 of Cormen, Leiserson, Rivest & Stein,
"Introduction to Algorithms" (4th ed., 2022).

TODO: quick sort is not implemented yet.
"""


def merge_sort(arr):
    """Sort a list of comparable elements in increasing order.

    Divide-and-conquer strategy:
        1. Divide   - split arr into two halves of roughly equal size.
        2. Conquer  - recursively merge_sort each half.
        3. Combine  - merge the two sorted halves into one sorted list.

    Parameter: arr - list of comparable elements (e.g. ints or floats)
    Return:    a NEW list containing arr sorted in increasing order

    Complexity:
        Time   - O(n log n) in the best, average, and worst case.
        Space  - O(n) extra at any moment; each merge builds a new
                 list, so the recursion allocates O(n log n) element
                 slots over the whole run.
        Stable - yes, because the merge keeps the left element on ties.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list.

    Parameter: left  - sorted list of comparable elements
               right - sorted list of comparable elements
    Return:    a new list containing every element of left and right
               in non-decreasing order

    The '<=' comparison takes the LEFT element first on ties, which
    is what makes the whole sort stable.
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # One half is exhausted; append whatever the other half has left.
    result.extend(left[i:])
    result.extend(right[j:])
    return result


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
