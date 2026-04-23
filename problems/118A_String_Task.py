#https://codeforces.com/problemset/problem/118/A

s = input()

s = s.lower()
ans = []
for i in s:
    if i  in {'a', 'e', 'i', 'o', 'u', 'y'}:
        continue
    else:
        ans.append(f'.{i}')
s = "".join(ans)
print(s)