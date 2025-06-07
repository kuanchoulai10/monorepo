class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # Approach 1: 
        # - Time complexity: O(m+n)
        m = len(matrix)
        n = len(matrix[0])
        
        r = 0
        c = n - 1
        
        while r < m and c >= 0:
            if target > matrix[r][c]:
                r += 1
            elif target < matrix[r][c]:
                c -= 1
            else:
                return True
        return False

        # Approach 2:
        # - Time complexity: O(m logn)
        def binary_search(nums: List[int], target: int) -> bool:
            left = 0
            right = len(nums) - 1
        
            while left <= right:
                m = (left + right) // 2
                if nums[m] == target:
                    return True
                elif nums[m] > target:
                    right = m - 1
                else:
                    left = m + 1
            return False
        
        for r in range(len(matrix)):
            is_found = binary_search(matrix[r], target)
            if is_found:
                return True
        return False
