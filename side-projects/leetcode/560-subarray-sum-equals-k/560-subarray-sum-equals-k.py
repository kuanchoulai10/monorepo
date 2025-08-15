class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # key:value = prefix_sum: count
        prefix_sums = {0: 1}
        counts = 0

        curr_sum = 0
        for i, num in enumerate(nums):
            curr_sum += num
            complement = curr_sum - k
            # Add up 
            if complement in prefix_sums:
                counts += prefix_sums[complement]
            # Update prefix_sums
            if curr_sum in prefix_sums:
                prefix_sums[curr_sum] += 1
            else:
                prefix_sums[curr_sum] = 1
        return counts
