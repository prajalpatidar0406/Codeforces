#https://codeforces.com/problemset/problem/1366/A

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(min(a, b, (a+b)//3))