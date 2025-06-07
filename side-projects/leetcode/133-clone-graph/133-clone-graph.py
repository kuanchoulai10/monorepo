"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        o2n = {}

        def clone(node: Node) -> Node:
            """
            dfs-cloning approach
            """
            if node in o2n:
                return o2n[node]

            new_n = Node(node.val)
            o2n[node] = new_n
            for nb in node.neighbors:
                new_n.neighbors.append(
                    clone(nb)
                )

            return new_n
        
        return clone(node) if node else None
