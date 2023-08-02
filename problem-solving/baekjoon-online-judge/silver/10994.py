# 10994. 별 찍기 - 19

def star(n):
    # n이 1일 때에는 *이 히나 있는 리스트를 반환한다
    if n == 1:
        return ['*']
    # n - 1까지의 결과 리스트를 가지고 *을 추가해준다
    before = star(n - 1)
    result = list()
    result.append((4 * n - 3) * '*')
    result.append('*' + ' ' * (4 * n - 5) + '*')
    for i in range(len(before)):
        result.append('* ' + before[i] + ' *')
    result.append('*' + ' ' * (4 * n - 5) + '*')
    result.append((4 * n - 3) * '*')
    # 현 단계까지의 리스트를 반환한다
    return result


n = int(input())
result = star(n)

for i in range(len(result)):
    print(*result[i], sep='')