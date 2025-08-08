# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# --8<-- [start:iterative]
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
         
        prev = None
        curr = head

        while curr != None:
            nxt = curr.next

            curr.next = prev

            prev = curr
            curr = nxt

        return prev
# --8<-- [end:iterative]

# --8<-- [start:recursive]
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:

        if head == None:
            return None
        
        new_head = head
        if head.next != None:
            new_head = self.reverseList(head.next)
            head.next.next = head
        head.next = None
        return new_head
# --8<-- [end:recursive]
