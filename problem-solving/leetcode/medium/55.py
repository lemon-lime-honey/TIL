# 55. Jump Game
# 유튜브 `NeetCode` 채널의 영상을 참고했다.

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        # 목적지 위치 초기화(리스트의 가장 마지막)
        target = len(nums) - 1

        # 리스트를 거꾸로 순회한다
        # 순회하는 위치와 그 위치의 리스트 원소 값을 더한 것이
        # 목적지보다 멀거나 같다면 목적지를 순회 중인 위치로 변경한다
        for i in range(len(nums) - 1, -1, -1):
            if i + nums[i] >= target:
                target = i

        # 순회를 마친 후 목적지가 시작점이면 True,
        # 아니면 False를 반환한다
        return False if target else True