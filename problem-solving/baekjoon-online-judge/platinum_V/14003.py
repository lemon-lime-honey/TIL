# 14003. 가장 긴 증가하는 부분 수열 5

from bisect import bisect_left

n = int(input())
numbers = list(map(int, input().split()))
sub = [1 for i in range(n)]

result = [numbers[0]]

for i in range(1, n):
    # 부분 수열 리스트의 가장 마지막 원소가
    # 숫자 리스트의 i번째 원소보다 작으면
    # 수열 마지막에 그냥 추가한다
    # 인덱스 리스트의 i번째 원소 값을
    # 부분 수열 리스트의 길이로 바꾼다
    if result[-1] < numbers[i]:
        result.append(numbers[i])
        sub[i] = len(result)
    # 그렇지 않으면 이분탐색을 이용해
    # 부분 수열 리스트에서 들어갈 수 있는
    # 위치를 찾아 숫자를 바꾼다
    # 인덱스 리스트의 i번째 원소 값을
    # 이분탐색으로 구한 인덱스 + 1로 바꾼다
    else:
        idx = bisect_left(result, numbers[i])
        result[idx] = numbers[i]
        sub[i] = idx + 1

print(len(result))
ref = len(result)
answer = list()

# 인덱스 리스트의 값을 마지막부터 탐색하며
# 부분 수열의 길이와 같은 것부터
# 1씩 줄어갈 때마다 해당하는 숫자를
# 결과 리스트에 추가한다
for i in range(n - 1, -1, -1):
    if sub[i] == ref:
        answer.append(numbers[i])
        ref -= 1

# 결과 리스트를 뒤집어서 출력한다
print(*answer[::-1])