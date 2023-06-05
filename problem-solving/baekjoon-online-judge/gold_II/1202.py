# 1202. 보석 도둑

import heapq, sys
input = sys.stdin.readline

n, k = map(int, input().split())
jewels = list()
jewel = list()
total = 0

# 보석 정보를 무게와 가격 기준으로 최소 힙에 추가한다
for i in range(n):
    m, v = map(int, input().split())
    heapq.heappush(jewels, (m, v))

# 가방은 오름차순 정렬한다
bags = [int(input()) for i in range(k)]
bags.sort()

# 담을 수 있는 최대 무게가 가장 작은 것부터
for bag in bags:
    # 보석의 무게가 조건에 맞는 동안
    # 힙에서 보석 정보를 추출해
    # 보석의 가치를 최대 힙에 추가한다
    while jewels and jewels[0][0] <= bag:
        heapq.heappush(jewel, -heapq.heappop(jewels)[1])
    # 조건에 맞는 무게를 가진 보석 중 가장 비싼 보석의 값을
    # 결과에 더한다
    if jewel: total -= heapq.heappop(jewel)
    # 담을 수 있는 보석이 더이상 존재하지 않으면 루프를 빠져나간다
    elif not jewels: break

print(total)