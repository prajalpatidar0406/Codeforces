#https://codeforces.com/problemset/problem/1832/B

t = int(input())
for _ in range(t):
    n,k = map(int, input().split())
    arr = list(map(int, input().split()))
    arr.sort()
    crr_sum =  sum(arr[:-k])
    maxi_sum = crr_sum
    l = 0
    h = n-k
    for j in range(k):
        crr_sum = crr_sum - arr[l] - arr[l+1] + arr[h]
        l += 2
        h += 1
        maxi_sum = max(maxi_sum, crr_sum)
    
    print(maxi_sum)