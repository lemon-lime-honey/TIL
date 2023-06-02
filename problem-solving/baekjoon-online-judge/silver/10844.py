# 10844. 쉬운 계단 수

n = int(input())

dp = [[0 for i in range(10)] for j in range(n)]

# 가장 큰 자리수에는 0이 올 수 없다
for i in range(1, 10):
    dp[0][i] = 1

# i: 자리 수
# j: 0부터 9까지의 숫자
for i in range(1, n):
    for j in range(10):
        if j == 0:
            dp[i][j] = dp[i - 1][1]
        elif j == 9:
            dp[i][j] = dp[i - 1][8]
        else:
            dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j + 1]

print(sum(dp[-1]) % 1000000000)