#https://codeforces.com/problemset/problem/1791/E

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    cnt_ne = 0
    for i in arr:
        if i < 0:
            cnt_ne += 1
            
    brr = list(map(abs,arr))
    # print(brr)
    if cnt_ne%2 == 0:
        print(sum(brr))
    else:
        print(sum(brr) - (2*min(brr)))