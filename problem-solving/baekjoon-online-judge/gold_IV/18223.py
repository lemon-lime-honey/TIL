# 18223. 민준이와 마산 그리고 건우

import sys, heapq
input = sys.stdin.readline
INF = sys.maxsize

def dijkstra(start):
    result = [INF for i in range(v)]
    result[start] = 0
    que = [(0, start)]
    while que:
        cost, point = heapq.heappop(que)
        if result[point] < cost: continue
        for next_cost, next_point in graph[point]:
            if cost + next_cost < result[next_point]:
                result[next_point] = cost + next_cost
                heapq.heappush(que, (cost + next_cost, next_point))
    return result

v, e, p = map(int, input().split())
graph = [[] for i in range(v)]

for i in range(e):
    a, b, c = map(int, input().split())
    graph[a - 1].append((c, b - 1))
    graph[b - 1].append((c, a - 1))

# 출발지점과 각 지점 사이의 최단 거리 구하기
one = dijkstra(0)
# 건우가 있는 지점부터 각 지점 사이의 최단 거리 구하기
two = dijkstra(p - 1)

# 최단경로로 움직일 때 건우가 있는 지점을 지난다면 SAVE HIM
if one[p - 1] + two[-1] == one[-1]:
    print('SAVE HIM')
# 지나지 않는다면 GOOD BYE
else:
    print('GOOD BYE')