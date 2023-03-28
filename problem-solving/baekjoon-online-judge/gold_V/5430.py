# 5430. AC

import sys
from collections import deque

t = int(sys.stdin.readline())

# R이 나왔을 때 실제로 뒤집으면 시간초과
for i in range(t):
    p = sys.stdin.readline().strip()
    n = int(sys.stdin.readline())
    temp = sys.stdin.readline().strip().replace('[', '').replace(']', '')
    flag = 0
    try:
        x = deque(map(str, temp.split(',')))
    except:
        flag = 1

    rev = False
    for command in p:
        if command == 'R':
            rev = not rev
        elif command == 'D':
            if (len(x) == 0) + (n == 0):
                flag = 1
                break
            else:
                if rev:
                    x.pop()
                else:
                    x.popleft()

    if flag == 1:
        print('error')
    else:
        if rev:
            print(f"[{','.join(list(x)[::-1])}]")
        else:
            print(f"[{','.join(list(x))}]")