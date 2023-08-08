# 2573. 빙산

from collections import deque
from copy import deepcopy
import sys
input = sys.stdin.readline


dr = [0, 0, -1, 1]
dc = [1, -1, 0, 0]


# 배열을 순회하며 빙산의 높이를 갱신하고
# 최종 결과를 다시 배열에 저장한다
def melt(targets):
    global maps

    result = deepcopy(maps)
    for row, col in targets:
        que = deque([(row, col)])
        while que:
            r, c = que.popleft()
            cnt = 0
            for i in range(4):
                nr, nc = r + dr[i], c + dc[i]
                if (0 <= nr < n) and (0 <= nc < m) and not maps[nr][nc]:
                    cnt += 1
            if cnt:
                result[r][c] -= cnt
                if result[r][c] < 0: result[r][c] = 0

    maps = result


n, m = map(int, input().split())
maps = [list(map(int, input().split())) for i in range(n)]
time = 0

# 빙산이 두 덩어리 이상으로 분리되거나 다 녹을 때까지 반복해서
# 빙산의 개수를 세고 시간을 더하고 빙산의 높이를 갱신한다
while True:
    glacier = list()
    que = deque()
    visited = [[False for i in range(m)] for j in range(n)]
    chk = 0
    for i in range(n):
        for j in range(m):
            if maps[i][j]:
                glacier.append((i, j))
                if not visited[i][j]:
                    que.append((i, j))
                    visited[i][j] = True
                    while que:
                        r, c = que.popleft()
                        for k in range(4):
                            nr, nc = r + dr[k], c + dc[k]
                            if (0 <= nr < n) and (0 <= nc < m):
                                if not visited[nr][nc] and maps[nr][nc]:
                                    visited[nr][nc] = True
                                    que.append((nr, nc))
                    chk += 1
    if not glacier:
        print(0)
        break
    if chk > 1:
        print(time)
        break
    time += 1
    melt(glacier)