# 13424. 비밀 모임
# 원작에서는 8층(구 번역 기준 7층)의 트롤에게 춤을 가르치는
# 바너버스(구 번역 바르나바) 태피스트리 앞 필요의 방에서 D.A. 모임을 가진다
# 엄브릿지 너무 싫다

import sys
input = sys.stdin.readline
INF = sys.maxsize

t = int(input())

for i in range(t):
    n, m = map(int, input().split())
    way = [[INF for j in range(n)] for k in range(n)]

    # 양방향 경로
    for j in range(m):
        a, b, c = map(int, input().split())
        way[a - 1][b - 1] = c
        way[b - 1][a - 1] = c

    # 한 지점에서 그 지점으로 가는 데에는 비용이 필요하지 않다
    for j in range(n):
        way[j][j] = 0

    # 플로이드-워셜
    for j in range(n):
        for k in range(n):
            for l in range(n):
                if way[k][j] + way[j][l] < way[k][l]:
                    way[k][l] = way[k][j] + way[j][l]

    k = int(input())
    member = list(map(int, input().split()))
    result = [0 for j in range(n)]

    # D.A. 회원들의 이동 거리의 총합이 최소가 되는 장소 찾기
    for j in range(k):
        for l in range(n):
            result[l] += way[member[j] - 1][l]

    print(result.index(min(result)) + 1)