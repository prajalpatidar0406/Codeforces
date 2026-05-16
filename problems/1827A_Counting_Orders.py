#https://codeforces.com/problemset/problem/1827/A
#recheck
#recheck_reason: "copied from tutorial"

from bisect import bisect_right
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    brr = list(map(int, input().split()))
    arr.sort()
    brr.sort(reverse=True)
    result = 1
    for i in range(n):
        idx = n - bisect_right(arr, brr[i])
        print(idx, arr[idx-1], brr[i])
        result *= max((idx-i), 0)
        print(result)
    print(result)