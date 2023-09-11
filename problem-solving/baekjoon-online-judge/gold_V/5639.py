# 5639. 이진 검색 트리

from itertools import takewhile
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**4)

# 전위순회를 후위순회로 변환하기 위한 함수
# 재귀호출을 이용했다.
# 전위순회: 루트 + 왼쪽 + 오른쪽...의 반복
# 후위순회: 왼쪽 + 오른쪽 + 루트...의 반복
# itertools 모듈의 takewhile 함수를 사용해 양쪽 하위 트리를 구할 수 있다
def post(nums):
    if not nums: return list()
    root = nums[0]
    left = list(takewhile(lambda x: x < root, nums[1:]))
    right = nums[len(left) + 1:]
    return post(left) + post(right) + [root]


numbers = list()

while True:
    try: numbers.append(int(input()))
    except: break

result = post(numbers)
print(*result, sep='\n')

'''
itertools.takewhile(predicate, iterable)
`iterable`에서 `predicate`가 참인 부분까지의 원소를 반환한다.
위의 코드에서 `takewhile(lambda x: x < root, nums[1:])`은 주어진 배열에서
`root`를 제외한 뒷부분 중 `root`보다 작은 원소 리스트를 반환한다.
'''