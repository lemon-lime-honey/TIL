# 3745. 오름세

from bisect import bisect_left
import sys
input = sys.stdin.readline

while True:
    # 테스트 케이스의 개수에 관한 언급이 없어
    # while loop 안에서 try-except문을 사용했다
    try:
        n = int(input())
        cost = list(map(int, input().split()))
        result = [cost[0]]
        # 가장 긴 증가하는 부분 수열의 길이 구하기
        for i in range(1, n):
            if result[-1] < cost[i]:
                result.append(cost[i])
            else:
                idx = bisect_left(result, cost[i])
                result[idx] = cost[i]
        print(len(result))
    except:
        break