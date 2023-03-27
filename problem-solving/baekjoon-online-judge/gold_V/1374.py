# 1374. 강의실

import heapq, sys

lecture_num = int(sys.stdin.readline())
lecture = list()
room = [(0, 0)]

# 강의 정보를 입력받아 힙 lecture에 저장한다
# 이때 시작 시간과 종료 시간을 묶는다
for i in range(lecture_num):
    number, start, end = map(int, sys.stdin.readline().split())
    heapq.heappush(lecture, (start, end))

# 이미 배정된 강의 중 가장 빨리 끝나는 강의의 종료시간과
# 배정되지 않은 강의 중 가장 빨리 시작하는 강의의 시작시간을 비교한다
# 종료시간이 시작시간보다 빠르거나 같으면 그 강의실에 강의를 배정한다
# 그렇지 않으면 새로운 강의실에 강의를 배정한다
while lecture:
    time = heapq.heappop(lecture)
    space = heapq.heappop(room)
    if space[0] <= time[0]:
        heapq.heappush(room, (time[1], time[0]))
    else:
        heapq.heappush(room, space)
        heapq.heappush(room, (time[1], time[0]))

print(len(room))