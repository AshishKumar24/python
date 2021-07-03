# move the zeroes to the end of array

arr = [0, 1, 0, 3, 12]

for i, ele in enumerate(arr):
    if ele == 0:
        del arr[i]
        arr.append(ele)

print(arr)
