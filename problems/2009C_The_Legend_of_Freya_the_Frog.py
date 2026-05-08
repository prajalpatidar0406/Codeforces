#https://codeforces.com/problemset/problem/2009/C

t = int(input())
for _ in range(t):
    x, y, k = map(int, input().split())
    print(max(2*((x+k-1)//k) -1, 2*((y+k-1)//k)))