class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        nums = [-float('inf')] + nums + [-float('inf')]
        lower = 1
        upper = len(nums)-2

        while True:
            m = (lower + upper) // 2
            if (nums[m] > nums[m-1]) and (nums[m] > nums[m+1]):
                return m-1 # offset negative infinite number we just added at the first place
            else:
                if nums[m-1] > nums[m]:
                    upper = m-1
                elif nums[m+1] > nums[m]:
                    lower = m+1
