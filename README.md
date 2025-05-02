# Maxwell Mean Sort

**Maxwell Mean Sort** is a custom high-performance hybrid sorting algorithm created by **Jace Maxwell Horner**. It uses adaptive mean-based partitioning and a manual stack to deliver competitive speed and correctness across a wide range of array sizes, written in C and callable via Python.

---

## 🔧 Features

- In-place sort (no extra memory required)
- Mean-based partitioning
- Adaptive manual stack recursion
- Insertion sort fallback for small ranges
- Outperforms TimSort and Quicksort in real-world tests
- Simple Python wrapper with ctypes

---

## 🚀 Benchmarks (Python 3.11 + C DLL)

**Test system**: HP Omen 45L  
**Running alongside**: Discord, League of Legends: TFT, and miscellaneous background apps  
**Benchmark script**: `benchmark_3way.py`  
**Test runs**: 25 per array size  

| Array Size | TimSort (avg) | Maxwell Mean (C) (avg) | Quicksort (Py) (avg) |
|------------|---------------|-------------------------|----------------------|
| 1,000      | 0.000067 s    | **0.000044 s**          | 0.001163 s           |
| 10,000     | 0.000804 s    | **0.000588 s**          | 0.012204 s           |
| 100,000    | 0.013288 s    | **0.007390 s**          | 0.162290 s           |
| 1,000,000  | 0.196507 s    | **0.097638 s**          | 2.252110 s           |
| 10,000,000 | 3.034803 s    | **1.158973 s**          | —                    |

✅ All runs verified correct (25/25 per test set)

---

## 📁 Files Included

- `maxwell_mean.c` — Source code (C implementation)
- `maxwell_mean.dll` — Compiled 32/64-bit Windows DLL
- `benchmark_3way.py` — 3-way comparison benchmark (TimSort, Quicksort, Maxwell Mean)
- `README.md` — Project overview and attribution (this file)

---

## 📦 Usage Example

```bash
# Ensure DLL is compiled
gcc -shared -o maxwell_mean.dll -O2 -fPIC maxwell_mean.c

# Run benchmark in Python
python benchmark_3way.py
