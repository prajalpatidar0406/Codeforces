#https://codeforces.com/problemset/problem/58/A

import re

s = input()
hello = ".*".join(re.escape(x) for x in "hello")
if re.search(hello, s):
    print("YES")
else:
    print("NO")