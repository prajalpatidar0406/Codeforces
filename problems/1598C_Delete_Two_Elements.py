#https://codeforces.com/problemset/problem/1598/C
#unsolved
#reason: "due to TLE on test 4"

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    sumx = sum(arr)
    mean = sumx / n
    ans = 0
    for i in range(n):
        for j in range(i+1, n):
            csum = arr[i] + arr[j]
            new_mean = (sumx-csum)/ (n-2)
            if new_mean == mean:
                ans += 1
    print(ans)