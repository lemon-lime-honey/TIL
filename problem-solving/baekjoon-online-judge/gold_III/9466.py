# 9466. 텀 프로젝트

import sys
input = sys.stdin.readline
sys.setrecursionlimit(10 ** 6)


def dfs(p):
    global result
    chk[p] = True
    arr.append(p)

    # 다음 학생이 이미 나온 적 있는 경우
    # 이번 사이클에서 나온 적(리스트 arr)이 있으면
    # 그 학생이 나온 시점부터 지금까지의 arr를 result에 추가한다
    if chk[students[p]]:
        if students[p] in arr:
            result += arr[arr.index(students[p]):]
        return
    else:
        dfs(students[p])


t = int(input())

for i in range(t):
    n = int(input())
    students = [0] + list(map(int, input().split()))
    chk = [False for i in range(n + 1)]
    result = list()

    for j in range(1, n + 1):
        if not chk[j]:
            arr = list()
            dfs(j)

    print(n - len(result))