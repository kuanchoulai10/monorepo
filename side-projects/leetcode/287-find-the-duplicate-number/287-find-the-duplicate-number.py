# --8<-- [start:fast-slow-pointers]
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        def getNext(idx: int) -> int:
            return nums[idx]
        
        slow, fast = 0, 0

        while True:
            slow = getNext(slow)
            fast = getNext(getNext(fast))
            if slow == fast:
                break
        
        slow2 = 0
        while True:
            slow = getNext(slow)
            slow2 = getNext(slow2)
            if slow == slow2:
                break

        return slow
# --8<-- [end:fast-slow-pointers]
# --8<-- [start:binary-search]
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:

        low = 1
        high = len(nums) - 1

        while low <= high:
            target = (low + high) // 2

            counts = 0
            for num in nums:
                if num <= target:
                    counts += 1
            
            if counts <= target:
                low = target + 1
            else:
                duplicate = target
                high = target - 1

        return duplicate
# --8<-- [end:binary-search]
