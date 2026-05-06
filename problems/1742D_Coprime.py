#https://codeforces.com/problemset/problem/1742/D

import math

def solve(arr, n):
    dp = {}
    for i in range(n):
        dp[arr[i]] = i+1
    values = list(dp.keys())
    ans = -1
    for x in range(len(values)):
        v1 = values[x]
        for y in range(x, len(values)):
            v2 = values[y]
            if math.gcd(v1, v2) == 1:
                ans = max(ans, dp[v1] + dp[v2])
    return ans

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    print(solve(arr, n))