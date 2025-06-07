class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        from collections import deque
        m, n = len(grid), len(grid[0])
        ans = 0
        visited = set()
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for r in range(m):
            for c in range(n):
                if (r, c) not in visited and grid[r][c] == "1":
                    ans += 1
                    # bfs
                    visited.add((r, c))
                    q = deque([(r, c)])
                    while q:
                        sr, sc = q.popleft()
                        for dr, dc in directions:
                            row = sr + dr
                            col = sc + dc
                            if 0 <= row < m and 0 <= col < n:
                                if (row, col) not in visited and grid[row][col] == "1":
                                    q.append((row, col))
                                    visited.add((row, col))
        return ans