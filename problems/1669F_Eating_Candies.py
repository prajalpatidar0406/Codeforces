#https://codeforces.com/problemset/problem/1669/F

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    l = 0
    h = n-1
    ans = 0
    suml, sumr = arr[0], arr[-1]
    while(l < h):
        if suml == sumr:
            ans = l + 1 + (n-h)
            l += 1
            h -= 1
            suml += arr[l]
            sumr += arr[h]
        elif suml > sumr:
            h -= 1
            sumr += arr[h]
        else:
            l += 1
            suml += arr[l]
    
    print(ans)