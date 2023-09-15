# 6068. 시간 관리하기

import heapq, sys
input = sys.stdin.readline

n = int(input())
result = list()
data = list()
time = 0

# 힙에 데이터를 추가한다
# 끝내야 하는 시간으로 내림차순,
# 그 다음 순위로는 소요시간 오름차순으로
# 정렬되어야 한다.
for i in range(n):
    t, s = map(int, input().split())
    heapq.heappush(data, (-s, t))

while data:
    s, t = heapq.heappop(data)
    s = -s

    # 먼저 `time`을 `s - t`로 갱신한다
    if not time:
        time = s - t
    # `time`이 `s - t`보다 크면 `s - t`로 갱신
    # `s`는 해당 작업을 끝내야 하는 시간이므로
    # 그 작업을 시작하기 직전인 `s - t`가 더 작으면
    # 남은 시간을 나타내는 `time`은 `s - t`여야 한다
    # 그렇지 않은 경우 `time`에서 `t`를 빼준다.
    else:
        if time > s:
            time = s - t
        else:
            time -= t

# 모든 데이터를 확인한 후 `time`이 음수라면 `-1`을 출력한다
# 그렇지 않다면 `time`을 출력한다.
print(time if time >= 0 else -1)