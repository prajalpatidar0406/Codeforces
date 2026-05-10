#https://codeforces.com/problemset/problem/227/B

from bisect import bisect_left
n = int(input())
arr = list(map(int, input().split()))
m = int(input())
queries = list(map(int, input().split()))
arr = sorted((value, index) for index, value in enumerate(arr))
vasya = 0
petya = 0
for q in queries:
    idx = bisect_left(arr, (q,))
    vasya += arr[idx][1] + 1
    petya += n - arr[idx][1]

print(vasya, petya)