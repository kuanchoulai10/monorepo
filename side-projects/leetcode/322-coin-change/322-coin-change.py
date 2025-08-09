class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount+1] * (amount+1)
        dp[0] = 0
        for a in range(1, amount+1):
            for c in coins:
                if a >= c:
                    dp[a] = min(
                        dp[a],
                        dp[a-c] + 1
                    )
        
        if dp[amount] == amount+1:
            return -1
        else:
            return dp[amount]