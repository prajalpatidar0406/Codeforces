#https://codeforces.com/problemset/problem/1999/D

t = int(input())
for _ in range(t):
    s = list(input())
    x = input()
    xl, sl = 0, 0
    xh, sh = len(x), len(s)

    while xl < xh and sl < sh :
        if s[sl] == "?":
            s[sl] = x[xl]
        if(s[sl] == x[xl]):
            xl += 1
            sl += 1
        else:
            sl += 1
    
    if xl >= xh:
        ans = "".join(["a" if x == "?"  else x for x in s])
        print("YES")
        print(ans)
    else:
        print("NO")