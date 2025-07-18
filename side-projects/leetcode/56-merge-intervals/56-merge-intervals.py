class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key = lambda i: i[0])

        output = [intervals[0]]
        for i in range(1, len(intervals)):
            prev_start, prev_end = output[-1]
            curr_start, curr_end = intervals[i]

            if curr_start <= prev_end: # overlapping
                # merge
                output[-1][1] = max(prev_end, curr_end)
            else:
                output.append([curr_start, curr_end])

        return output