class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l = 0
        r = len(nums)-1

        while l <= r:
            m = (l + r) // 2

            if nums[m] == target:
                return m

            # left sorted side
            if nums[m] >= nums[-1]:
                if nums[0] <= target <= nums[m]:
                    r = m - 1
                else:
                    l = m + 1
            # right sorted side
            else:
                if nums[m] <= target <= nums[-1]:
                    l = m + 1
                else:
                    r = m - 1
        
        return -1