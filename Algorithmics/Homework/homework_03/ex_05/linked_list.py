class LinkedList:
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self):
        self.head = None

    def search(self, target: int) -> bool:
        current = self.head
        while current:
            if current.value == target:
                return True
            current = current.next
        return False

    def add(self, num: int) -> None:
        new_node = self.Node(num)
        new_node.next = self.head
        self.head = new_node

    def erase(self, num: int) -> bool:
        current = self.head
        prev = None

        # If the head node holds the value to be erased
        if current and current.value == num:
            self.head = current.next
            return True

        # Traverse the list to find the node to erase
        while current:
            if current.value == num:
                break
            prev = current
            current = current.next

        # If the value was not found in the list
        if not current:
            return False

        # Remove the node
        prev.next = current.next
        return True
