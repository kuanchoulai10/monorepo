# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# --8<-- [start: recursive]
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        ans = float("inf")
        counter = 0
        def dfs(node: TreeNode, k: int) -> None:
            nonlocal ans, counter

            if node.left:
                dfs(node.left, k)
            
            counter += 1
            if counter == k:
                ans = node.val
                return
            
            if node.right:
                dfs(node.right, k)
            
        dfs(root, k)
        return ans
# --8<-- [end: recursive]
# --8<-- [start: iterative]

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        counter = 0
        stack = []
        current_node = root

        while current_node or stack:
            while current_node:
                stack.append(current_node)
                current_node = current_node.left

            current_node = stack.pop()
            counter += 1
            if counter == k:
                return current_node.val
            current_node = current_node.right
        return 
# --8<-- [end: iterative]