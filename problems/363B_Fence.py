#https://codeforces.com/problemset/problem/363/B

n,k = map(int, input().split())
arr = list(map(int, input().split()))

min_sum = sum(arr[:k])
idx = 0
sum = min_sum
for j in range(k,n):
    sum = sum - arr[j-k] + arr[j]
    if min_sum > sum:
        idx = j-k + 1
        min_sum = sum

print(idx+1)
    

