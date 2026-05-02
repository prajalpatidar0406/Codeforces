#https://codeforces.com/problemset/problem/1914/C

def dfs(arr, brr, idx, max_brr, k, ans):
    if k <= 0:
        return ans
    a = 0
    if idx < len(arr):
        a = dfs(arr, brr, idx+1, max(max_brr, brr[idx]), k-1, ans + arr[idx])
    b = ans + (k*max_brr)
    return max(a, b)

t = int(input())
for _ in range(t):
    n,k = map(int, input().split())
    arr = list(map(int, input().split()))
    brr = list(map(int, input().split()))
    # print(dfs(arr, brr, 1, brr[0], k-1, arr[0]))
    ans = 0
    max_brr = 0
    sum = 0
    for i in range(min(k,n)):
        sum += arr[i]
        max_brr = max(max_brr, brr[i])
        ans = max(ans, sum + (k-i-1) * max_brr)
    print(ans)

