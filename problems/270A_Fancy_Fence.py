#https://codeforces.com/problemset/problem/270/A

t = int(input())
for _ in range(t):
    angle = int(input())
    ext = 180 - angle
    sides = 360 / ext
    if sides < 3 or int(sides) != sides:
        print("NO")
    else:
        print("YES")