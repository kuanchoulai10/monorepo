class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort() # O(m log m)
        result = []
        for s in spells: # O(n log m)
            l = 0
            r = len(potions) - 1

            # idx = float("inf")
            idx = len(potions)

            while l <= r:
                m = (l + r) // 2
                if s * potions[m] >= success:
                    r = m - 1
                    idx = m
                else:
                    l = m + 1
            
            # if idx == float("inf"):
            #     result.append(0)
            # else:
            #     result.append(len(potions)-idx)
            result.append(len(potions)-idx)
        return result