#https://codeforces.com/problemset/problem/1490/C

import math

t = int(input())
for _ in range(t):
    x = int(input())
    h = math.ceil(math.cbrt(x))
    iss = False
    for a in range(h,0,-1):

        b3 = x - (a*a*a)
        if b3 > 0:
            b = math.cbrt(b3)
            b_int= int(b)
            if b_int == b:
                iss = True
                break
    
    print("YES" if iss else "NO")