# 17626. Four Squares

n = int(input())
dp = [0, 1]

for i in range(2, n + 1):
    minimum = int(1e9)
    # i에서 제곱수를 뺀 것의 dp 값 중 가장 작은 것을 찾는다
    for j in range(1, int(i ** 0.5) + 1):
        minimum = min(minimum, dp[i - (j ** 2)])
    # 찾은 수에 1을 더한 후 dp에 추가한다
    dp.append(minimum + 1)

print(dp[n])