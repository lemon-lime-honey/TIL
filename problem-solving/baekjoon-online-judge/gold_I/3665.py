# 3665. 최종 순위

import sys
from collections import deque
input = sys.stdin.readline

t = int(input())

for i in range(t):
    n = int(input())
    last = list(map(int, input().split()))
    graph = [[] for j in range(n + 1)]
    chk = [0 for j in range(n + 1)]
    result = list()
    que = deque()

    # 작년 상황에서의 간선과 진입차수
    for j in range(n):
        graph[last[j]] = last[j + 1:]
        chk[last[j]] = j
    
    m = int(input())

    # 올해 상황 추가
    for j in range(m):
        a, b = map(int, input().split())
        if a in graph[b]:
            graph[b].remove(a)
            chk[a] -= 1
            graph[a].append(b)
            chk[b] += 1
        else:
            graph[a].remove(b)
            chk[b] -= 1
            graph[b].append(a)
            chk[a] += 1

    # 진입차수가 0인 원소 찾아 큐에 추가하기
    for j in range(1, n + 1):
        if chk[j] == 0:
            que.append(j)

    # 큐가 비어 있는 경우 사이클 존재
    # IMPOSSIBLE 출력
    if not que:
        print("IMPOSSIBLE")
        continue

    # 위상정렬
    while que:
        now = que.popleft()
        result.append(now)
        for element in graph[now]:
            chk[element] -= 1
            if chk[element] == 0:
                que.append(element)

    if len(result) < n:
        print('IMPOSSIBLE')
    else:
        print(*result)