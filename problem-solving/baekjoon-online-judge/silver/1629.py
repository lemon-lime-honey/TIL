# 1629. 곱셈

import sys


def exp(a, b, c):
    # base case: b가 1일 때 a % c를 반환한다
    if b == 1: return a % c
    # b가 1이 아닐 때 (a ** (b // 2)) % c를 계산한다
    res = exp(a, b // 2, c)
    # b가 홀수일 때에는 위의 res의 제곱에 a를 한 번 더 곱하고 c로 나눈 나머지 반환
    # b가 짝수일 때에는 res의 제곱을 c로 나눈 나머지 반환
    return (res * res * a) % c if b % 2 else (res * res) % c

a, b, c = map(int, sys.stdin.readline().split())
result = exp(a, b, c)
print(result)