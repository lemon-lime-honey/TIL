# 2638. 치즈

from collections import deque


dr = [0, 0, 1, -1]
dc = [1, -1, 0, 0]


def bfs():
    que = deque()
    que.append([0, 0])
    visited[0][0] = True
    while que:
        r, c = que.popleft()
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if (0 <= nr < n) and (0 <= nc < m) and not visited[nr][nc]:
                # 바깥 공기
                if cheese[nr][nc] == 0:
                    visited[nr][nc] = True
                    que.append([nr, nc])
                # 치즈가 바깥 공기에 닿을 때마다 1을 더해준다
                # 결국 bfs를 한 번 진행했을 때 공기에 닿은 칸의 값은 (변 + 1)이다
                else:
                    cheese[nr][nc] += 1


n, m = map(int, input().split())
cheese = [list(map(int, input().split())) for i in range(n)]
time = 0

while True:
    visited = [[False for i in range(m)] for j in range(n)]
    chk = False
    bfs()
    for i in range(n):
        for j in range(m):
            # 치즈의 두 변 이상에 공기가 닿으면 녹는다
            if cheese[i][j] > 2:
                cheese[i][j] = 0
            # 그 외의 경우에는 다시 1로 되돌린다
            elif cheese[i][j] > 0:
                cheese[i][j] = 1
                chk = True
    time += 1
    # 치즈가 하나도 남지 않으면 break
    if not chk: break

print(time)