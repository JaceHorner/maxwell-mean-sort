#include <stdio.h>
#include <stdlib.h>

#define INSERTION_THRESHOLD 50

// --- Insertion Sort ---
void insertion_sort(int* arr, int start, int end) {
    for (int i = start + 1; i <= end; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= start && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

// --- Partition Around Mean ---
int partition(double pivot, int* arr, int start, int end) {
    int left = start;
    int right = end;
    while (left <= right) {
        while (left <= right && arr[left] <= pivot) left++;
        while (left <= right && arr[right] > pivot) right--;
        if (left < right) {
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
    }
    return left;
}

// --- Stack Frame Struct ---
typedef struct {
    int start, end;
} Frame;

// --- Maxwell Mean Sort with Manual Stack ---
void maxwell_mean_sort(int* arr, int len) {
    Frame stack[64];
    int top = 0;
    stack[top++] = (Frame){0, len - 1};

    while (top > 0) {
        Frame frame = stack[--top];
        int start = frame.start;
        int end = frame.end;
        int size = end - start + 1;

        if (size <= INSERTION_THRESHOLD) {
            insertion_sort(arr, start, end);
            continue;
        }

        // Compute mean pivot
        double sum = 0;
        for (int i = start; i <= end; i++) sum += arr[i];
        double pivot = sum / size;

        // Partition in-place
        int mid = partition(pivot, arr, start, end);

        // Push right and left segments
        if (mid < end) stack[top++] = (Frame){mid, end};
        if (start < mid - 1) stack[top++] = (Frame){start, mid - 1};
    }
}

// --- Python-callable Wrapper ---
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT void maxwell_mean_sort_py(int* arr, int len) {
    maxwell_mean_sort(arr, len);
}