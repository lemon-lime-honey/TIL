# 1365. 꼬인 전깃줄

from bisect import bisect_left
import sys
input = sys.stdin.readline

n = int(input())
pole = list(map(int, input().split()))
result = [pole[0]]

# 가장 긴 증가하는 부분 수열
# 전신주 리스트를 순회한다
# 결과 리스트의 마지막 원소보다 전신주의 높이가 더 크면
# 결과 리스트에 추가한다
# 그렇지 않으면 이분 탐색으로 결과 리스트에
# 전신주 높이가 들어갈 자리를 찾아 바꿔준다
for i in range(1, n):
    if result[-1] < pole[i]:
        result.append(pole[i])
    else:
        chk = bisect_left(result, pole[i])
        result[chk] = pole[i]

# 전신주 총 개수에서 결과 리스트의 길이를 뺀 값을 출력한다
print(n - len(result))