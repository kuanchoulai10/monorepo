# --8<-- [start:iterative]
from collections import deque
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = deque([[]])
        for num in nums:
            for _ in range(len(result)):
                perm = result.popleft()
                for i in range(len(perm)+1):
                    result.append(
                        perm[:i] + [num] + perm[i:]
                    )
        return list(result)
# --8<-- [end:iterative]

# --8<-- [start:recursive]
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        if len(nums) == 1:
            return [nums]

        result = []
        perms = self.permute(nums[1:])
        for perm in perms:
            for i in range(len(perm)+1):
                result.append(
                    perm[:i] + [nums[0]] + perm[i:]
                )
        return result
# --8<-- [end:recursive]
