"""Selection Sort (generator)
"""
from typing import List, Generator, Dict
def selection_sort(arr: List[int]) -> Generator[Dict, None, None]:
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0
    yield {"state": a.copy(), "highlight": (), "info": "start", "comparisons": comparisons, "swaps": swaps}
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            yield {"state": a.copy(), "highlight": (min_idx, j), "info": f"compare {min_idx} and {j}", "comparisons": comparisons, "swaps": swaps}
            if a[j] < a[min_idx]:
                min_idx = j
                yield {"state": a.copy(), "highlight": (min_idx,), "info": f"new min {min_idx}", "comparisons": comparisons, "swaps": swaps}
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            yield {"state": a.copy(), "highlight": (i, min_idx), "info": f"swapped {i} & {min_idx}", "comparisons": comparisons, "swaps": swaps}
    yield {"state": a.copy(), "highlight": (), "info": "done", "comparisons": comparisons, "swaps": swaps}
