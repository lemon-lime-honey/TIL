# 11000. 강의실 배정

import heapq, sys

n = int(sys.stdin.readline())
lecture = list()
room = [1]

# 데이터 입력받기
# 힙에 저장할 때 시작 시간과 종료 시간을 묶는다
for i in range(n):
    n1, n2 = map(int, sys.stdin.readline().split())
    heapq.heappush(lecture, (n1, n2))

# 강의 시간이 저장된 힙 lecture
while lecture:
    # 배정하지 않은 강의 중 가장 먼저 시작하는 강의의 시작 시간과
    # 강의실에 배정된 강의 중 가장 먼저 끝나는 강의의 종료 시간을 비교한다
    # 시작 시각 time[0]이 종료 시각 ref보다 
    # 작거나 같으면 ref의 값을 time[1]으로 바꾸고 힙 room에 넣는다
    # 크면 room에 time[1]을 넣는다
    time = heapq.heappop(lecture)
    ref = heapq.heappop(room)
    if ref <= time[0]:
        ref = time[1]
        heapq.heappush(room, ref)
    else:
        heapq.heappush(room, ref)
        heapq.heappush(room, time[1])

print(len(room))