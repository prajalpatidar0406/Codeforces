#https://codeforces.com/problemset/problem/224/A

import math
a, b, c = map(int, input().split())
x = math.sqrt((a*b)/c)
y = math.sqrt((a*c)/b)
z = math.sqrt((c*b)/a)
print(4*int(x+y+z))