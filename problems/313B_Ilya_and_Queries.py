#https://codeforces.com/problemset/problem/313/B

s = input()
m = int(input())
dp = [0] * (len(s) + 1)
for i in range(0,len(s)-1):
    if s[i] == s[i+1]:
        dp[i+1] = dp[i] + 1
    else:
        dp[i+1] = dp[i]

for _ in range(m):
    l,r = map(int, input().split())
    # print(dp)
    if(l == 1):
        print(dp[r-1])
    else:
        print(dp[r-1] - dp[l-1])