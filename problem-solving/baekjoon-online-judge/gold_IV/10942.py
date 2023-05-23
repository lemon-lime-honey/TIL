# 10942. 팰린드롬?

import sys
input = sys.stdin.readline

n = int(input())
numbers = list(map(int, input().split()))
dp = [[0 for i in range(n)] for j in range(n)]
m = int(input())

# 길이가 1이면 팰린드롬
for i in range(n):
    dp[i][i] = 1

# 길이가 2이면 서로 같을 때 팰린드롬
for i in range(n - 1):
    if numbers[i] == numbers[i + 1]:
        dp[i][i + 1] = 1

# 나머지 경우
# i가 길이라고 하자
for i in range(2, n): 
    for j in range(n - i):
        k = j + i
        if numbers[j] == numbers[k] and dp[j + 1][k - 1]:
            dp[j][k] = 1

for i in range(m):
    s, e = map(int, input().split())
    print(dp[s - 1][e - 1])