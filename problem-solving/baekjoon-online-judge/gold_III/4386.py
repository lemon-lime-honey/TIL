# 4386. 별자리 만들기

from math import sqrt
import sys
input = sys.stdin.readline


# find
def find(s):
    if s != const[s]:
        const[s] = find(const[s])
    return const[s]


# union
def union(s1, s2):
    s1, s2 = find(s1), find(s2)
    if s1 == s2: return True
    if s1 < s2: const[s2] = s1
    else: const[s1] = s2
    return False


n = int(input())
stars = [list(map(float, input().split())) for i in range(n)]
const = [i for i in range(n)]
paths = list()
result = 0

# 별과 별 사이의 경로 길이를 구하고 리스트 paths에
# 그 길이와 함께 출발점과 도착점을 튜플로 묶어 넣는다
for i in range(n):
    for j in range(i + 1, n):
        distance = sqrt((stars[i][0] - stars[j][0]) ** 2 + (stars[i][1] - stars[j][1]) ** 2)
        paths.append((distance, i, j))

# 리스트 paths를 경로 기준으로 오름차순 정렬한다
paths.sort()

# paths를 순회하며 union 함수를 실행한다
# 반환값이 True이면 이미 연결된 관계이므로 생략,
# False이면 결과값에 거리를 더해준다
for dist, start, end in paths:
    chk = union(start, end)
    if not chk:
        result += dist

print(f'{result:.2f}')