# 10282. 해킹

import sys, heapq
input = sys.stdin.readline

t = int(input())

for i in range(t):
    n, d, c = map(int, input().split())
    computer = [[] for j in range(n)]
    result = [int(1e9) for j in range(n)]
    result[c - 1] = 0
    que = [(0, c - 1)]

    for j in range(d):
        a, b, s = map(int, input().split())
        computer[b - 1].append((s, a - 1))

    # 다익스트라
    while que:
        cost, point = heapq.heappop(que)

        for next_cost, next_point in computer[point]:
            if cost + next_cost < result[next_point]:
                result[next_point] = cost + next_cost
                heapq.heappush(que, (cost + next_cost, next_point))
    
    time = 0
    cnt = 0

    # 감염되는 컴퓨터의 수와 마지막 컴퓨터가 감염되기까지 걸리는 시간 구하기
    for j in range(n):
        if result[j] != int(1e9):
            time = max(time, result[j])
            cnt += 1
    
    print(cnt, time)