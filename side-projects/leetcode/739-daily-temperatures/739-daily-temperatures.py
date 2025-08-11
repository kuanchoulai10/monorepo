class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        days = [0] * len(temperatures)
        stack: list[tuple[int, int]] = [] # list of pairs = (idx, temp)

        for curr_day, curr_temp in enumerate(temperatures):

            while len(stack) != 0 and stack[-1][1] < curr_temp:
                target_day, _ = stack.pop()
                days[target_day] = curr_day - target_day

            stack.append((curr_day, curr_temp))

        return days