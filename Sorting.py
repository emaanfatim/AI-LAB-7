import time
import heapq


def print_array(arr):
    print("[", ", ".join(map(str, arr)), "]", sep="")

def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def analyze_array(arr):
    n = len(arr)

    if n == 0:
        return {
            "size": 0,
            "min": None,
            "max": None,
            "sortedness": 100,
            "pattern": "Empty"
        }

    inversions = sum(1 for i in range(n-1) if arr[i] > arr[i+1])
    sortedness = 100 - ((inversions / n) * 100)

    if is_sorted(arr):
        pattern = "Already Sorted"
    elif all(arr[i] > arr[i+1] for i in range(n-1)):
        pattern = "Reverse Sorted"
    elif sortedness >= 80:
        pattern = "Nearly Sorted"
    else:
        pattern = "Random"

    return {
        "size": n,
        "min": min(arr),
        "max": max(arr),
        "sortedness": round(sortedness, 2),
        "pattern": pattern
    }


def bubble_sort(arr):
    c = 0
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            c += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return c

def selection_sort(arr):
    c = 0
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            c += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return c

def insertion_sort(arr):
    c = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            c += 1
            if arr[j] > key:
                arr[j+1] = arr[j]
                j -= 1
            else:
                break
        arr[j+1] = key
    return c

def quick_sort(arr):
    c = [0]

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            c[0] += 1
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i + 1

    def quick(low, high):
        if low < high:
            p = partition(low, high)
            quick(low, p-1)
            quick(p+1, high)

    quick(0, len(arr)-1)
    return c[0]

def merge_sort(arr):
    c = [0]

    def merge(left, right):
        res = []
        i = j = 0
        while i < len(left) and j < len(right):
            c[0] += 1
            if left[i] < right[j]:
                res.append(left[i]); i += 1
            else:
                res.append(right[j]); j += 1
        res.extend(left[i:])
        res.extend(right[j:])
        return res

    def divide(a):
        if len(a) <= 1:
            return a
        mid = len(a)//2
        return merge(divide(a[:mid]), divide(a[mid:]))

    sorted_arr = divide(arr)
    for i in range(len(arr)):
        arr[i] = sorted_arr[i]

    return c[0]

def heap_sort(arr):
    heap = arr[:]
    heapq.heapify(heap)
    for i in range(len(arr)):
        arr[i] = heapq.heappop(heap)
    return 0

def python_sort(arr):
    arr.sort()
    return 0

def smart_decision(info):
    size = info["size"]
    pattern = info["pattern"]
    sortedness = info["sortedness"]

    if pattern == "Already Sorted":
        return ("Insertion Sort",
                "Already sorted → O(n)",
                "Bubble Sort")

    elif pattern == "Reverse Sorted":
        return ("Merge Sort",
                "Reverse sorted → avoids O(n²)",
                "Heap Sort")

    elif pattern == "Nearly Sorted":
        if size < 15:
            return ("Bubble Sort",
                    "Nearly sorted small → few swaps",
                    "Insertion Sort")
        else:
            return ("Insertion Sort",
                    "Nearly sorted → efficient shifting",
                    "Bubble Sort")

    elif size <= 5:
        return ("Selection Sort",
                "Very small → simple & consistent",
                "Insertion Sort")

    elif size <= 15:
        return ("Insertion Sort",
                "Small dataset → low overhead",
                "Selection Sort")

    elif size <= 50:
        if sortedness < 40:
            return ("Quick Sort",
                    "Random medium → fast average",
                    "Merge Sort")
        else:
            return ("Insertion Sort",
                    "Moderately sorted",
                    "Quick Sort")

    else:
        if pattern == "Random":
            return ("Heap Sort",
                    "Large random → guaranteed O(n log n)",
                    "Merge Sort")
        else:
            return ("Merge Sort",
                    "Large structured data",
                    "Heap Sort")

def main():
    print("="*60)
    print(" SMART SORTING SYSTEM")
    print("="*60)

    arr = list(map(int, input("\nEnter numbers: ").split()))

    print("\n Input Array:")
    print_array(arr)

    info = analyze_array(arr)

    print("\n DATA ANALYSIS")
    print(f"Size        : {info['size']}")
    print(f"Sortedness  : {info['sortedness']}%")
    print(f"Range       : {info['min']} – {info['max']}")
    print(f"Pattern     : {info['pattern']}")

    algorithms = [
        ("Python Sort", python_sort),
        ("Quick Sort", quick_sort),
        ("Merge Sort", merge_sort),
        ("Heap Sort", heap_sort),
        ("Insertion Sort", insertion_sort),
        ("Selection Sort", selection_sort),
        ("Bubble Sort", bubble_sort)
    ]

    results = []

    for name, func in algorithms:
        temp = arr.copy()
        start = time.time()
        comp = func(temp)
        end = time.time()

        results.append({
            "name": name,
            "time": round((end-start)*1000, 5),
            "comparisons": comp,
            "sorted": temp
        })

    results.sort(key=lambda x: x["time"])

    print("\n PERFORMANCE TABLE")
    print("-"*60)
    print(f"{'Algorithm':<20}{'Time (ms)':<15}{'Comparisons'}")
    print("-"*60)

    for r in results:
        print(f"{r['name']:<20}{r['time']:<15}{r['comparisons']}")

    print("-"*60)

    decision, reason, secondary = smart_decision(info)

    print("\n SMART DECISION")
    print("-"*60)
    print(f"Primary Recommendation : {decision}")
    print(f"Secondary Option       : {secondary}")
    print(f"Reason                 : {reason}")

    best = results[0]

    print("\n FASTEST ALGORITHM (TESTED)")
    print(f"{best['name']} → {best['time']} ms")

    print("\n Sorted Output:")
    print_array(best["sorted"])

    

    print("\n" + "="*60)

main()
