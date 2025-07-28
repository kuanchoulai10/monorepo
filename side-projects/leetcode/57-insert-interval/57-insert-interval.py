class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        output = []

        for i, interval in enumerate(intervals):
            curr_start, curr_end = interval
            new_start, new_end = newInterval
            # Case 1: new interval is all the way to the left
            if new_end < curr_start:
                output.append(newInterval)
                output += intervals[i:]
                return output
            # Case 2: new interval is all the way to the right
            elif curr_end < new_start:
                output.append(interval)
            # Case 3: overlapping
            else:
                newInterval = [
                    min(new_start, curr_start),
                    max(new_end, curr_end)
                ]

        output.append(newInterval)

        return output