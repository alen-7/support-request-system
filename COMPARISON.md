# Comparing searching and sorting approaches

## Searching by request ID

| Approach | How it works | Time | Needs a sorted list? |
|----------|--------------|------|----------------------|
| Linear search | Check every request until the ID is found | O(n) | No |
| Binary search | Look at the middle, discard the half that cannot contain the ID, repeat | O(log n) | Yes |

The program itself uses a dictionary lookup (O(1)) for ID search. Linear and
binary search are included so the approaches can be compared.

Binary search is much faster per lookup, but the list must be sorted first
(O(n log n), done once). It pays off when we search many times. For a few
lookups on a small list, linear search is simpler and just as good.

## Sorting requests

| Approach | How it works | Time | Extra space |
|----------|--------------|------|-------------|
| Bubble sort (written by hand) | Repeatedly swap neighbours that are out of order | O(n^2) worst case, O(n) if already sorted | O(n) here, because it works on a copy |
| Built-in `sorted()` | Timsort, a mix of merge sort and insertion sort | O(n log n) | O(n) |

Both give the same result (the tests check this). Bubble sort is easy to
understand but becomes slow quickly as n grows. The built-in sort is the
better choice for real use.

## My measurements (one run of `compare_algorithms.py`)

Times are in seconds and differ on every computer.

Search, 200 lookups:

| n | Linear | Binary | One-off sort for binary |
|---|--------|--------|-------------------------|
| 500 | 0.00109 | 0.00017 | 0.00008 |
| 2000 | 0.00395 | 0.00021 | 0.00035 |
| 8000 | 0.02145 | 0.00043 | 0.00178 |

Sort, one sort:

| n | Bubble | Built-in |
|---|--------|----------|
| 200 | 0.00321 | 0.00006 |
| 500 | 0.02092 | 0.00021 |
| 1000 | 0.08576 | 0.00038 |

## What the numbers show
- When n grows 4 times (2000 to 8000), linear search takes about 5 times
  longer, while binary search only about doubles.
- When n grows 2 times (500 to 1000), bubble sort takes about 4 times longer,
  which matches O(n^2). The built-in sort grows by less than 2 times.

Re-run the script on your own computer and replace these numbers with yours.
