# 14938. 서강그라운드

import sys
input = sys.stdin.readline

n, m, r = map(int, input().split())
field = [[int(1e9) for i in range(n)] for j in range(n)]
t = list(map(int, input().split()))
result = 0

# 경로 입력
for i in range(r):
    r, b, l = map(int, input().split())
    field[r - 1][b - 1] = field[b - 1][r - 1] = l

for i in range(n):
    field[i][i] = 0

# 플로이드-워셜
for i in range(n):
    for j in range(n):
        for k in range(n):
            field[j][k] = min(field[j][k], field[j][i] + field[i][k])

# 각 시작위치마다 그 위치로부터 수색범위인 m까지 갈 수 있는 구역에 있는 아이템의 수를 구한다
for i in range(n):
    chk = 0
    for j in range(n):
        if field[i][j] <= m:
            chk += t[j]
    result = max(result, chk)

print(result)