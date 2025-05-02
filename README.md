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
**Runs per size**: 25 (with hundreds more done manually)

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
> Its **average performance** is solidly **O(n log n)**, and it handles large arrays with minimal memory thanks to its in-place design.  
> Worst-case O(n²) is only encountered in extreme pivot imbalance scenarios.

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
