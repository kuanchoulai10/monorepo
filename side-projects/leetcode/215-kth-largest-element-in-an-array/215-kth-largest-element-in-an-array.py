class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # O(N logN)
        # nums.sort()
        # return nums[len(nums) - k]

        k = len(nums)-k
        def quick_select(l: int, r: int):
            pivot_value = nums[r]
            p = l

            # put all the value that is less than or equal to the pivot value to the left
            for i in range(l, r):
                curr_value = nums[i]
                if curr_value <= pivot_value:
                    nums[p], nums[i] = nums[i], nums[p]
                    p += 1
            # put the pivot value to the pivot location
            nums[p], nums[r] = nums[r], nums[p]

            # Case 1: the index that you are looking for is on the right the pivot value
            if k > p:
                return quick_select(p+1, r)
            # Case 2: the index that you are looking for is equal to the pivot value
            elif k == p:
                return nums[p]
            # Case 3: the index that you are looking for is on the left the pivot value
            else:
                return quick_select(l, p-1)
        
        return quick_select(0, len(nums)-1)