# 1238. 파티

import sys, heapq
input = sys.stdin.readline

# 다익스트라
# rev = True일 때 rev_road
# rev = False일 때 road
def dijkstra(rev):
    result = [int]
    result = [int(1e9) for i in range(n + 1)]
    result[x] = 0
    que = [x]
    
    if rev:
        while que:
            point = heapq.heappop(que)

            for next_time, next_point in rev_road[point]:
                if result[point] + next_time < result[next_point]:
                    result[next_point] = result[point] + next_time
                    heapq.heappush(que, next_point)
    else:
        while que:
            point = heapq.heappop(que)

            for next_time, next_point in road[point]:
                if result[point] + next_time < result[next_point]:
                    result[next_point] = result[point] + next_time
                    heapq.heappush(que, next_point)
    
    return result

n, m, x = map(int, input().split())
road = [[] for i in range(n + 1)]
rev_road = [[] for i in range(n + 1)]

# 도로 정보를 그대로(rev = False) 받거나 뒤집어서(rev = True) 받거나
for i in range(m):
    start, end, cost = map(int, input().split())
    road[start].append((cost, end))
    rev_road[end].append((cost, start))

first = dijkstra(True)
second = dijkstra(False)
answer = 0

# 최대 이동 시간을 구한다
for i in range(1, n + 1):
    temp = first[i] + second[i]
    answer = max(answer, temp)

print(answer)