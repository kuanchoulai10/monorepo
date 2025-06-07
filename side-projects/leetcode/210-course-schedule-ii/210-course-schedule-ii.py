class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # Build a prerequisite list for each course
        prereq = {course: [] for course in range(numCourses)}
        for c, p in prerequisites:
            prereq[c].append(p)

        ans = []
        visited = set()
        path = set()
        cycle_detected = False
        def dfs(crs: int) -> None:
            nonlocal ans, visited, path, cycle_detected
            if crs in path:
                cycle_detected = True
                return
            if crs in visited:
                return

            path.add(crs)
            for pre in prereq[crs]:
                dfs(pre)
                if cycle_detected: # early stop
                    return
            path.remove(crs)

            visited.add(crs)
            ans.append(crs)


        for course in range(numCourses):
            if course not in visited:
                dfs(course)
                if cycle_detected:
                    return []
        return ans