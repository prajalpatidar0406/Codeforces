#https://codeforces.com/problemset/problem/1917/B
#unsolved
#reason: "due to time limit exceed on TEST 3"

def solve(s, dp):
    if len(s) < 1 or s in dp:
        return
    dp.add(s)
    solve(s[1:], dp)
    solve(s[:1]+s[2:], dp)
t = int(input())
for _ in range(t):
    n = int(input())
    s = input()
    dp = set()
    solve(s,dp)
    print(len(dp))