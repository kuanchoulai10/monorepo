class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums)-1

        # Rotated len(nums) times
        if nums[l] < nums[r]:
            return nums[l]

        while l <= r:
            m = (l + r) // 2

            left_larger_than_curr  = (m == 0           or nums[m-1] > nums[m])
            right_larger_than_curr = (m == len(nums)-1 or nums[m+1] > nums[m])
            if left_larger_than_curr and right_larger_than_curr:
                return nums[m]

            if nums[m] > nums[-1]: # left sorted side
                l = m + 1
            else:
                r = m - 1