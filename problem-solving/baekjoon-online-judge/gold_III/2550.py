from bisect import bisect_left
import sys
input = sys.stdin.readline

n = int(input())
switch = list(map(int, input().split()))
lamp = list(map(int, input().split()))
dp = [1 for i in range(n)]
cable = list()

# 연결 정보를 스위치와 램프의 번호가 아니라
# 위치를 기준으로 바꿔준다
for i in range(n):
    for j in range(n):
        if switch[i] == lamp[j]:
            cable.append(j)
            break

result = [cable[0]]

# 가장 긴 증가하는 부분 수열 구하기
for i in range(1, n):
    if result[-1] < cable[i]:
        result.append(cable[i])
        dp[i] = len(result)
    else:
        idx = bisect_left(result, cable[i])
        result[idx] = cable[i]
        dp[i] = idx + 1

ref = len(result)
answer = list()

# 리스트 dp를 역순으로 순회하며 배열을 구한다
# 이때 결과 리스트에 원소를 추가할 때 스위치의 번호를 넣는다
for i in range(n - 1, -1, -1):
    if ref == 0:
        break
    if dp[i] == ref:
        answer.append(switch[i])
        ref -= 1

print(len(result))
print(*answer[::-1])