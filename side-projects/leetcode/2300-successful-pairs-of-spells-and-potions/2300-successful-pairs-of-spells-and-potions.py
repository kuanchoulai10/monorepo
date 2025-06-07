class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        # sort the potions array
        potions.sort()
        ans = []
        # binary search
        for s in spells:
            lower = 0
            upper = len(potions)-1

            idx = len(potions) # default: must larger than the biggest index in potions array

            while lower <= upper:
                m = (lower + upper) // 2
                if s * potions[m] >= success:
                    upper = m - 1
                    idx = m
                else:
                    lower = m + 1

            ans.append(len(potions)-idx)
        
        return ans