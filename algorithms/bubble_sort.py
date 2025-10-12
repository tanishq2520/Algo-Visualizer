"""Bubble Sort (generator)

Yields dicts with:
- state: list of numbers
- highlight: tuple of indices being compared or swapped
- info: short string
"""
from typing import List, Generator, Dict
def bubble_sort(arr: List[int]) -> Generator[Dict, None, None]:
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0
    yield {"state": a.copy(), "highlight": (), "info": "start", "comparisons": comparisons, "swaps": swaps}
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            yield {"state": a.copy(), "highlight": (j, j+1), "info": f"compare {j} and {j+1}", "comparisons": comparisons, "swaps": swaps}
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                yield {"state": a.copy(), "highlight": (j, j+1), "info": f"swapped {j} & {j+1}", "comparisons": comparisons, "swaps": swaps}
    yield {"state": a.copy(), "highlight": (), "info": "done", "comparisons": comparisons, "swaps": swaps}
