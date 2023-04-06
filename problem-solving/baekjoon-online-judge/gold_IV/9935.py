# 9935. 문자열 폭발

string = input()
bomb = input()
stack = list()
bomb_len = len(bomb)
ref = 0

while ref < len(string):
    # 스택을 쌓아가다
    stack.append(string[ref])
    # 스택 마지막 문자가 폭탄 마지막 문자와 같고
    # 스택 마지막 부분이 폭탄과 같다면 폭탄 길이만큼 스택에서 pop한다
    if stack[-1] == bomb[-1] and (''.join(stack[-1 * bomb_len:])) == bomb:
        for i in range(bomb_len):
            stack.pop()
    ref += 1

# 스택에 문자가 남아있으면 출력한다
if stack:
    print(''.join(stack))
# 남아있지 않으면 FRULA를 출력한다
else:
    print('FRULA')
