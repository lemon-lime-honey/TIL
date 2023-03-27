# 14502. 연구소

from collections import deque
from copy import deepcopy
import sys

# 벽 세 개 세우고 BFS
def wall(wall_cnt):
    if wall_cnt == 3:
        bfs()
        return

    for i in range(n):
        for j in range(m):
            if not original_map[i][j]:
                original_map[i][j] = 1
                wall(wall_cnt + 1)
                original_map[i][j] = 0

# BFS
def bfs():
    wall_map = deepcopy(original_map)
    que = deque()

    for i in range(n):
        for j in range(m):
            if wall_map[i][j] == 2:
                que.append((i, j))
    
    while que:
        r, c = que.popleft()

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]

            if (0 <= nr < n) and (0 <= nc < m) and not wall_map[nr][nc]:
                wall_map[nr][nc] = 2
                que.append((nr, nc))
    
    global result
    cnt = 0

    # BFS를 수행할 때마다 바이러스로부터 안전한 구역의 수를 센 후 그 이전 값과 비교해 큰 값으로 유지
    for i in range(n):
        for j in range(m):
            if not wall_map[i][j]:
                cnt += 1
    
    result = max(cnt, result)

dr = [0, 0, -1, 1]
dc = [1, -1, 0, 0]

n, m = map(int, sys.stdin.readline().split())
original_map = [[] for i in range(n)]
result = 0

for i in range(n):
    original_map[i] = list(map(int, sys.stdin.readline().split()))

wall(0)
print(result)