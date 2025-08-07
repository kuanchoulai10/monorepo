# --8<-- [start:sol1]
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0
        chars = set()
        left = 0
        for right in range(len(s)):
            while s[right] in chars:
                chars.remove(s[left])
                left += 1
            chars.add(s[right])
            max_length = max(
                max_length,
                len(s[left:right+1])
            )
        return max_length
# --8<-- [end:sol1]

# --8<-- [start:sol2]
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length = 0
        char_set = set()
        len_substr = 0
        for i in range(len(s)):
            while s[i] in char_set:
                char_set.remove(s[i-len_substr])
                len_substr -= 1
            char_set.add(s[i])
            len_substr += 1
            max_length = max(
                max_length,
                len_substr
            )
        return max_length
# --8<-- [end:sol2]
