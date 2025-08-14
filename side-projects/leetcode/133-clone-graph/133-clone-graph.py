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
        old2new = {}

        def clone(old: Node) -> Node:
            """
            dfs-cloning approach
            """
            if old in old2new:
                return old2new[old]

            new = Node(old.val)
            old2new[old] = new
            for nb in old.neighbors:
                new.neighbors.append(
                    clone(nb)
                )

            return new
        
        return clone(node) if node else None
