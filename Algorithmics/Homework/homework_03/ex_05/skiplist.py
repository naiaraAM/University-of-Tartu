import random

class SkiplistNode:
    def __init__(self, value: int, level: int):
        self.value = value
        self.forward = [None] * (level + 1)  # Array of forward pointers for each level


class Skiplist:
    def __init__(self, max_level=16, x=2):
        self.max_level = max_level  # Maximum level for the skip list
        self.head = SkiplistNode(-1, self.max_level)  # Create head node with value -1 and max level
        self.level = 0  # Current level of the skip list
        self.x = x  # Randomization factor

    def random_level(self) -> int:
        level = 0
        while random.random() < 1 / self.x and level < self.max_level:
            level += 1
        return level

    def search(self, target: int) -> bool:
        current = self.head
        for i in range(self.level, -1, -1):  # Start from the highest level
            while current.forward[i] and current.forward[i].value < target:
                current = current.forward[i]
        current = current.forward[0]  # Move to level 0
        return current is not None and current.value == target

    def add(self, num: int):
        update = [None] * (self.max_level + 1)
        current = self.head

        # Start from the highest level and move down to level 0
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < num:
                current = current.forward[i]
            update[i] = current  # Store the node at each level

        # Move to level 0
        current = current.forward[0]

        # If the element doesn't exist, insert it
        if current is None or current.value != num:
            new_level = self.random_level()

            # If the new level is greater than the current level, update pointers
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.head
                self.level = new_level

            # Create the new node with random level and insert it
            new_node = SkiplistNode(num, new_level)
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def erase(self, num: int) -> bool:
        update = [None] * (self.max_level + 1)
        current = self.head

        # Start from the highest level and move down to level 0
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < num:
                current = current.forward[i]
            update[i] = current

        # Move to level 0
        current = current.forward[0]

        # If the node is found, remove it
        if current and current.value == num:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Decrease the level if necessary
            while self.level > 0 and self.head.forward[self.level] is None:
                self.level -= 1
            return True
        return False

    def calculate_pointers(self, m):
        total_pointers = 0
        for i in range(1, self.max_level + 1):
            total_pointers += m * (i - 1)
        return total_pointers
