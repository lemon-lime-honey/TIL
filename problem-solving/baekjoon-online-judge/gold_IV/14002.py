# 14002. 가장 긴 증가하는 부분 수열 4

n = int(input())
a = list(map(int, input().split()))
dp = [1] * n
result = list()

# 수열 a = {10, 20, 10, 30, 20, 50}
# i = 4일 때
#     j = 5, a[4] < a[5]이므로
#         dp[4] = max(dp[4], dp[5] + 1) = max(1, 2) = 2
# i = 3일 때
#     j = 4, a[3] > a[4]이므로 넘어감
#     j = 5, a[3] < a[5]이므로
#         dp[3] = max(dp[3], dp[5] + 1) = max(1, 2) = 2
# i = 2일 때
#     j = 3, a[2] < a[3]이므로
#         dp[2] = max(dp[2], dp[3] + 1) = max(1, 3) = 3
#     j = 4, a[2] < a[4]이므로
#         dp[2] = max(dp[2], dp[4] + 1) = max(3, 3) = 3
#     j = 5, a[2] < a[5]이므로
#         dp[2] = max(dp[2], dp[5] + 1) = max(3, 2) = 3
# i = 1일 때
#     j = 2, a[1] > a[2]이므로 넘어감
#     j = 3, a[1] < a[3]이므로
#         dp[1] = max(dp[1], dp[3] + 1) = max(1, 3) = 3
#     j = 4, a[1] == a[4]이므로 넘어감
#     j = 5, a[1] < a[5]이므로
#         dp[1] = max(dp[1], dp[5] + 1) = max(3, 2) = 3
# i = 0일 때
#     j = 1, a[0] < a[1]이므로
#         dp[0] = max(dp[0], dp[1] + 1) = max(1, 4) = 4
#     j = 2, a[0] == a[2]이므로 넘어감
#     j = 3, a[0] < a[3]이므로
#         dp[0] = max(dp[0], dp[3] + 1) = max(4, 3) = 4
#     j = 4, a[1] < a[4]이므로
#         dp[0] = max(dp[0], dp[4] + 1) = max(4, 3) = 4
#     j = 5, a[1] < a[5]이므로
#         dp[0] = max(dp[0], dp[5] + 1) = max(4, 2) = 4
# dp = [4, 3, 3, 2, 2, 1]
# 따라서 가장 긴 증가하는 부분 수열의 길이: 4
for i in range(n - 1, -1, -1):
    for j in range(i + 1, n):
        if a[i] < a[j]:
            dp[i] = max(dp[i], dp[j] + 1)

answer = max(dp)
print(answer)

# 배열 dp에서 값이 줄어드는 부분의 인덱스를 가진 수열 a의 원소를 추가한다
for i in range(n):
    if dp[i] == answer:
        result.append(a[i])
        answer -= 1

print(*result)