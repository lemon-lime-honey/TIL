import sys
input = sys.stdin.readline
INF = sys.maxsize

# 벨만-포드
def bellman_ford(start):
    route[start - 1] = 0
    for i in range(n):
        for j in range(m):
            point, next_point, cost = bus[j]
            if route[point - 1] != INF and route[point - 1] + cost < route[next_point - 1]:
                route[next_point - 1] = route[point - 1] + cost
                # (n - 1)번 돌고 난 후에도 값에 변화가 생긴다면 음수 사이클이 존재한다는 뜻
                if i == n - 1:
                    return True
    return False

n, m = map(int, input().split())
bus = [list(map(int, input().split())) for i in range(m)]
route = [INF for i in range(n)]

negative = bellman_ford(1)

# 시간을 무한히 오래 전으로 돌릴 수 있으면 -1을 출력한다
if negative: print(-1)
else:
    # 값이 INF이면 접근할 수 없는 곳이므로 -1을 출력한다
    # 아니면 해당 도시로 가는 가장 빠른 시간을 출력한다
    for i in range(1, n):
        if route[i] == INF: print(-1)
        else: print(route[i])