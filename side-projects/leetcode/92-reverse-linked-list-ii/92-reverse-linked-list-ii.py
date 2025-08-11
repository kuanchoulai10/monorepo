# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        pre_head = ListNode(None, head)
        # Stage 1
        prev = pre_head
        curr = head
        for _ in range(left-1):
            prev = curr
            curr = curr.next
        pre_left = prev
        # Stage 2
        prev = None
        for _ in range(right-left+1):
            nxt = curr.next

            curr.next = prev
            
            prev = curr
            curr = nxt
        # Stage 3
        pre_left.next.next = curr
        pre_left.next = prev

        return pre_head.next
