# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        ans = root.val

        def dfs(node: TreeNode) -> int:
            nonlocal ans
            if node is None:
                return 0
            
            left_max = dfs(node.left)
            right_max = dfs(node.right)
            left_max = max(left_max, 0)
            right_max = max(right_max, 0)

            # with 2 children
            ans = max(
                ans,
                node.val + left_max + right_max
            )

            # with only 1 child
            return node.val + max(left_max, right_max)

        dfs(root)
        return ans