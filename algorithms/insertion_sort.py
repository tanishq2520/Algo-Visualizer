"""Insertion Sort (generator)
"""
from typing import List, Generator, Dict
def insertion_sort(arr: List[int]) -> Generator[Dict, None, None]:
    a = arr.copy()
    comparisons = 0
    swaps = 0
    yield {"state": a.copy(), "highlight": (), "info": "start", "comparisons": comparisons, "swaps": swaps}
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        yield {"state": a.copy(), "highlight": (i,), "info": f"take {i}", "comparisons": comparisons, "swaps": swaps}
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                yield {"state": a.copy(), "highlight": (j + 1,), "info": "shift", "comparisons": comparisons, "swaps": swaps}
                j -= 1
            else:
                break
        a[j + 1] = key
        yield {"state": a.copy(), "highlight": (j + 1,), "info": f"placed at {j+1}", "comparisons": comparisons, "swaps": swaps}
    yield {"state": a.copy(), "highlight": (), "info": "done", "comparisons": comparisons, "swaps": swaps}
