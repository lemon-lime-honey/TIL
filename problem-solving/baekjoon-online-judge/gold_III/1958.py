# 1958. LCS 3

one = input()
two = input()
three = input()
dp = [[[0 for i in range(len(three) + 1)] for j in range(len(two) + 1)] for k in range(len(one) + 1)]

# 3차원 배열을 만들어 LCS의 길이를 구한다
# 2차원과 크게 다르지는 않지만 아래 else절 max 안에 들어가는 값이 누락되지 않도록 주의해야 한다
for i in range(len(one) - 1, -1, -1):
    for j in range(len(two) - 1, -1, -1):
        for k in range(len(three) - 1, -1, -1):
            if one[i] == two[j] == three[k]:
                dp[i][j][k] = dp[i + 1][j + 1][k + 1] + 1
            else:
                dp[i][j][k] = max(dp[i + 1][j][k], dp[i + 1][j + 1][k], 
                                  dp[i + 1][j][k + 1], dp[i][j + 1][k], 
                                  dp[i][j + 1][k + 1], dp[i][j][k + 1])

print(dp[0][0][0])