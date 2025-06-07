# Reminders
# 1. exactly one solution
# 2. may not use the same element twice
# 3. return indices
# 4. input: may be some duplicate values
# 5. return the answer in any order.

# Naive approach
# Nested for-loop
# - outer loop: go through the array from the first element to the second last.
# - inner loop: go through the array from the element that is next to the element that the outer loop focus on to the last
# time complexity: O(n^2)
# space complexity: O(1)


# Hashmap approach
# time complexity: O(n)
# space complexity: O(n)
# Explanation:
# 1. go through the array, store the complement and the index of it for each number in dict
# 2. if the number is in the dict, then we found the answer


# d = {2:0}
# target = 9
# complement = 2
#           >
# nums = [2,7,11,15]

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_idx = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_idx:
                return [num_to_idx[complement], i]
            num_to_idx[num] = i
        return []
