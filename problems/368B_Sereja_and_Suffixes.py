#https://codeforces.com/problemset/problem/368/B

n,m = map(int, input().split())
arr = list(map(int, input().split()))
st = set()
dp = [0] * n
for i, val in reversed(list(enumerate(arr))):
    st.add(val)
    dp[i] = len(st)

for _ in range(m):
    l = int(input())
    print(dp[l-1])