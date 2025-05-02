# Maxwell Mean Sort

**Maxwell Mean Sort** is a high-performance hybrid sorting algorithm created by **Jace Maxwell Horner**. Implemented in C and callable via Python, it uses adaptive mean-based partitioning, a manual stack to avoid recursion, and insertion sort for small ranges. It consistently outperforms Python’s built-in TimSort and Quicksort in real-world benchmarks across all tested input sizes.

---

## 🔧 Features

- 🚀 Written in C for maximum speed  
- 💾 In-place sort with low memory overhead  
- 📊 Mean-based adaptive pivoting  
- 🧱 Manual stack (no recursion)  
- 🔁 Insertion sort fallback for small segments  
- 🧪 Verified correct across hundreds of runs  
- 🐍 Python wrapper via `ctypes`  
- ⚖️ Open source under MIT License  

---

## 🚀 Benchmarks

**System**: HP Omen 45L  
**Apps running**: Discord, League of Legends: TFT, miscellaneous background programs  
**Environment**: Python 3.11 + 64-bit DLL  
**Benchmark script**: `benchmark_3way.py`  
**Runs per size**: 25 (with hundreds more run manually)

| Array Size     | TimSort (avg) | Maxwell Mean (C) (avg) | Quicksort (Py) (avg) |
|----------------|---------------|--------------------------|------------------------|
| 1,000          | 0.000067 s    | **0.000044 s** (34% faster) | 0.001163 s           |
| 10,000         | 0.000804 s    | **0.000588 s** (27% faster) | 0.012204 s           |
| 100,000        | 0.013288 s    | **0.007390 s** (44% faster) | 0.162290 s           |
| 1,000,000      | 0.196507 s    | **0.097638 s** (50% faster) | 2.252110 s           |
| 10,000,000     | 3.034803 s    | **1.158973 s** (61% faster) | —                    |

✅ All outputs verified for correctness on every run.

---

## 📊 Complexity Comparison

| Algorithm         | Best Case  | Average Case | Worst Case | Space Complexity |
|------------------|------------|---------------|-------------|------------------|
| **Maxwell Mean** | O(n)       | O(n log n)    | O(n²)       | O(log n)         |
| TimSort (Python) | O(n)       | O(n log n)    | O(n log n)  | O(n)             |
| Quicksort (Py)   | O(n log n) | O(n log n)    | O(n²)       | O(log n)         |

> Maxwell Mean achieves **O(n)** best-case performance on sorted or nearly sorted arrays, with efficient manual stack partitioning.  
> Its **average-case** performance is solidly **O(n log n)**, while it avoids recursion depth issues by using an explicit stack.  
> **Worst-case O(n²)** behavior may occur in highly skewed distributions, but is rare in practice.

---

## ⚙️ How It Works

**Maxwell Mean Sort** combines classic partitioning with adaptive strategies for real-world performance. Here's the step-by-step behavior:

1. **Manual Stack Initialization**  
   - Avoids recursion by using a custom stack for managing subarray ranges. Starts with the full array.

2. **Loop Until Sorted**  
   - Continues processing while the stack has unsorted ranges.

3. **Use Insertion Sort for Small Segments**  
   - For ranges with ≤50 elements, insertion sort is applied (faster for tiny partitions).

4. **Compute the Mean**  
   - The pivot is the arithmetic mean of all values in the current segment.

5. **Partition Around Mean**  
   - All elements ≤ mean go to the left, > mean go to the right (in-place partitioning).

6. **Push Subranges Back on Stack**  
   - After partitioning, left and right subsegments are pushed to be sorted in future iterations.

7. **Repeat**  
   - The process continues until all segments are sorted.

This hybrid approach is both space-efficient and practical for large-scale use.

---

## 📁 Files Included

- `maxwell_mean.c` — C source code  
- `maxwell_mean.dll` — Compiled DLL (64-bit Windows)  
- `benchmark_3way.py` — Benchmark script for 3-way comparison  
- `README.md` — This file  
- `LICENSE` — MIT License  

---

## 📦 Usage

### Compile the DLL (if needed):

```bash
gcc -shared -o maxwell_mean.dll -O2 -fPIC maxwell_mean.c

python benchmark_3way.py
