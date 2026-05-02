#https://codeforces.com/problemset/problem/519/B

from collections import Counter
n = int(input())
a1 = Counter(map(int, input().split()))
a2 = Counter(map(int, input().split()))
a3 = Counter(map(int, input().split()))

print(*(a1-a2))
print(*(a2-a3))