#https://codeforces.com/problemset/problem/1472/C

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    dp = arr.copy()
    maxi_sum = 0
    for i in range(n-1, -1, -1):
        next = i + arr[i]
        dp[i] += dp[next] if next < n else 0
        maxi_sum = max(maxi_sum, dp[i])
    
    print(maxi_sum)