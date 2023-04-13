# 21939. 문제 추천 시스템 Version 1

import heapq, sys
input = sys.stdin.readline

n = int(input())
problems = dict()  # 문제 번호에 따른 난이도를 저장하는 딕셔너리
easy = list()
hard = list()

for i in range(n):
    p, l = map(int, input().split())
    # 최소 힙, 최대 힙을 둘 다 사용한다
    # 가장 어려운 문제가 여러 개일 때 문제 번호가 큰 것을 출력해야 하므로
    # 최대 힙에 push할 때 문제 번호에도 -1을 곱해야 한다.
    heapq.heappush(easy, (l, p))
    heapq.heappush(hard, (-1 * l, -1 * p))
    problems[p] = l

m = int(input())

for i in range(m):
    command = list(input().split())
    # Add
    if command[0] == 'add':
        heapq.heappush(easy, (int(command[2]), int(command[1])))
        heapq.heappush(hard, (-1 * int(command[2]), -1 * int(command[1])))
        problems[int(command[1])] = int(command[2])
    # Solved
    # 입력된 문제를 풀었다는 의미로 난이도를 0으로 바꾼다
    elif command[0] == 'solved':
        problems[int(command[1])] = 0
    # Recommend
    else:
        # 어려운 문제 추천
        if command[1] == '1':
            while hard and problems[-1 * hard[0][1]] != -1 * hard[0][0]:
                heapq.heappop(hard)
            print(-1 * hard[0][1])
        # 쉬운 문제 추천
        else:
            while easy and problems[easy[0][1]] != easy[0][0]:
                heapq.heappop(easy)
            print(easy[0][1])