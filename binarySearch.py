import time
arr = [1, 2, 3, 4, 5, 6, 7, 8]


def binary_search(start, end, arr, num):
    if end >= start:
        mid = (start+end) // 2
        if arr[mid] == num:
            return mid
        elif arr[mid] > num:
            return binary_search(start, mid, arr, num)
        elif arr[mid] < num:
            return binary_search(mid+1, end, arr, num)
    else:
        return -1


num = 9
index = binary_search(0, 7, arr, num)

if index == -1:
    print("Element not present")
else:
    print(f"Element is at the index: {index}")
