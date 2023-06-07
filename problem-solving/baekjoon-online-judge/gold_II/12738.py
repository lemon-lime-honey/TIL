# 12738. 가장 긴 증가하는 부분 수열 3

n = int(input())
numbers = list(map(int, input().split()))
result = [numbers[0]]

for i in range(1, n):
    # 부분 수열 리스트의 가장 마지막 원소가
    # 숫자 리스트의 i번째 원소보다 작으면
    # 수열 마지막에 그냥 추가한다
    if result[-1] < numbers[i]:
        result.append(numbers[i])
    # 그렇지 않으면 이분탐색을 이용해
    # 부분 수열 리스트에서 들어갈 수 있는 
    # 위치를 찾아 숫자를 바꾼다
    else:
        lo, hi = 0, len(result) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if result[mid] < numbers[i]:
                lo = mid + 1
            else:
                hi = mid

        result[hi] = numbers[i]

# 부분 수열의 길이를 출력한다
print(len(result))