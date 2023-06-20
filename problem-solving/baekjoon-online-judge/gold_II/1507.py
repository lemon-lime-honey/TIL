# 1507. 궁금한 민호

from copy import deepcopy
import sys
input = sys.stdin.readline

n = int(input())
cities = [list(map(int, input().split())) for i in range(n)]
original = deepcopy(cities)
result = 0

for i in range(n):
    for j in range(n):
        for k in range(n):
            if i == j or i == k: continue
            # 경유지를 거쳐서 이동할 때와 바로 이동할 때의 이동시간이 같으면
            # 바로 이동할 때의 값을 0으로 바꿔준다
            if cities[j][k] == cities[j][i] + cities[i][k]:
                original[j][k] = 0
            # 경유지를 거쳐서 이동할 때보다 바로 이동할 때 이동시간이 더 길면
            # -1을 출력하고 종료한다
            elif cities[j][k] > cities[j][i] + cities[i][k]:
                print(-1)
                sys.exit()

for i in range(n):
    for j in range(n):
        result += original[i][j]

# 왼쪽 위에서 오른쪽 아래로 향하는 대각선 기준으로 대칭이므로
# 모든 도로의 소요 시간의 합은 행렬의 값을 다 더한 것을 2로 나눈 값이다
print(result // 2)