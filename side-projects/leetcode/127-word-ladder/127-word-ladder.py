class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        from collections import defaultdict, deque

        if endWord not in wordList:
            return 0

        # create an adjacent dict where key is the pattern and value is list of neighbor words
        neighbors = defaultdict(list)
        wordList.append(beginWord)
        for word in wordList:
            for j in range(len(word)):
                pattern = word[:j] + "*" + word[j+1:]
                neighbors[pattern].append(word)

        q = deque([beginWord])
        visited = set([beginWord])
        ans = 1
        while q:
            # bfs: iterate through each word in the queue
            for i in range(len(q)):
                word = q.popleft()
                if word == endWord:
                    return ans
                # for each word, iterate through all the patterns and find all the neighbors for each pattern
                for j in range(len(word)):
                    pattern = word[:j] + "*" + word[j+1:]
                    for neiWord in neighbors[pattern]:
                        if neiWord not in visited:
                            visited.add(neiWord)
                            q.append(neiWord)
            ans += 1

        return 0