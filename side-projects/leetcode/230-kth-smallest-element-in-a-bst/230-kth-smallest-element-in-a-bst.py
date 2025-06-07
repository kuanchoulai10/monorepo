# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        # Approach 1: iterative
        # counter = 0
        # stack = []
        # curr = root
        # while curr or stack:
        #     while curr:
        #         stack.append(curr)
        #         curr = curr.left
        #     curr = stack.pop()
        #     counter += 1
        #     if counter == k:
        #         return curr.val
        #     curr = curr.right

        # Approach 2: recursive
        counter = 0
        ans = float("inf")
        def dfs(node: TreeNode, k: int) -> None:
            nonlocal counter, ans
            if node is None:
                return
            dfs(node.left, k)
            counter += 1
            if counter==k:
                ans = node.val
                return
            dfs(node.right, k)
        dfs(root, k)
        return ans
