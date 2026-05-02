#https://codeforces.com/problemset/problem/467/B

n,m,k = map(int, input().split())
arr = []
for _ in range(m):
    arr.append(int(input()))
player = int(input())
count = 0
for i in arr:
    diff = player ^ i
    count += diff.bit_count() <= k
print(count)