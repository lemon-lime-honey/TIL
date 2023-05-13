# 2252. 줄 세우기
# 위상정렬

import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())
graph = [[] for i in range(n + 1)]
chk = [0 for i in range(n + 1)]
result = list()
que = deque()

# 그래프 정보 추가
# 추가할 때마다 노드의 진입차수를 1씩 더해준다
for i in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    chk[b] += 1

# 진입차수가 0인 노드를 큐에 추가한다
for i in range(1, n + 1):
    if chk[i] == 0:
        que.append(i)

while que:
    # 큐를 순회하며 원소를 뺄 때마다 결과 리스트에 추가한다
    temp = que.popleft()
    result.append(temp)

    # 큐에서 뺀 원소에 연결된 노드를 순회하며
    # 그 노드의 진입차수를 1씩 빼준다
    # 그리고 노드의 진입차수가 0이 되었다면
    # 큐에 추가한다
    for target in graph[temp]:
        chk[target] -= 1
        if chk[target] == 0:
            que.append(target)

print(*result)