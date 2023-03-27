# 1504. 특정한 최단 경로

import sys, heapq
input = sys.stdin.readline

# 다익스트라
def dijkstra(start):
    distance = [int(1e9) for i in range(n + 1)]
    que = list()
    heapq.heappush(que, (0, start))
    distance[start] = 0

    while que:
        length, point = heapq.heappop(que)

        if length > distance[point]: continue
        for element in graph[point]:
            next_length, next_point = element
            if length + next_length < distance[next_point]:
                distance[next_point] = length + next_length
                heapq.heappush(que, (length + next_length, next_point))
    
    return distance

n, e = map(int, input().split())
graph = [[] for i in range(n + 1)]

# 경로 정보 입력
# 도착지와 거리를 묶을 때 거리 c가 앞으로 와야한다
# 양방향 간선이므로 양쪽 모두 간선 정보를 입력한다
for i in range(e):
    a, b, c = map(int, input().split())
    graph[a].append((c, b))
    graph[b].append((c, a))

one, two = map(int, input().split())

# 출발지, 경유지1, 경유지2에서 함수를 사용한다
front = dijkstra(1)
middle = dijkstra(one)
back = dijkstra(two)

# 출발지 ~ 경유지1, 경유지1 ~ 경유지2, 경유지2 ~ 도착지 중 어느 하나라도 경로가 존재하지 않는 경우
if front[one] == int(1e9) or middle[two] == int(1e9) or back[n] == int(1e9):
    print(-1)
else:
    # (출발지 ~ 경유지2) + (경유지2 ~ 경유지1) + (경유지1 ~ 도착지)가 더 빠른 경우
    if (front[two] + middle[two] + middle[n]) < (front[one] + middle[two] + back[n]):
        print(front[two] + middle[two] + middle[n])
    # (출발지 ~ 경유지1) + (경유지1 ~ 경유지2) + (경유지2 ~ 도착지)가 더 빠른 경우
    else:
        print(front[one] + middle[two] + back[n])