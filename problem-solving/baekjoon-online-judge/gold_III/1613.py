# 1613. 역사

import sys
input = sys.stdin.readline

n, k = map(int, input().split())
graph = [[int(1e9) for i in range(n)] for j in range(n)]
rev_graph = [[int(1e9) for i in range(n)] for j in range(n)]

for i in range(k):
    a, b = map(int, input().split())
    graph[a - 1][b - 1] = 1
    rev_graph[b - 1][a - 1] = 1

s = int(input())
question = [list(map(int, input().split())) for i in range(s)]

for i in range(n):
    graph[i][i] = 0
    rev_graph[i][i] = 0

# 플로이드-워셜
for i in range(n):
    for j in range(n):
        for k in range(n):
            graph[j][k] = min(graph[j][k], graph[j][i] + graph[i][k])
            rev_graph[j][k] = min(rev_graph[j][k], rev_graph[j][i] + rev_graph[i][k])

# 뒤집은 그래프와 뒤집지 않은 그래프에서 값에 변화가 있었다면 1과 -1을 출력하고
# 변화가 없으면 0을 출력한다
for element in question:
    front, end = element
    if graph[front - 1][end - 1] != int(1e9):
        print(-1)
    elif rev_graph[front - 1][end - 1] != int(1e9):
        print(1)
    else:
        print(0)