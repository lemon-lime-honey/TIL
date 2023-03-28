# 14442. 벽 부수고 이동하기 2

from collections import deque
import sys
input = sys.stdin.readline

def bfs():
    result = [[[0 for i in range(k + 1)] for j in range(m)] for l in range(n)]
    que = deque([[0, 0, 0]])
    result[0][0][0] = 1

    # BFS
    # 2206. 벽 부수고 이동하기와 비슷하다
    while que:
        r, c, h = que.popleft()
        if r == n - 1 and c == m - 1:
            return result[r][c][h]

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if (0 <= nr < n) and (0 <= nc < m):
                # 벽을 부수지 않고도 진행할 수 있는 경우
                if not graph[nr][nc] and not result[nr][nc][h]:
                    result[nr][nc][h] = result[r][c][h] + 1
                    que.append([nr, nc, h])
                # 벽을 부수면 진행할 수 있는 경우
                # result[nr][nc][h + 1]을 확인하는 부분이 있어야 한다
                elif graph[nr][nc] and (h < k) and not result[nr][nc][h + 1]:
                    result[nr][nc][h + 1] = result[r][c][h] + 1
                    que.append([nr, nc, h + 1])
    
    return -1

dr = [0, 0, -1, 1]
dc = [1, -1, 0, 0]

n, m, k = map(int, input().split())
graph = [list(map(int, input().rstrip())) for i in range(n)]
print(bfs())