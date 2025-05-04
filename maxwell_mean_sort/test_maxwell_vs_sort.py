import ctypes
import random
import time

# Load C DLL
c_sort = ctypes.CDLL("./maxwell_mean.dll")
c_sort.maxwell_mean_sort_py.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
c_sort.maxwell_mean_sort_py.restype = None

data = [random.randint(0, 100000) for _ in range(1000000)]

# Python .sort()
a = list(data)
start = time.perf_counter()
a.sort()
print("Python .sort():", time.perf_counter() - start)

# Maxwell Mean (C)
b = (ctypes.c_int * len(data))(*data)
start = time.perf_counter()
c_sort.maxwell_mean_sort_py(b, len(data))
print("Maxwell Mean (C):", time.perf_counter() - start)

# Check
print("Match:", a == list(b))
