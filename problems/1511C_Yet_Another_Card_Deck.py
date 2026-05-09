#https://codeforces.com/problemset/problem/1511/C
#unsolved
#reason: "due to time limit exceed"

import sys
input = sys.stdin.readline

n, q = map(int, input().split())
arr = list(map(int, input().split()))
queries = list(map(int, input().split()))
mp = [-1] * 51
cnt = 0
for i in range(n):
    if mp[arr[i]] == -1:
        mp[arr[i]] = i+1
        cnt += 1
    if cnt == 50:
        break
ans = []
for i in range(q):
    idx = mp[queries[i]]
    ans.append(str(idx))
    for j in range(1,51):
        if mp[j] != -1 and mp[j] < idx:
            mp[j] += 1
    mp[queries[i]] = 1
print(' '.join(ans))

