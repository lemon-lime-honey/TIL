n = int(input())

# 초기 설정
# 열과 두 종류의 대각선 중복 여부를 확인할 set
# 오른쪽 아래 방향 대각선이 negDiag
# 오른쪽 위 방향 대각선이 posDiag
negDiag = set()
posDiag = set()
col = set()
result = 0

def backtrack(row):
    global result
    # 모든 행을 다 확인했을 때
    if row == n:
        result += 1
        return

    for c in range(n):
        # 퀸이 공격을 받을 수 있는 자리인지 판별
        if c in col or (row + c) in posDiag or (row - c) in negDiag:
            continue

        # 백트래킹
        col.add(c)
        posDiag.add(row + c)
        negDiag.add(row - c)
        backtrack(row + 1)
        col.remove(c)
        posDiag.remove(row + c)
        negDiag.remove(row - c)

backtrack(0)

print(result)