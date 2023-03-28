# 1719. 택배

import sys
input = sys.stdin.readline

n, m = map(int, input().split())
graph = [[1e9 for i in range(n)] for j in range(n)]
result = [[(i + 1) for i in range(n)] for j in range(n)]

for i in range(m):
    a, b, c = map(int, input().split())
    graph[a - 1][b - 1] = graph[b - 1][a - 1] = c

# 자기 자신으로 가는 경우 초기화
for i in range(n):
    graph[i][i] = 0
    result[i][i] = '-'

# 플로이드-워셜
# 값에 변화가 생겼을 때 2차원 배열 result에 직전 지점 갱신하기
for i in range(n):
    for j in range(n):
        for k in range(n):
            if (graph[j][i] + graph[i][k]) < graph[j][k]:
                graph[j][k] = graph[j][i] + graph[i][k]
                result[j][k] = result[j][i]

for i in range(n):
    print(*result[i])