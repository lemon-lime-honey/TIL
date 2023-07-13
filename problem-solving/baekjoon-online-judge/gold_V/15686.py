# 15686. 치킨 배달

from itertools import combinations
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
household = list()
chicken = list()
cities = list()
result = int(1e9)

for i in range(n):
    # 도시 정보 입력
    cities.append(list(map(int, input().split())))
    for j in range(n):
        # 집과 치킨집의 위치를 저장한다
        if cities[i][j] == 1:
            household.append((i, j))
        elif cities[i][j] == 2:
            chicken.append((i, j))

# m개의 치킨집을 고르는 조합
chicken_comb = combinations(chicken, m)

# 조합을 순회하며 도시의 치킨 거리를 구한다
for chicken_set in chicken_comb:
    house = [int(1e9) for i in range(len(household))]
    for r, c in chicken_set:
        for i in range(len(house)):
            house[i] = min(house[i], abs(household[i][0] - r) + abs(household[i][1] - c))
    result = min(result, sum(house))

print(result)