#https://codeforces.com/problemset/problem/1598/B
#unsolved
#reason: "Wrong answer on test 2"

from collections import defaultdict
t = int(input())
for _ in range(t):
    n = int(input())
    mp = defaultdict(list)
    for i in range (n):
        week_data = list(map(int, input().split()))
        for j in range(5):
            if week_data[j] == 1:
                mp[j].append(i)
    
    keys = list(mp.keys())
    solvable = False
    for i in keys:
        if solvable:
            break
        for j in keys:
            if i == j:
                continue
            v1 = set(mp[i])
            v2 = set(mp[j])
            x1 = v1 - v2
            x2 = v2 - v1
            x1l, v1l, x2l, v2l = len(x1), len(v1), len(x2), len(v2)
            if (x1l + v2l) == n or (x2l + v1l) == n:
                solvable = True
                break
    
    print("YES" if solvable else "NO")
