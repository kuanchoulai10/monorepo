# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# --8<-- [start:dfs-resursive]
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:

        result: List[str] = []
        path: List[str] = []

        def dfs(node: TreeNode, path: List[str]) -> None:
            path.append(str(node.val))

            if node.left == None and node.right == None:
                result.append("->".join(path))
            
            if node.left:
                dfs(node.left, path)
            
            if node.right:
                dfs(node.right, path)
            
            path.pop()
        
        dfs(root, path)
        return result
# --8<-- [end:dfs-resursive]

# --8<-- [start:dfs-iterative]
class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        result: List[str] = []

        stack: List[Tuple[TreeNode, str]] = []
        stack.append(
            (root, str(root.val))
        )
        while stack:
            node, path = stack.pop()
            if node.left == None and node.right == None:
                result.append(path)
            if node.left:
                stack.append(
                    (node.left, path + "->" + str(node.left.val))
                )
            if node.right:
                stack.append(
                    (node.right, path + "->" + str(node.right.val))
                )
        return result
# --8<-- [end:dfs-iterative]