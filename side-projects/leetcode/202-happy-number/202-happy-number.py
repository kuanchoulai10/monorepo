# --8<-- [start:set]
class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set()

        while n not in seen:
            seen.add(n)
            n = self.getNext(n)
        
        return n == 1

    def getNext(self, n: int) -> int:
        nextNumber = 0
        while n != 0:
            nextNumber += (n % 10) ** 2
            n //= 10
        return nextNumber
# --8<-- [end:set]

# --8<-- [start:fast-slow]
class Solution:
    def isHappy(self, n: int) -> bool:
        slow = n
        fast = self.getNext(n)

        while slow != fast:
            slow = self.getNext(slow)
            fast = self.getNext(self.getNext(fast))
        
        return fast == 1

    def getNext(self, n: int) -> int:
        nextNumber = 0
        while n != 0:
            nextNumber += (n % 10) ** 2
            n //= 10
        return nextNumber
# --8<-- [end:fast-slow]
