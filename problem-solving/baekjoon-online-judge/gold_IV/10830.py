# 10830. 행렬 제곱
# 1629(Silver I, 곱셈)

import sys
input = sys.stdin.readline


# 정사각행렬 두 개를 곱하는 함수
def mul_matrix(m1, m2):
    res = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] += m1[i][k] * m2[k][j] % 1000
    return res


# 1629번 문제와 유사하게 해결했다
def exp(a, b):
    if b == 1: return a
    res = exp(a, b // 2)
    return mul_matrix(mul_matrix(res, res), a) if b % 2 else mul_matrix(res, res)


n, b = map(int, input().split())
matrix = [list(map(int, input().split())) for i in range(n)]
result = exp(matrix, b)

for row in result:
    for element in row:
        print(element % 1000, end=" ")
    print()