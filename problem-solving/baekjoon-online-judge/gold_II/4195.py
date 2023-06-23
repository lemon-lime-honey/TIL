# 4195. 친구 네트워크

import sys
input = sys.stdin.readline


def find(p):
    if p != root[p]:
        root[p] = find(root[p])
    return root[p]


def union(p1, p2):
    p1, p2 = find(p1), find(p2)
    if p1 == p2: return friend[p1]
    root[p2] = p1

    # union 연산을 하게 되면 친구 네트워크의 크기도 업데이트
    friend[p1] += friend[p2]
    return friend[p1]


t = int(input())

for i in range(t):
    f = int(input())
    # 루트 정보와 친구 네트워크의 크기를 위한 두 개의 딕셔너리
    root = dict()
    friend = dict()

    for j in range(f):
        a, b = map(str, input().strip().split())

        # 입력된 이름이 처음으로 입력된 경우
        if root.get(a) is None:
            root[a] = a
            friend[a] = 1
        if root.get(b) is None:
            root[b] = b
            friend[b] = 1

        # 입력된 이름 연결하기
        result = union(a, b)
        print(result)