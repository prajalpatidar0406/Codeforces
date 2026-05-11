#https://codeforces.com/problemset/problem/1516/B
#unsolved
#reason: "Wrong answer on Test 4"

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    if len(set(arr)) == 1:
        print("YES")
    else:
        xorr = 0
        for ele in arr:
            xorr = xorr ^ ele
        ischeck = False
        for ele in arr:
            a = xorr ^ ele
            if a == ele:
                ischeck = True
                break
        if ischeck:
            print("YES")
        else:
            print("NO")