#https://codeforces.com/problemset/problem/706/B
import sys
from bisect import bisect_right
input = sys.stdin.readline

n = int(input())
shops = list(map(int, input().split()))
shops.sort()
q = int(input())
for _ in range(q):
    coins = int(input())
    print(bisect_right(shops,coins))

