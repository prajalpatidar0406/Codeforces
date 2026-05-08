#https://codeforces.com/problemset/problem/349/A

n = int(input())
sale = True
price = 25
arr = list(map(int, input().split()))
dp = [0, 0, 0] # 0th index 25-rupple count, 1st index 50-rupple count, 2nd index 100-rupple count
for bill in arr:
    diff = bill - price
    if diff == 25:
        if dp[0] > 0:
            dp[0] -= 1
        else:
            sale = False
            break
        dp[1] += 1
    elif diff == 75:
        if dp[1] > 0 and dp[0] > 0:
            dp[1] -= 1
            dp[0] -= 1
        elif dp[0] >= 3:
            dp[0] -= 3
        else:
            sale = False
            break
        dp[2] += 1
    else:
        dp[0] += 1

print("YES" if sale else "NO")