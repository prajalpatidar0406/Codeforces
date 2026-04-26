#https://codeforces.com/problemset/problem/706/B
#unsolved
#reason: "Time limit exceed on test 5"

n = int(input())
shops = list(map(int, input().split()))
shops.sort()
q = int(input())
for _ in range(q):
    coins = int(input())
    low = 0
    high = n -1
    # print(shops)
    while high > low:
        mid = (high - low)//2 + low
        if shops[mid] == coins:
            low = mid
            if shops[high] != coins:
                high -= 1
        elif shops[mid] > coins:
            high = mid
        else:
            low = mid+1
        # print(high,low,mid)
    
    if shops[high] <= coins:
        print(high + 1)
    elif high > 0:
        print(high)
    else:
        print(0)
    # print("__________")

