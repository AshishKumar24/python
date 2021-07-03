# To get the maximum sum of the k consecutive elements in array of size n

def maxSum(arr, k):
    arr_sum = []
    for i in range(len(arr)):
        sum = 0
        if len(arr) - i >= k:
            for j in range(k):
                sum += arr[i+j]

        arr_sum.append(sum)
    return sorted(arr_sum, reverse=True)[0]


import numpy

arr = [80, -50, 90, 100]
k = 2
print(f"Max sum of {k} consecutive elements is {maxSum(arr, k)}")
