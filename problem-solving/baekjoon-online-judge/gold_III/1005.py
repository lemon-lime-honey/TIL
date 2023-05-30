# 1005. ACM Craft

from collections import deque
import sys
input = sys.stdin.readline

t = int(input())

for i in range(t):
    n, k = map(int, input().split())
    # 건설 소요 시간
    time = [0] + list(map(int, input().split()))
    # 건설 순서
    building = [[] for j in range(n + 1)]
    # 진입차수
    deg = [0 for j in range(n + 1)]
    dp = [0 for j in range(n + 1)]

    for j in range(k):
        x, y = map(int, input().split())
        building[x].append(y)
        deg[y] += 1

    # 승리 조건
    w = int(input())

    que = deque()
    for j in range(1, n + 1):
        # 진입차수가 0인 건물 번호를 큐에 넣는다
        # 리스트 dp의 해당하는 원소 값을 해당 건물 건설 소요 시간으로 설정한다
        if deg[j] == 0:
            que.append(j)
            dp[j] = time[j]

    while que:
        now = que.popleft()
        for next_point in building[now]:
            # 다음 건물의 진입차수를 1 뺀 후
            # 리스트 dp의 다음 건물에 해당하는 원소 값을
            # 현재 건물 건설까지 걸린 소요 시간 + 다음 건물 건설 소요 시간과
            # 다음 건물 건설 소요 시간 중 더 큰 것으로 설정한다
            deg[next_point] -= 1
            dp[next_point] = max(dp[now] + time[next_point], dp[next_point])
            # 다음 건물의 진입차수가 0이라면 큐에 다음 건물 번호를 넣는다
            if deg[next_point] == 0:
                que.append(next_point)

    print(dp[w])