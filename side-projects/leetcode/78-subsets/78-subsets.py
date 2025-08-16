# --8<-- [start:iterative]
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        
        res = [[]]
        for n in nums:
            for _ in range(len(res)):
                subset = res.pop(0)

                # not include the current number "n"
                res.append(subset.copy())

                # include the current number "n"
                subset.append(n)
                res.append(
                    subset
                )

        return res
# --8<-- [end:iterative]
# --8<-- [start:recursive]
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []

        subset = []

        def dfs(i) -> None:
            if i >= len(nums):
                res.append(subset.copy())
                print(subset)
                return
            
            subset.append(nums[i])
            dfs(i+1)

            subset.pop()
            dfs(i+1)
        
        dfs(0)
        return res
# --8<-- [end:recursive]
