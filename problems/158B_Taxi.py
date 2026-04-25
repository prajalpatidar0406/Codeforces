#https://codeforces.com/problemset/problem/158/B

n = int(input())
arr = list(map(int, input().split()))
arr.sort()
i = 0
j = n -1
cnt = 0
while i <= j:
    if i == j:
        i +=1
        cnt += 1
    elif arr[i] + arr[j] <= 4:
        arr[j] += arr[i]
        i += 1
    else:
        j -= 1
        cnt += 1

print(cnt)