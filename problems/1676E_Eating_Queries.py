#https://codeforces.com/problemset/problem/1676/E

from bisect import bisect_left
t = int(input())
for _ in range(t):
    n,q = map(int, input().split())
    arr = list(map(int, input().split()))
    arr.sort(reverse=True)
    pref = [0] * (n+1)
    for i in range(n):
        pref[i+1] = arr[i] + pref[i]
    for __ in range(q):
        x = int(input())
        ans = bisect_left(pref, x)
        print(ans if ans <= n else -1)
