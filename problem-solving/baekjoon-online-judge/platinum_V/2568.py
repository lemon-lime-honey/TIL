# 2568. 전깃줄 - 2

from bisect import bisect_left
import sys
input = sys.stdin.readline

n = int(input())
cables = list()
answer = set()

# 전깃줄 정보 입력
# 양 전신주의 위치를 튜플에 넣어 케이블 리스트에 추가한다
# answer set에 전깃줄이 연결된 전신주 A의 위치의 번호를 추가한다
for i in range(n):
    ipt = tuple(map(int, input().split()))
    cables.append(ipt)
    answer.add(ipt[0])

dp = [1 for i in range(n)]
result = list()
cables.sort()  # 전신주 A 기준으로 케이블 리스트를 정렬한다

# LIS 구하기
for i in range(n):
    start, end = cables[i]
    if not result:
        result.append(end)
    else:
        if result[-1] < end:
            result.append(end)
            dp[i] = len(result)
        else:
            chk = bisect_left(result, end)
            result[chk] = end
            dp[i] = chk + 1

# 없애야 하는 전깃줄의 최소 개수 출력
ref = len(result)
print(n - ref)

# 있어야 하는 전깃줄의 시작지점을 answer set에서 제거한다
for i in range(n - 1, -1, -1):
    if dp[i] == ref:
        answer.remove(cables[i][0])
        ref -= 1

# answer set을 리스트로 변환하고 정렬해 출력한다
answer = sorted(answer)
print(*answer, sep='\n')