# 11444. 피보나치 수 6
# 1629(Silver I, 곱셈), 10830(Gold IV, 행렬 제곱)

# 두 개의 2X2 행렬을 곱하는 함수
def mul_matrix(m1, m2):
    res = [[0 for i in range(2)] for j in range(2)]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                res[i][j] += m1[i][k] * m2[k][j] % 1000000007
    return res


# 1629, 10830번과 유사하게 해결했다.
def exp(a, b):
    if b == 1: return a
    res = exp(a, b // 2)
    return mul_matrix(mul_matrix(res, res), a) if b % 2 else mul_matrix(res, res)


n = int(input())
matrix = [[1, 1], [1, 0]]
final_matrix = exp(matrix, n)

print(final_matrix[0][1] % 1000000007)