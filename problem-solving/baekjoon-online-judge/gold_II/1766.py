# 1766. 문제집

import heapq, sys
input = sys.stdin.readline

n, m = map(int, input().split())
problems = [[] for i in range(n + 1)]
chk = [0 for i in range(n + 1)]
result = list()
que = list()

# 데이터 입력
for i in range(m):
    a, b = map(int, input().split())
    problems[a].append(b)
    chk[b] += 1

# 문제 진입차수 리스트를 순회한다
# 진입차수가 0인 문제는 힙에 추가한다
for i in range(1, n + 1):
    if chk[i] == 0:
        heapq.heappush(que, i)

# 힙에서 그 중 가장 작은 번호를 가진 문제를 뽑는다
# 문제 선행관계 리스트를 돌며 문제에 연결된 다른 문제의 진입차수를 1씩 뺀다
# 진입차수가 0인 문제를 발견하면 힙에 추가한다
while que:
    now = heapq.heappop(que)
    result.append(now)
    for problem in problems[now]:
        chk[problem] -= 1
        if chk[problem] == 0:
            heapq.heappush(que, problem)

print(*result)