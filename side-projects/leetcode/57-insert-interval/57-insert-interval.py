class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        output = []

        for i in range(len(intervals)):
            curr_start, curr_end = intervals[i]
            new_start, new_end = newInterval
            print(f"ROUND {i+1}")
            print(f"    Current interval: {intervals[i]}")
            print(f"    New interval: {newInterval}")
            
            # Case 1: new interval is all the way to the left
            if new_end < curr_start:
                output.append(newInterval)
                output += intervals[i:]
                return output
            # Case 2: new interval is all the way to the right
            elif new_start > curr_end:
                output.append(intervals[i])
            # Case 3: overlapping
            else:
                newInterval = [
                    min(newInterval[0], intervals[i][0]),
                    max(newInterval[1], intervals[i][1])
                ]
        
        output.append(newInterval)

        return output