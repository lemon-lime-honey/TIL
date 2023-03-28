# 1644. 소수의 연속합

import sys

n = int(sys.stdin.readline())

# n이 1일 때 0 출력
if n == 1: print(0)
# n이 1이 아닐 때
else:
    sieve_bool = [False, False] + [True] * (n - 1)
    sieve = list()

    # 에라토스테네스의 체
    for i in range(2, n + 1):
        if sieve_bool[i]:
            sieve.append(i)
            for j in range(2 * i, n + 1, i):
                sieve_bool[j] = False

    up = 0
    down = 0
    result = 0
    total = sieve[0]

    # 투 포인터
    while up < len(sieve):
        if total < n:
            up += 1
            if up == len(sieve):
                break
            total += sieve[up]
        elif total == n:
            total -= sieve[down]
            result += 1
            down += 1
        elif total > n:
            total -= sieve[down]
            down += 1

    print(result)