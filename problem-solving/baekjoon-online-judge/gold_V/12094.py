# 12094. A와 B

s = list(input())
t = list(input())

while len(s) != len(t):
    # 변환된 문자열의 마지막 문자가 A이면 pop한다
    if t[-1] == 'A':
        t.pop()
    # 변환된 문자열의 마지막 문자가 B이면 pop하고 뒤집는다
    elif t[-1] == 'B':
        t.pop()
        t = t[::-1]

print(1 if s == t else 0)