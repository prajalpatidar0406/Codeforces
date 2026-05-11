#https://codeforces.com/problemset/problem/1213/B

t =  int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    ans = 0
    mini = arr[-1]
    for i in range(n-1, -1 , -1):
        if arr[i] > mini:
            ans += 1
        elif arr[i] < mini:
            mini = arr[i]
    print(ans)