#https://codeforces.com/problemset/problem/456/A

n = int(input())
arr = []
for _ in range(n):
    a,b = map(int, input().split())
    arr.append((a,b))
arr.sort()
Alex = False
for i in range(0, n-1):
    if arr[i][0] < arr[i+1][0] and arr[i][1] > arr[i+1][1]:
        Alex = True

if Alex:
    print("Happy Alex")
else:
    print("Poor Alex")
