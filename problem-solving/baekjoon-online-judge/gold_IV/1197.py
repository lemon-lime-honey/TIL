# 1197. 최소 스패닝 트리
# 크루스칼 알고리즘: 가장 적은 비용으로 모든 노드를 연결한다

import heapq, sys
input = sys.stdin.readline


# 유니온 파인드
def find(p):
    if p != chk[p]:
        chk[p] = find(chk[p])
    return chk[p]


def union(p1, p2):
    p1, p2 = find(p1), find(p2)

    if p1 == p2: return
    if p1 < p2: chk[p2] = p1
    else: chk[p1] = p2


v, e = map(int, input().split())
graph = [list(map(int, input().split())) for i in range(e)]
# 가중치를 기준으로 오름차순 정렬한다
graph.sort(key=lambda x:x[2])
chk = [i for i in range(v + 1)]
result = 0

# 가중치가 가장 작은 간선부터 간선 정보를 사용하여 노드를 연결한다
# 노드를 연결할 때에는 유니온 파인드 알고리즘을 사용하며,
# 유니온 연산을 할 때마다 결과값 변수에 가중치를 더한다
for a, b, c in graph:
    if find(a) != find(b):
        union(a, b)
        result += c

print(result)