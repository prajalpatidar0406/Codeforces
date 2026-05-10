#https://codeforces.com/problemset/problem/1618/C

import math

def check_if_divide(arr, divi):
    for val in arr:
        if val%divi == 0:
            return True
    return False

def solve(n, arr):
    if n == 2:
        maxi = max(arr)
        return maxi if arr[0] != arr[1] else 0
    gcde = math.gcd(*arr[0:n:2])
    gcdo = math.gcd(*arr[1:n:2])
    if not check_if_divide(arr[0:n:2], gcdo):
        return gcdo
    if not check_if_divide(arr[1:n:2], gcde):
        return gcde
    return 0

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    print(solve(n, arr))