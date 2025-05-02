import ctypes
import random
import time
import statistics

# Load C DLL
c_sort = ctypes.CDLL("./maxwell_mean.dll")
c_sort.maxwell_mean_sort_py.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
c_sort.maxwell_mean_sort_py.restype = None

# Python quicksort implementation
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)

# Config
SIZE = 100_000
NUM_RUNS = 25
SEED = 420
RANGE = 1_000_000

timsort_times = []
maxwell_times = []
quicksort_times = []
failures = 0

for i in range(NUM_RUNS):
    print(f"\n🔁 Run {i + 1}")
    random.seed(SEED + i)
    data = [random.randint(0, RANGE) for _ in range(SIZE)]

    # TimSort
    start = time.perf_counter()
    sorted_py = sorted(data)
    time_timsort = time.perf_counter() - start
    timsort_times.append(time_timsort)
    print(f"TimSort:         {time_timsort:.6f} s")

    # Maxwell Mean Sort (C)
    c_array = (ctypes.c_int * SIZE)(*data)
    start = time.perf_counter()
    c_sort.maxwell_mean_sort_py(c_array, SIZE)
    time_maxwell = time.perf_counter() - start
    sorted_c = list(c_array)
    maxwell_times.append(time_maxwell)
    print(f"Maxwell Mean (C): {time_maxwell:.6f} s")

    # Quicksort (pure Python)
    start = time.perf_counter()
    sorted_quick = quicksort(data)
    time_quick = time.perf_counter() - start
    quicksort_times.append(time_quick)
    print(f"Quicksort (Py):   {time_quick:.6f} s")

    # Verify correctness
    if sorted_py != sorted_c or sorted_py != sorted_quick:
        print("❌ Mismatch detected!")
        failures += 1
    else:
        print("✅ Correct: Outputs match.")

# Summary
print("\n=== AVERAGE TIMES ===")
print(f"TimSort avg:         {statistics.mean(timsort_times):.6f} s")
print(f"Maxwell Mean avg:    {statistics.mean(maxwell_times):.6f} s")
print(f"Quicksort (Py) avg:  {statistics.mean(quicksort_times):.6f} s")
print(f"\nCorrect runs: {NUM_RUNS - failures}/{NUM_RUNS}")