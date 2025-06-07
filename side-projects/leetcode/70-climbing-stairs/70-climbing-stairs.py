class Solution:
    def climbStairs(self, n: int) -> int:
        dp = []
        for i in range(n):
            if i==0:
                dp.append(1)
            elif i==1:
                dp.append(2)
            else:
                dp.append(dp[i-2] + dp[i-1])
        return dp[-1]
