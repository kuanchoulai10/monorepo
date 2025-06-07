class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        from collections import deque
        queue = deque()

        time = 0
        fresh = 0
        # - find rotten oranges and put all of it into the queue
        # - count the number of fresh oranges
        m = len(grid)
        n = len(grid[0])
        for r in range(m):
            for c in range(n):
                orange = grid[r][c]
                if orange == 1:
                    fresh += 1
                if orange == 2:
                    queue.append([r, c])

        directions = [
            [0, 1],
            [1, 0],
            [0, -1],
            [-1, 0]
        ]
        while queue and fresh > 0:
            # for each minute, do the bfs
            for i in range(len(queue)):
                r, c = queue.popleft()
                # for each rotten orange, update all the adjacent oranges (4 directions)
                for dr, dc in directions:
                    row = r + dr
                    col = c + dc
                    # if the orange is in bounds and fresh, make it rotten
                    if (0 <= row <= m-1) and (0 <= col <= n-1):
                        if grid[row][col] == 1:
                            grid[row][col] = 2
                            fresh -= 1
                            queue.append([row, col])
            time += 1

        return time if fresh==0 else -1