# 1918. 후위 표기식

ipt = input()
stack = list()
result = list()

for i in range(len(ipt)):
    # 문자인 경우 결과 배열에 그냥 넣는다
    if ipt[i].isalpha():
        result.append(ipt[i])
    # 여는 괄호인 경우 스택에 넣는다
    elif ipt[i] == '(':
        stack.append(ipt[i])
    # 닫는 괄호인 경우 여는 괄호가 나오기 직전까지 
    # 스택에서 pop한 것을 결과 배열에 넣는 것을 반복한다
    # 마지막에 여는 괄호를 pop한다
    elif ipt[i] == ')':
        while stack and stack[-1] != '(':
            result.append(stack.pop())
        stack.pop()
    # 곱셈 또는 나눗셈일 때
    # 스택에서 곱셈 또는 나눗셈이 나오기 직전까지
    # pop한 것을 결과 배열에 넣는 것을 반복한다
    # 스택에 ipt[i]를 넣는다
    elif ipt[i] in '*/':
        while stack and (stack[-1] in '*/'):
            result.append(stack.pop())
        stack.append(ipt[i])
    # 덧셈 또는 뺄셈일 때
    # 여는 괄호가 나오기 직전까지 스택에서 pop한 것을
    # 결과 배열에 넣는 것을 반복한다
    # 스택에 ipt[i]를 넣는다
    elif ipt[i] in '+-':
        while stack and stack[-1] != '(':
            result.append(stack.pop())
        stack.append(ipt[i])

# 스택에 남아있는 것을 결과 배열에 넣는다
while stack:
    result.append(stack.pop())

print(''.join(result))