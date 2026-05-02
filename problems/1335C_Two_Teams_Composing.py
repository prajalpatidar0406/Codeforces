#https://codeforces.com/problemset/problem/1335/C

from collections import Counter

def solve(arr):
    multi_cnt = 1
    for val,c in arr.items():
        if c > 1:
            multi_cnt = max(multi_cnt,c)
    n = len(arr)
    if n > multi_cnt:
        return multi_cnt
    elif multi_cnt > n:
        return n
    else:
        return n-1


t = int(input())
for _ in range(t):
    n = int(input())
    arr = Counter(map(int, input().split()))
    if n == 1:
        print(0)
    else:
        print(solve(arr))