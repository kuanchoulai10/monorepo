# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        preHead = ListNode(None, head)

        prev = preHead
        curr = head

        while curr and curr.next:
            nxt = curr.next
            aftNxt = curr.next.next

            prev.next = nxt
            curr.next = aftNxt
            nxt.next = curr

            prev = curr
            curr = aftNxt

        return preHead.next