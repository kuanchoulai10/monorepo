class Solution:
    def findMin(self, nums: List[int]) -> int:
        l = 0
        r = len(nums) - 1

        ans = nums[0]
        while l <= r:
            if nums[l] < nums[r]:
                ans = min(ans, nums[l])
                break

            m = (l + r) // 2
            ans = min(ans, nums[m])

            # left sorted portion
            if nums[m] >= nums[l]:
                l = m + 1
            # right sorted portion
            else:
                r = m - 1
        
        return ans
