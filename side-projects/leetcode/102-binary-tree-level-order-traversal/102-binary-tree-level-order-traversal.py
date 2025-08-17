# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []

        if root == None:
            return result

        queue = deque()
        queue.append(root)
        while queue:
            nodes = []
            for _ in range(len(queue)):
                n = queue.popleft()
                if n.left:
                    queue.append(n.left)
                if n.right:
                    queue.append(n.right)
                nodes.append(n.val)
            result.append(nodes)
        
        return result