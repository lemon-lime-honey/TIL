# 13913. 숨바꼭질 4

from collections import deque

n, k = map(int, input().split())
visited = [-1 for i in range(200001)]
before = [-1 for i in range(200001)]
que = deque([n])
visited[n] = 0
route = [k]

while que:
    point = que.popleft()
    for next_point in (point - 1, point + 1, 2 * point):
        if 0 <= next_point < 200001:
            if visited[next_point] == -1:
                visited[next_point] = visited[point] + 1
                # 직전 지점을 저장한다
                before[next_point] = point
                que.append(next_point)

# 경로 찾기
while True:
    temp = before[route[-1]]
    if temp == -1: break
    route.append(before[route[-1]])

print(visited[k])
print(*route[::-1])