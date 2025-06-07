class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        from collections import deque
        originalColor = image[sr][sc]
        if originalColor == color:
            return image
        m = len(image)
        n = len(image[0])
        q = deque([[sr, sc]])
        directions = [[0, 1], [1, 0], [-1,0], [0,-1]]
        while q:
            r, c = q.popleft()
            image[r][c] = color
            for dr, dc in directions:
                row = r + dr
                col = c + dc
                if (0 <= row <= m-1) and (0 <= col <= n-1):
                    if image[row][col] == originalColor:
                        q.append([row, col])
        return image
