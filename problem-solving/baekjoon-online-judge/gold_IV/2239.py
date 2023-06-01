# 2239. 스도쿠

import sys
input = sys.stdin.readline


def puzzle(n):
    if n == len(zeros):
        for i in range(9):
            print(*board[i], sep='')
        sys.exit()

    r, c = zeros[n]
    row, col = r // 3, c // 3
    nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # 3x3 정사각형
    # 이미 있는 숫자를 후보군에서 제거한다
    for i in range(3 * row, (row + 1) * 3):
        for j in range(3 * col, (col + 1) * 3):
            if board[i][j] in nums:
                nums.remove(board[i][j])

    # 행과 열
    # 이미 있는 숫자를 후보군에서 제거한다
    for i in range(9):
        if board[i][c] in nums:
            nums.remove(board[i][c])
        if board[r][i] in nums:
            nums.remove(board[r][i])

    # 후보군에 남아있는 숫자를 오름차순으로 차례대로 빈칸에 추가하고
    # 그 다음 칸에 넣어야 할 숫자를 찾기 위해 puzzle(n + 1)을 실행한다
    for num in sorted(list(nums)):
        board[r][c] = num
        puzzle(n + 1)

    # 초기화
    board[r][c] = 0


board = list()
zeros = list()

for i in range(9):
    board.append(list(map(int, input().strip())))
    for j in range(9):
        # 빈칸 위치 저장하기
        if board[-1][j] == 0:
            zeros.append((i, j))

puzzle(0)