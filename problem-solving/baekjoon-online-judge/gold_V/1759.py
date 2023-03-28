# 1759. 암호 만들기

import sys
input = sys.stdin.readline

# 백트래킹
# 완성된 암호의 자음 개수가 2개 이상, 모음 개수가 1개 이상이면 출력한다
def backtrack(start: int):
    global consonant, vowel
    if len(answer) == l:
        if consonant > 1 and vowel > 0:
            print(*answer, sep='')
            return

    # 문자를 추가할 때마다 자음 개수 또는 모음 개수에 1을 더한다
    for i in range(start, c):
        answer.append(letters[i])
        if letters[i] in 'aeiou':
            vowel += 1
        else:
            consonant += 1
        backtrack(i + 1)
        answer.pop()
        if letters[i] in 'aeiou':
            vowel -= 1
        else:
            consonant -= 1

l, c = map(int, input().split())
letters = list(input().split())
answer = list()
letters.sort()
consonant = 0
vowel = 0

backtrack(0)