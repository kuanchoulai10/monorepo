from collections import deque
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        originalColor = image[sr][sc]
        if originalColor == color:
            return image

        m, n = len(image), len(image[0])

        delta = ((0, 1), (1, 0), (-1, 0), (0, -1))

        queue = deque([(sr, sc)])
        seen: Set[Tuple[int, int]] = set()
        seen.add((sr, sc))
        while queue:
            r, c = queue.popleft()
            image[r][c] = color
            for dr, dc in delta:
                row = r + dr
                col = c + dc
                if (0 <= row <= m-1) and (0 <= col <= n-1):
                    if image[row][col] == originalColor:
                        if (row, col) not in seen:
                            queue.append((row, col))
                            seen.add((row, col))
        return image