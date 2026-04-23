#https://codeforces.com/problemset/problem/69/A

n = int(input())

sum_x, sum_y, sum_z = 0,0,0

for i in range(n):
    x, y , z = map(int, input().split())
    sum_x += x
    sum_y += y
    sum_z += z

if sum_x != 0 or sum_y != 0 or sum_z != 0:
    print("NO")
else:
    print("YES")