# 1865. 웜홀

import sys
input = sys.stdin.readline
INF = sys.maxsize

# 벨만-포드
def bellman_ford(start):
    result[start - 1] = 0

    for i in range(n):
        for j in range(len(way)):
            s, e, t = way[j]
            if result[s - 1] + t < result[e - 1]:
                result[e - 1] = result[s - 1] + t
                # n - 1번 순회한 후 n번째에도 값에 변화가 생기면
                # 음수 사이클이 존재한다는 뜻
                # True를 반환한다
                if i == (n - 1):
                    return True
    # 음수 사이클이 없으니 False를 반환한다
    return False

tc = int(input())

for i in range(tc):
    n, m, w = map(int, input().split())
    result = [INF for j in range(n)]
    way = list()

    for j in range(m):
        s, e, t = map(int, input().split())
        way.append((s, e, t))
        way.append((e, s, t))

    for j in range(w):
        s, e, t = map(int, input().split())
        way.append((s, e, -1 * t))

    chk = bellman_ford(1)

    if chk: print('YES')
    else: print('NO')