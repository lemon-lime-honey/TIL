# 2636. 치즈

from collections import deque


dr = [0, 0, 1, -1]
dc = [1, -1, 0, 0]


def bfs():
    que = deque()
    que.append([0, 0])
    visited[0][0] = True
    cnt = 0
    while que:
        r, c = que.popleft()
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if (0 <= nr < n) and (0 <= nc < m) and not visited[nr][nc]:
                # 바깥 공기
                if cheese[nr][nc] == 0:
                    visited[nr][nc] = True
                    que.append([nr, nc])
                # 바깥 공기와 닿은 치즈
                else:
                    visited[nr][nc] = True
                    cheese[nr][nc] = 0
                    cnt += 1
    # 치즈 조각이 놓여있는 칸의 개수
    cnts.append(cnt)
    return cnt


n, m = map(int, input().split())
cheese = [list(map(int, input().split())) for i in range(n)]
cnts = list()
time = 0

while True:
    visited = [[False for i in range(m)] for j in range(n)]
    cnt = bfs()
    # 치즈가 남아있지 않으면 break
    if not cnt: break
    # 치즈가 남아있으면 시간을 한 시간 더한다
    time += 1

# cnts[-1]은 0이다
print(time, cnts[-2], sep='\n')