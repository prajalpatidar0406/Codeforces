#https://codeforces.com/problemset/problem/1770/A

from bisect import bisect_left

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))
    brr = list(map(int, input().split()))
    c  = arr + brr
    c = sorted(c[0:n+m-1])
    c.reverse()
    print(sum(c[0:n-1]) + brr[-1])
