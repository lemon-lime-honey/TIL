# 1922. 네트워크 연결

import heapq, sys
input = sys.stdin.readline


# find 연산.
def find(p):
    if p != chk[p]:
        chk[p] = find(chk[p])
    return chk[p]


# union 연산
def union(p1, p2):
    p1, p2 = find(p1), find(p2)

    if p1 == p2: return
    if p1 < p2: chk[p2] = p1
    else: chk[p1] = p2


# 정보 입력
n = int(input())
m = int(input())
graph = [list(map(int, input().split())) for i in range(m)]
graph.sort(key=lambda x:x[2])
chk = [i for i in range(n + 1)]
result = 0

# 크루스칼 알고리즘
for a, b, c in graph:
    if find(a) != find(b):
        union(a, b)
        result += c

print(result)