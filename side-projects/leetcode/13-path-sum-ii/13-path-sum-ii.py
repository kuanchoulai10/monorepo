# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        ans = []
        path = []

        def dfs(node: Optional[TreeNode], targetSum: int) -> None:
            if node is None:
                return 
            
            path.append(node.val)

            nextTargetSum = targetSum-node.val
            dfs(node.left, nextTargetSum)
            dfs(node.right, nextTargetSum)

            if (node.left is None) and (node.right is None) and (nextTargetSum==0):
                ans.append(path.copy())

            path.pop()

        dfs(root, targetSum)
        return ans
