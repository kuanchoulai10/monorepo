class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m, n = len(board), len(board[0])
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        def dfs(r: int, c: int):
            nonlocal m, n, board, directions
            if 0 <= r < m and 0 <= c < n and board[r][c] == "O":
                board[r][c] = "#"
                for dr, dc in directions:
                    dfs(r+dr, c+dc)
        
        for r in range(m):
            for c in range(n):
                if not (1 <= r <= m-2 and 1 <= c <= n-2):
                    if board[r][c] == 'O':
                        dfs(r, c)
        
        for r in range(m):
            for c in range(n):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "#":
                    board[r][c] = "O"
        
        return board
