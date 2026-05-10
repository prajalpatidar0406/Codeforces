#https://codeforces.com/problemset/problem/919/B
#unsolved
#reason: "due to TLE"

def check(n):
    sum = 0
    while n > 0:
        sum += n%10
        n //= 10
    return sum == 10

k = int(input())
cnt = 1
num = 19
while cnt < k:
    num += 1
    if check(num):
        cnt += 1

print(num)