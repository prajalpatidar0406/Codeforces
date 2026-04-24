#https://codeforces.com/problemset/problem/1873/E
#unsolved
#reason: "due to memory limit"

t = int(input())
for _ in range(t):
    n,x = map(int, input().split())
    arr = list(map(int, input().split()))
    arr.sort()
    prev = -1
    dp = [0] * arr[-1]
    for i in arr:
        for j in range(i):
            dp[j] += 1

    sum_c = sum(arr)
    h_h = x // n
    if h_h <= arr[-1]:
        cnt, units = 0, x
        for i in dp:
            units -= (n-i)
            if units < 0:
                break
            cnt += 1
        if units > 0:
            cnt += units // n
        print(cnt)
    else:
        high = h_h + (x%n + sum_c) // n
        print(high)       
        
    
    
