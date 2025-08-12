class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        result = 0
        num_zeros = 0
        num_ones = 0

        prefix_diff = {}
        for i, n in enumerate(nums):
            num_zeros += 1 if n == 0 else 0
            num_ones += 1 if n == 1 else 0

            diff = num_ones - num_zeros
            if diff == 0:
                result = num_zeros + num_ones
            else:
                if diff not in prefix_diff:
                    prefix_diff[diff] = i
                else:
                    j = prefix_diff[diff]
                    result = max(result, i-j)
        return result
