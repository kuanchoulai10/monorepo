# --8<-- [start:nested-loop]
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        n2i = {
            num: i
            for i, num in enumerate(nums1)
        }
        result = [-1] * len(nums1)
        for i in range(len(nums2)):
            if nums2[i] not in n2i:
                continue
            for j in range(i+1, len(nums2)):
                if nums2[j] > nums2[i]:
                    idx = n2i[nums2[i]]
                    result[idx] = nums2[j]
                    break
        return result
# --8<-- [end:nested-loop]

# --8<-- [start:stack]
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        n2i = {
            num: i
            for i, num in enumerate(nums1)
        }
        result = [-1] * len(nums1)
        stack = []
        for i in range(len(nums2)):
            current = nums2[i]
            while len(stack) != 0 and current > stack[-1]:
                idx = n2i[stack.pop()]
                result[idx] = current
            if current in n2i:
                stack.append(current)
        return result
# --8<-- [start:stack]
