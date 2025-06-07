# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        ans = []
        def dfs(node: Optional[TreeNode], path: List[str]) -> None:
            if node is None:
                return

            if node.left is None and node.right is None:
                path.append(str(node.val))
                ans.append("->".join(path))
                path.pop()
                return

            path.append(str(node.val))
            dfs(node.left, path)
            dfs(node.right, path)
            path.pop()

        dfs(root, [])
        return ans
