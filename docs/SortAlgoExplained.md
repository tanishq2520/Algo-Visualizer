 Sorting Algorithms Explained
 This tool visualizes several comparison-based sorting algorithms, each with a unique approach to ordering data. Understanding how each one works reveals why some are fast (O)(nlog n) and others are slow (O)(n^2).
 
 1. Merge Sort
 Merge Sort is a highly efficient, stable, and comparison-based sorting algorithm based on the divide-and-conquer principle. It guarantees an optimal time complexity of (O)(nlog n).
    Explanation
    Merge Sort works by recursively breaking the list down into smaller sub-lists until each sub-list contains only one element (which is inherently sorted). It then repeatedly merges the sorted sub-lists back together to produce a new, larger sorted list. The merge step is the crucial part, combining two sorted lists into one sorted list in linear time.
    
    Example: [8, 3, 1]
        Divide: Break the list into [8], [3], and [1].
        Merge 1: Merge [8] and [3] --> [3, 8].
        Merge 2: Merge [3, 8] and [1]. Compare 3 with 1 (1 wins). Compare 8 with remaining 3 (8 wins).-->[1, 3, 8]

2. Quick Sort

Quick Sort is an efficient, in-place, and comparison-based algorithm that also uses the divide-and-conquer strategy. While its worst-case performance is (O)(n^2), its average performance is highly efficient at (O)(nlog n).
    Explanation
    Quick Sort works by selecting a pivot element from the array (e.g., the last element). It then partitions the other elements into two sub-arrays: elements less than the pivot go before it, and elements greater than the pivot go after it. This process is then recursively applied to the sub-arrays until the entire array is sorted.
    
    Example: [5, 8, 3, 1]
        Pivot Selection: Select 1 as the pivot (last element).
        Partition: Scan the list. 5 is greater than 1, 8 is greater than 1, 3 is greater than 1. Place the pivot (1) at the beginning.
        Resulting list: [1, 8, 3, 5] (Pivot 1 is now in its final sorted position).
        Recurse: Apply the process to the sub-list [8, 3, 5].
        Pivot 5 is selected. Partitioning leads to [3, 5, 8].
        Final Sorted List: [1, 3, 5, 8]
    
3. Insertion Sort
Insertion Sort is a simple, stable sorting algorithm that is highly efficient for small data sets or lists that are already partially sorted. Its worst-case and average time complexity is (O)(n^2).
    Explanation
    Insertion Sort builds the final sorted list one item at a time. It iterates through the input elements and, for each element, finds its correct position within the already sorted portion of the list by shifting larger elements one position to the right.
    
    Example: [5, 1, 4]
        Start: [5] is the sorted portion.
        Insert 1: Take 1. Compare it to 5. Since 1 < 5, shift 5 to the right. 
        Insert 1.List: [1, 5, 4]
        Insert 4: Take 4. Compare it to 5. Since 4 < 5, shift 5 to the right.
        Compare 4 with 1. Since 4 > 1, stop. 
        Insert 4.
        List: [1, 4, 5]
     
4. Bubble Sort
Bubble Sort is the simplest sorting algorithm. It repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. Because it repeatedly moves the largest elements to the end, it gets its name from elements "bubbling up" to their correct position. Its time complexity is (O)(n^2).

    Explanation
    The algorithm performs multiple passes over the list. In each pass, it compares every adjacent pair and swaps them if the order is incorrect. After the first pass, the largest element is guaranteed to be in its final position at the end. This process repeats for the remaining unsorted portion.
    
    Example: [5, 1, 4]
        Pass 1:Compare (5, 1) --> Swap. List is [1, 5, 4].
        Compare (5, 4) --> Swap. List is [1, 4, 5]. (5 is now sorted)
        Pass 2 (on [1, 4]):Compare (1, 4) --> No swap.
        Final Sorted List: [1, 4, 5]
    
5. Selection Sort
Selection Sort is a simple, in-place comparison sorting algorithm with a time complexity of (O)(n^2). It is inefficient for large lists but is known for performing the minimum number of swaps (at most n-1).

    Explanation
    Selection Sort divides the input list into two parts: a sorted part on the left and an unsorted part on the right. It repeatedly finds the minimum element from the unsorted region and swaps it with the first element of that unsorted region (the boundary element). This process expands the sorted portion one element at a time.
    
    Example: [5, 1, 4]
        Pass 1 (Find Minimum):Scan the whole list [5, 1, 4].
        The minimum is 1 (at index 1).Swap 1 with the starting element (5 at index 0).
        List: [1, 5, 4]. (1 is now sorted)
        Pass 2 (Find Minimum):Scan the unsorted part [5, 4]. The minimum is 4 (at index 2).Swap 4 with the current starting element of the unsorted part (5 at index 1).
        List: [1, 4, 5].
        Final Sorted List: [1, 4, 5]