# 10159. 저울

import sys
input = sys.stdin.readline

n = int(input())
m = int(input())

# weight: [r] > [c]
# rev_weight: [r] < [c]
weight = [[int(1e9) for i in range(n)] for j in range(n)]
rev_weight = [[int(1e9) for i in range(n)] for j in range(n)]

for i in range(m):
    a, b = map(int, input().split())
    weight[a - 1][b - 1] = 1
    rev_weight[b - 1][a - 1] = 1

# 자기 자신 - 자기 자신 쌍의 경우 값이 0
for i in range(n):
    weight[i][i] = 0
    rev_weight[i][i] = 0

# 플로이드-워셜
for i in range(n):
    for j in range(n):
        for k in range(n):
            weight[j][k] = min(weight[j][k], weight[j][i] + weight[i][k])
            rev_weight[j][k] = min(rev_weight[j][k], rev_weight[j][i] + rev_weight[i][k])

result = list()

# 비교 결과를 알 수 있는 물건의 개수를 먼저 구한 후
# 그 값으로 결과를 알 수 없는 물건의 개수를 구한다.
for i in range(n):
    chk = 0
    for j in range(n):
        if weight[i][j] == int(1e9):
            weight[i][j] = 0
        if rev_weight[i][j] == int(1e9):
            rev_weight[i][j] = 0
        if weight[i][j]:
            chk += 1
        if rev_weight[i][j]:
            chk += 1
    result.append(n - chk - 1)

print(*result, sep='\n')