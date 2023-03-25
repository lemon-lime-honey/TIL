# 11779. 최소비용 구하기 2

import sys, heapq
input = sys.stdin.readline

n = int(input())
m = int(input())
bus = [[] for i in range(n + 1)]
result = [int(1e9)] * (n + 1)

for i in range(m):
    start, end, cost = map(int, input().split())
    bus[start].append((cost, end))

initial, final = map(int, input().split())
points = [initial] * (n + 1)
que = [(0, initial)]

# 다익스트라
while que:
    length, point = heapq.heappop(que)

    if length > result[point]: continue

    for next_length, next_point in bus[point]:
        if length + next_length < result[next_point]:
            heapq.heappush(que, (length + next_length, next_point))
            result[next_point] = length + next_length
            points[next_point] = point

route = list()
temp = final

# 경로 구하기
while temp != initial:
    route.append(temp)
    temp = points[temp]

route.append(initial)

print(result[final])
print(len(route))
print(*route[::-1])