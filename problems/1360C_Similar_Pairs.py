#https://codeforces.com/problemset/problem/1360/C

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    arr.sort()
    ec = 0
    iscc = False
    if arr[0]%2 == 0:
        ec += 1
    for i in range(1,n):
        if arr[i]%2 == 0:
            ec += 1
        if arr[i] - arr[i-1] == 1:
            iscc = True
    
    if ec%2 != 0 and not iscc:
        print("NO")
    else:
        print("YES")