# 1913. 달팽이

n = int(input())
target = int(input())

# 숫자가 적힐 칸 이동 방향
# 순서: 상, 우, 하, 좌
direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
table = [[0 for i in range(n)] for j in range(n)]
# 회전 시작점의 좌표
# 표의 중심에서 왼쪽 위로 올라간다
ref = [n // 2, n // 2]
# 찾을 숫자의 좌표
# 표의 중심 위치로 초기화한다
result = [n // 2 + 1, n // 2 + 1]

# 표의 중심에 1을 채운다
table[ref[0]][ref[1]] = 1
# 채울 숫자의 위치
pos = [0, 0]
# 채울 숫자
number = 2
# 이동 방향(0: 상, 1: 우, 2: 하, 3: 좌)
turn = 0

# 3*3부터 n*n까지 한바퀴씩
for i in range(3, n + 1, 2):
    # 회전 시작점의 한 칸 위에 숫자를 채우고 숫자에 1을 더해준다
    pos = ref
    pos = pos[0] + direction[turn][0], pos[1] + direction[turn][1]
    table[pos[0]][pos[1]] = number
    if number == target:
        result = pos[0] + 1, pos[1] + 1
    number += 1

    # 방향: 오른쪽
    # i - 2번 오른쪽으로 가면서 숫자를 채운다
    turn = 1
    for j in range(i - 2):
        pos = pos[0] + direction[turn][0], pos[1] + direction[turn][1]
        table[pos[0]][pos[1]] = number
        if number == target:
            result = pos[0] + 1, pos[1] + 1
        number += 1

    # 방향: 아래
    # i - 1번 아래로 가면서 숫자를 채운다
    turn = 2
    for j in range(i - 1):
        pos = pos[0] + direction[turn][0], pos[1] + direction[turn][1]
        table[pos[0]][pos[1]] = number
        if number == target:
            result = pos[0] + 1, pos[1] + 1
        number += 1

    # 방향: 왼쪽
    # i - 1번 왼쪽으로 가면서 숫자를 채운다
    turn = 3
    for j in range(i - 1):
        pos = pos[0] + direction[turn][0], pos[1] + direction[turn][1]
        table[pos[0]][pos[1]] = number
        if number == target:
            result = pos[0] + 1, pos[1] + 1
        number += 1

    # 방향: 위
    # i - 1번 위로 가면서 숫자를 채운다
    turn = 0
    for j in range(i - 1):
        pos = pos[0] + direction[turn][0], pos[1] + direction[turn][1]
        table[pos[0]][pos[1]] = number
        if number == target:
            result = pos[0] + 1, pos[1] + 1
        number += 1

    # 회전 시작점의 위치를 바꾼다
    ref[0] -= 1
    ref[1] -= 1

for i in range(n):
    print(*table[i])

print(*result)