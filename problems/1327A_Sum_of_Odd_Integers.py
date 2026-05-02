#https://codeforces.com/problemset/problem/1327/A

t = int(input())
for _ in range(t):
    n,k = map(int, input().split())
    iss = True
    if n >= k**2:
        iss = (k%2 == 1) if n%2 ==1 else (k%2 == 0)
    else:
        iss = False
    print("YES" if iss else "NO")
