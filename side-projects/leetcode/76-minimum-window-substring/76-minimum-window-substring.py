from collections import defaultdict
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        result = ""
        result_len = float("inf")

        if t == "":
            return result

        need_map = defaultdict(int)
        need_len = len(t)
        for char in t:
            need_map[char] += 1
        
        have_map = defaultdict(int)
        have_len= 0


        l = 0
        for r in range(len(s)):
            r_char = s[r]
            have_map[r_char] += 1
            if r_char in need_map and have_map[r_char] <= need_map[r_char]:
                have_len += 1

            while have_len == need_len:
                candidate = s[l: r+1]
                if len(candidate) < result_len:
                    result = candidate
                    result_len = len(candidate)

                l_char = s[l]
                have_map[l_char] -= 1
                if l_char in need_map and have_map[l_char] < need_map[l_char]:
                    have_len -= 1
                l += 1
        return result