"""Binary Search (generator)

Yields search range updates.
"""
from typing import List, Generator, Dict, Optional
def binary_search(arr: List[int], target: int) -> Generator[Dict, None, Optional[int]]:
    a = arr
    lo = 0
    hi = len(a) - 1
    comparisons = 0
    yield {"state": a.copy(), "highlight": (lo, hi), "info": "start", "comparisons": comparisons}
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        yield {"state": a.copy(), "highlight": (mid,), "info": f"check {mid}", "comparisons": comparisons}
        if a[mid] == target:
            yield {"state": a.copy(), "highlight": (mid,), "info": "found", "comparisons": comparisons}
            return mid
        elif a[mid] < target:
            lo = mid + 1
            yield {"state": a.copy(), "highlight": (lo, hi), "info": "move right", "comparisons": comparisons}
        else:
            hi = mid - 1
            yield {"state": a.copy(), "highlight": (lo, hi), "info": "move left", "comparisons": comparisons}
    yield {"state": a.copy(), "highlight": (), "info": "not found", "comparisons": comparisons}
    return None
