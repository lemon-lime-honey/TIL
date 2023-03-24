# 13549. 숨바꼭질 3

from collections import deque
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
graph = [int(1e9) for i in range(200001)]
graph[n] = 0
que = deque([n])

# 0-1 너비 우선 탐색
# 가중치가 0 또는 1로 주어졌을 때 사용할 수 있다
# 순간이동의 가중치가 0, -1 또는 +1 이동의 가중치가 1
# 가중치가 0이면 큐의 앞에, 1이면 큐의 뒤에 넣는다
while que:
    now = que.popleft()

    if 2 * now < 200001:
        if graph[now] < graph[2 * now]:
            graph[2 * now] = graph[now]
            que.appendleft(2 * now)
    if 0 <= (now - 1) < 200001:
        if graph[now] + 1 < graph[now - 1]:
            graph[now - 1] = graph[now] + 1
            que.append(now - 1)
    if 0 <= (now + 1) < 200001:
        if graph[now] + 1 < graph[now + 1]:
            graph[now + 1] = graph[now] + 1
            que.append(now + 1)

print(graph[k])