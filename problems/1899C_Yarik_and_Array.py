#https://codeforces.com/problemset/problem/1899/C

def check_same_parity(a, b):
    return (a%2 == b%2)

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    crr_sum = arr[0]
    max_sum = arr[0]
    for i in range(1,n):
        if check_same_parity(arr[i], arr[i-1]):
            crr_sum = arr[i]
        else:
            crr_sum += arr[i]
        crr_sum = max(crr_sum, arr[i])
        max_sum = max(max_sum, crr_sum)
    
    print(max_sum)