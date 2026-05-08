#https://codeforces.com/problemset/problem/1899/B

import math
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    divs = []
    for x in range(1, int(math.sqrt(n)) + 1):
        if n%x == 0:
            divs.append(x)
            z = n//x
            if z != x:
                divs.append(z)
    ans = 0
    for x in divs:
        maxi = 0
        mini = 1e63-1
        for i in range(0, n, x):
            sumx= sum(arr[i:i+x])
            maxi = max(maxi, sumx)
            mini = min(mini, sumx)
        ans = max(ans, maxi-mini)
    print(ans)
        
