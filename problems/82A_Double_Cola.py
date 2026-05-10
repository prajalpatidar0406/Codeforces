#https://codeforces.com/problemset/problem/82/A

import math

n = int(input())
idx = math.log2(n/5 + 1)
fi = math.floor(idx)
val = 5 * (pow(2,fi) - 1)
diff = n - val
pos = math.ceil(diff/pow(2,fi))
match pos:
    case 1:
        print("Sheldon")
    case 2:
        print("Leonard")
    case 3:
        print("Penny")
    case 4:
        print("Rajesh")
    case _:
        print("Howard")
