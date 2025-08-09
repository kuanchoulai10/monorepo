class NumArray:
    def __init__(self, nums: List[int]):
        self._prefix_sums = [0] * (len(nums)+1)
        for i in range(len(nums)):
            self._prefix_sums[i+1] = self._prefix_sums[i] + nums[i]
        print(self._prefix_sums)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix_sums[right+1] - self._prefix_sums[left]

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)