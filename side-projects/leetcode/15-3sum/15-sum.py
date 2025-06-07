# HashSet without Sorting
def two_sum(nums: List[int], target: int, result: List[List[int]]) -> List[List[int]]:
    seen = set()
    for j in range(len(nums)):
        complement = target - nums[j]
        if complement in seen:
            t = tuple(sorted(
                [-target, nums[j], complement]
            ))
            result.add(t)
        seen.add(nums[j])

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        seen = set()
        result = set()
        for i in range(len(nums)-2):
            target = -nums[i]
            if nums[i] not in seen:
                two_sum(
                    nums=nums[i+1:],
                    target=target,
                    result=result
                )
                seen.add(nums[i])
        return list(result)