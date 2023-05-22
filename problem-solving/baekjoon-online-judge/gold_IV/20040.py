# 20040. 사이클 게임

import sys
input = sys.stdin.readline


def find(p):
    if p != chk[p]:
        chk[p] = find(chk[p])
    return chk[p]


def union(p1, p2):
    p1, p2 = find(p1), find(p2)
    if p1 == p2:
        return True
    if p1 < p2: chk[p2] = p1
    else: chk[p1] = p2
    return False


n, m = map(int, input().split())
chk = [i for i in range(n)]
result = -1

for i in range(m):
    a, b = map(int, input().split())
    # 유니온 연산을 한다
    # 이미 연결이 된 경우 True, 아닌 경우 False 반환
    flag = union(a, b)
    # 이미 연결이 되어 있었으며 결과값이 한 번도 바뀐 적이 없을 때
    # 결과값을 구한다
    if flag and result == -1:
        result = i + 1

print(0 if result == -1 else result)