class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack: List[Tuple[int, int]] = []  # [(idx, height)]

        max_h = -float("inf")
        for curr_i, curr_h in enumerate(heights):

            updated_i = curr_i

            while stack and curr_h < stack[-1][1]:
                prev_i, prev_h = stack.pop()
                updated_i = prev_i
                w = curr_i - prev_i
                max_h = max(max_h, prev_h * w)

            stack.append((updated_i, curr_h))


        for i, h in stack:
            w = len(heights) - i
            max_h = max(
                max_h,
                h * w
            )
        
        return max_h