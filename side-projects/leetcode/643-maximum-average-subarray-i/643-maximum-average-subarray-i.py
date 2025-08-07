class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        curr_sums = 0
        max_sums = -float("inf")
        for i in range(len(nums)):
            if i+1 < k:
                curr_sums += nums[i]
            elif i+1 == k:
                curr_sums += nums[i]
                max_sums = max(
                    max_sums,
                    curr_sums
                )
            else:
                curr_sums += nums[i]
                curr_sums -= nums[i-k]
                max_sums = max(
                    max_sums,
                    curr_sums
                )
        return max_sums / k
