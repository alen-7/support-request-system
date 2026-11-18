"""Times linear vs binary search, and bubble sort vs built-in sort.

Run:  python compare_algorithms.py
Numbers differ on every computer, but the pattern stays the same.
"""

import random
import time

from search_sort import (
    binary_search_by_id,
    bubble_sort,
    builtin_sort,
    linear_search_by_id,
)


def make_items(n):
    ids = [f"REQ-{i:05d}" for i in range(n)]
    random.shuffle(ids)
    return [
        {"request_id": item, "created": f"2026-01-{(i % 28) + 1:02d}"}
        for i, item in enumerate(ids)
    ]


def timed(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return time.perf_counter() - start, result


def compare_search(n, lookups=200):
    items = make_items(n)
    targets = [random.choice(items)["request_id"] for _ in range(lookups)]
    by_id = lambda item: item["request_id"]
    sort_time, sorted_items = timed(builtin_sort, items, by_id)

    start = time.perf_counter()
    for target in targets:
        linear_search_by_id(items, target)
    linear = time.perf_counter() - start

    start = time.perf_counter()
    for target in targets:
        binary_search_by_id(sorted_items, target)
    binary = time.perf_counter() - start
    return linear, binary, sort_time


def compare_sort(n):
    items = make_items(n)
    key = lambda item: (item["created"], item["request_id"])
    bubble_time, bubble_result = timed(bubble_sort, items, key)
    builtin_time, builtin_result = timed(builtin_sort, items, key)
    assert bubble_result == builtin_result  # both must give the same answer
    return bubble_time, builtin_time


def main():
    random.seed(1)
    print("SEARCH: 200 lookups (seconds)")
    print(f"{'n':>7} {'linear':>10} {'binary':>10} {'one-off sort':>14}")
    for n in (500, 2000, 8000):
        linear, binary, sort_time = compare_search(n)
        print(f"{n:>7} {linear:>10.5f} {binary:>10.5f} {sort_time:>14.5f}")

    print("\nSORT: one sort of n requests (seconds)")
    print(f"{'n':>7} {'bubble':>10} {'built-in':>10}")
    for n in (200, 500, 1000):
        bubble_time, builtin_time = compare_sort(n)
        print(f"{n:>7} {bubble_time:>10.5f} {builtin_time:>10.5f}")


if __name__ == "__main__":
    main()
