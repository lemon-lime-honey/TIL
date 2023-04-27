# 7662. 이중 우선순위 큐

import heapq, sys

t = int(sys.stdin.readline())

for i in range(t):
    k = int(sys.stdin.readline())
    # 최대힙과 최소힙용 리스트를 준비한다
    maxHeap = list()
    minHeap = list()
    chk = [True] * k
    
    for j in range(k):
        command = list(sys.stdin.readline().split())
        # Insert
        # 힙에 값을 추가할 때 들어온 순서를 고려하기 위해 j도 포함시킨다
        if command[0] == 'I':
            heapq.heappush(maxHeap, (-1 * int(command[1]), j))
            heapq.heappush(minHeap, (int(command[1]), j))
        # Delete
        # 수가 제거되었다면 리스트 chk에서 그 수에 해당하는 원소의 값을 False로 바꾼다
        # 이미 제거된 숫자라면 제거되지 않은 숫자가 나올 때까지 반복한다
        if command[0] == 'D':
            if len(maxHeap) or len(minHeap):
                if int(command[1]) == 1:
                    while maxHeap and not chk[maxHeap[0][1]]:
                        heapq.heappop(maxHeap)
                    if maxHeap:
                        chk[maxHeap[0][1]] = False
                        heapq.heappop(maxHeap)
                elif int(command[1]) == -1:
                    while minHeap and not chk[minHeap[0][1]]:
                        heapq.heappop(minHeap)
                    if minHeap:
                        chk[minHeap[0][1]] = False
                        heapq.heappop(minHeap)

    # 제거되었지만 힙에서 제거되지 않은 값을 제거한다
    while maxHeap and not chk[maxHeap[0][1]]:
        heapq.heappop(maxHeap)
    while minHeap and not chk[minHeap[0][1]]:
        heapq.heappop(minHeap)
    
    if maxHeap and minHeap:
        print(-1 * maxHeap[0][0], minHeap[0][0])
    else:
        print('EMPTY')