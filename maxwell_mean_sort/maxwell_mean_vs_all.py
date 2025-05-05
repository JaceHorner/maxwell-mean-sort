import ctypes
import random
import time
import statistics

# Load C DLL
c_sort = ctypes.CDLL("./maxwell_mean.dll")
c_sort.maxwell_mean_sort_py.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
c_sort.maxwell_mean_sort_py.restype = None

# Sorting algorithms in pure Python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heap_sort(arr):
    arr = arr.copy()
    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    return arr

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def shell_sort(arr):
    arr = arr.copy()
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def counting_sort(arr, max_val=None):
    arr = arr.copy()
    if not arr:
        return arr
    if max_val is None:
        max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    result = []
    for i, c in enumerate(count):
        result.extend([i] * c)
    return result

def radix_sort(arr):
    arr = arr.copy()
    RADIX = 10
    placement = 1
    max_digit = max(arr)
    while placement <= max_digit:
        buckets = [[] for _ in range(RADIX)]
        for num in arr:
            tmp = (num // placement) % RADIX
            buckets[tmp].append(num)
        arr = [num for bucket in buckets for num in bucket]
        placement *= RADIX
    return arr

def bucket_sort(arr, bucket_size=1000):
    if not arr:
        return arr
    min_val, max_val = min(arr), max(arr)
    bucket_count = ((max_val - min_val) // bucket_size) + 1
    buckets = [[] for _ in range(bucket_count)]
    for num in arr:
        index = (num - min_val) // bucket_size
        buckets[index].append(num)
    result = []
    for bucket in buckets:
        result.extend(insertion_sort(bucket))
    return result

# Benchmark Config
SIZE = 100_000
NUM_RUNS = 25
SEED = 420
RANGE = 1_000_000

# Initialize result dictionary
results = {
    "TimSort": [],
    "Maxwell Mean (C)": [],
    "Quicksort (Py)": [],
    "MergeSort (Py)": [],
    "HeapSort (Py)": [],
    "ShellSort (Py)": [],
    "CountingSort (Py)": [],
    "RadixSort (Py)": [],
    "BucketSort (Py)": [],
    "InsertionSort (Py)": [],
    "BubbleSort (Py)": [],
    "SelectionSort (Py)": []
}
failures = 0

for i in range(NUM_RUNS):
    print(f"\n🔁 Run {i + 1}")
    random.seed(SEED + i)
    data = [random.randint(0, RANGE) for _ in range(SIZE)]

    def time_sort(name, func, *args):
        start = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - start
        results[name].append(elapsed)
        print(f"{name:<22}: {elapsed:.6f} s")
        return result

    sorted_ref = sorted(data)
    time_sort("TimSort", sorted, data)

    c_array = (ctypes.c_int * SIZE)(*data)
    start = time.perf_counter()
    c_sort.maxwell_mean_sort_py(c_array, SIZE)
    elapsed = time.perf_counter() - start
    results["Maxwell Mean (C)"].append(elapsed)
    print(f"Maxwell Mean (C)     : {elapsed:.6f} s")
    sorted_maxwell = list(c_array)

    sorted_quick = time_sort("Quicksort (Py)", quicksort, data)
    sorted_merge = time_sort("MergeSort (Py)", merge_sort, data)
    sorted_heap = time_sort("HeapSort (Py)", heap_sort, data)
    sorted_shell = time_sort("ShellSort (Py)", shell_sort, data)
    sorted_counting = time_sort("CountingSort (Py)", counting_sort, data, RANGE)
    sorted_radix = time_sort("RadixSort (Py)", radix_sort, data)
    sorted_bucket = time_sort("BucketSort (Py)", bucket_sort, data)

    if SIZE <= 10000:
        sorted_insert = time_sort("InsertionSort (Py)", insertion_sort, data)
        sorted_bubble = time_sort("BubbleSort (Py)", bubble_sort, data)
        sorted_select = time_sort("SelectionSort (Py)", selection_sort, data)
    else:
        results["InsertionSort (Py)"].append(float('inf'))
        results["BubbleSort (Py)"].append(float('inf'))
        results["SelectionSort (Py)"].append(float('inf'))

    # Check correctness
    check_lists = [
        sorted_maxwell, sorted_quick, sorted_merge, sorted_heap, sorted_shell,
        sorted_counting, sorted_radix, sorted_bucket
    ]
    if SIZE <= 10000:
        check_lists += [sorted_insert, sorted_bubble, sorted_select]

    if not all(lst == sorted_ref for lst in check_lists):
        print("❌ Mismatch detected!")
        failures += 1
    else:
        print("✅ Correct: Outputs match.")

# Summary stats
summary_stats = []
for name, times in results.items():
    clean_times = [t for t in times if t != float('inf')]
    avg = statistics.mean(clean_times) if clean_times else float('inf')
    stdev = statistics.stdev(clean_times) if len(clean_times) > 1 else 0
    min_t = min(clean_times) if clean_times else float('inf')
    max_t = max(clean_times) if clean_times else float('inf')
    summary_stats.append((name, avg, stdev, min_t, max_t))

summary_stats.sort(key=lambda x: x[1])
best_time = summary_stats[0][1]
best_algos = [name for name, avg, *_ in summary_stats if avg == best_time]

def print_bar_chart(summary_stats, best_time):
    print("\n=== SORTING PERFORMANCE SUMMARY ===")
    print(f"{'Algorithm':<22} {'Avg Time (s)':<15} {'% Slower':<12} {'Stdev':<10} {'Min':<10} {'Max':<10}  Bar")
    max_len = 40
    for name, avg, stdev, min_t, max_t in summary_stats:
        percent_slower = ((avg - best_time) / best_time) * 100 if avg != best_time else 0
        bar_len = int((best_time / avg) * max_len) if avg != float('inf') else 0
        bar = '█' * bar_len
        print(f"{name:<22} {avg:<15.6f} {percent_slower:<12.2f} {stdev:<10.6f} {min_t:<10.6f} {max_t:<10.6f}  {bar}")

print(f"\n🚀 Fastest Algorithm(s): {', '.join(best_algos)} ({best_time:.6f} s)")
print_bar_chart(summary_stats, best_time)
print(f"\n✅ Correct runs: {NUM_RUNS - failures}/{NUM_RUNS}")
