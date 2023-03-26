# 11404. 플로이드

import sys
input = sys.stdin.readline

n = int(input())
m = int(input())
bus = [[int(1e9) for i in range(n)] for j in range(n)]

# 노선 정보 입력
for i in range(m):
    a, b, c = map(int, input().split())
    bus[a - 1][b - 1] = min(bus[a - 1][b - 1], c)

# 시작 도시와 도착 도시가 같을 때에는 이동할 필요가 없어 비용이 0이다
for i in range(n):
    bus[i][i] = 0

# 플로이드-워셜
for i in range(n):
    for j in range(n):
        for k in range(n):
            bus[j][k] = min(bus[j][k], bus[j][i] + bus[i][k])

# 갈 수 없는 경우: 0으로 변경해준다
for i in range(n):
    for j in range(n):
        if bus[i][j] == int(1e9):
            bus[i][j] = 0

for element in bus:
    print(*element)