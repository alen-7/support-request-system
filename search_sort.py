"""Searching and sorting algorithms we compare in this project.

Searching: linear search vs binary search.
Sorting:   bubble sort (written by hand) vs Python's built-in sorted().
"""


def linear_search_by_id(items, request_id):
    """Check every item one by one. Works on any list. Time: O(n)."""
    for item in items:
        if item["request_id"] == request_id:
            return item
    return None


def binary_search_by_id(sorted_items, request_id):
    """Repeatedly halve the search area. The list MUST be sorted by
    request_id first. Time: O(log n)."""
    low = 0
    high = len(sorted_items) - 1
    while low <= high:
        middle = (low + high) // 2
        middle_id = sorted_items[middle]["request_id"]
        if middle_id == request_id:
            return sorted_items[middle]
        elif middle_id < request_id:
            low = middle + 1
        else:
            high = middle - 1
    return None


def bubble_sort(items, key):
    """Sort by repeatedly swapping neighbours that are in the wrong order.
    Time: O(n^2) worst case. Returns a new list."""
    result = list(items)
    n = len(result)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if key(result[j]) > key(result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:  # already sorted, stop early
            break
    return result


def builtin_sort(items, key):
    """Python's built-in sort (Timsort). Time: O(n log n). Returns a new list."""
    return sorted(items, key=key)
