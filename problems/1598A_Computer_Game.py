#https://codeforces.com/problemset/problem/1598/A

def solve(n, r1, r2):
    if r1[0] == "1" or r2[-1] == "1":
        return False
    for i in range(n):
        if r1[i] == "1" and r2[i] == "1":
            return False
    return True

t = int(input())
for _ in range(t):
    n = int(input())
    r1 = input()
    r2 = input()
    print("YES" if solve(n, r1, r2) else "NO")