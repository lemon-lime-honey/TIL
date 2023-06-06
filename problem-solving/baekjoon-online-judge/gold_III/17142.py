# 17142. 연구소 3

from collections import deque
from itertools import combinations
import sys
input = sys.stdin.readline


dr = [0, 0, 1, -1]
dc = [1, -1, 0, 0]


def bfs(v):
    que = deque()
    visited = [[-1 for i in range(n)] for j in range(n)]

    for r, c in v:
        que.append((r, c))
        visited[r][c] = 0
    
    time = 0
    chk = 0

    while que:
        r, c = que.popleft()
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if (0 <= nr < n) and (0 <= nc < n):
                # 방문한 적 없는 빈 칸
                if not lab[nr][nc] and visited[nr][nc] == -1:
                    que.append((nr, nc))
                    visited[nr][nc] = visited[r][c] + 1
                    # 시간 최대값으로 갱신
                    time = max(time, visited[nr][nc])
                # 비활성 바이러스 활성화
                elif lab[nr][nc] == 2 and visited[nr][nc] == -1:
                    que.append((nr, nc))
                    visited[nr][nc] = visited[r][c] + 1

    # 방문하지 않은 지점의 수 세기
    for i in range(n):
        for j in range(n):
            if visited[i][j] == -1:
                chk += 1

    # 방문하지 않은 지점의 수가 벽의 수와 같으면
    # 소요 시간 반환
    if wall == chk:
        return time
    # 다르면 1,000,000,000 반환
    else:
        return int(1e9)


n, m = map(int, input().split())
virus = list()
lab = list()
wall = 0

# 정보 입력
# 2일 때 바이러스 리스트에 좌표 추가
# 1일 때 벽의 개수에 1 더하기
for i in range(n):
    lab.append(list(map(int, input().split())))
    for j in range(n):
        if lab[i][j] == 2:
            virus.append((i, j))
        elif lab[i][j] == 1:
            wall += 1

# 바이러스 리스트 중 m개를 뽑는 조합의 리스트
virus = list(combinations(virus, m))
result = int(1e9)

# 최소 소요 시간 구하기
for v in virus:
    result = min(result, bfs(v))

print(-1 if result == int(1e9) else result)