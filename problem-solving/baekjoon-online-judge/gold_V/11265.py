# 11265: 끝나지 않는 파티

import sys, heapq
input = sys.stdin.readline

n, m = map(int, input().split())
place = [list(map(int, input().split())) for i in range(n)]

# 플로이드-워셜
for i in range(n):
    for j in range(n):
        for k in range(n):
            if place[j][i] + place[i][k] < place[j][k]:
                place[j][k] = place[j][i] + place[i][k]

# 입력 받은 경로를 지나는데 걸리는 시간과 입력 받은 시간 비교
for i in range(m):
    a, b, c = map(int, input().split())
    if place[a - 1][b - 1] <= c:
        print('Enjoy other party')
    else:
        print('Stay here')