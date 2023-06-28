# 1516. 게임 개발

from collections import deque
import sys
input = sys.stdin.readline

n = int(input())
buildings = [[] for i in range(n + 1)]
time = [0 for i in range(n + 1)]
deg = [0 for i in range(n + 1)]
dp = [0 for i in range(n + 1)]

for i in range(1, n + 1):
    # 건물 정보 입력받기
    # 가장 첫 번째 원소는 해당 번호 건물의 건설 시간
    # 그 다음부터 -1 전까지는 해당 건물을 짓기 전에 건설되어야 하는 건물 번호
    ipt = list(map(int, input().split()))
    time[i] = ipt[0]
    for num in ipt[1:]:
        if num != -1:
            buildings[num].append(i)
            deg[i] += 1

que = deque()

# 초기에 진입 차수가 0인 건물을 찾아 큐에 넣고
# 최종 시간 리스트(dp)의 해당 원소를 건물 건설 시간으로 설정한다
for i in range(1, n + 1):
    if not deg[i]:
        que.append(i)
        dp[i] = time[i]

while que:
    now = que.popleft()
    for next_point in buildings[now]:
        deg[next_point] -= 1
        dp[next_point] = max(dp[now] + time[next_point], dp[next_point])
        if not deg[next_point]:
            que.append(next_point)

print(*dp[1:], sep='\n')