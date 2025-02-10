def collatz(n):
    if n == 1:
        return [1]
    if n % 2 == 0:
        return [n] + collatz(n // 2)
    return [n] + collatz(3 * n + 1)


class Tree:
    def __init__(self, val=None):
        self.value = val
        if self.value:
            self.left = Tree()
            self.right = Tree()
        else:
            self.left = None
            self.right = None

    def isempty(self):
        return self.value is None

    def insert(self, data):
        if self.isempty():
            self.value = data
            self.left = Tree()
            self.right = Tree()
        elif data < self.value:
            self.left.insert(data)
        elif data > self.value:
            self.right.insert(data)


# Generate bit-vector for the tree
def create_bit_vector(tree):
    bit_vector = []

    def traverse(node):
        if node.isempty():
            bit_vector.append(0)
        else:
            bit_vector.append(1)
            traverse(node.left)
            traverse(node.right)

    traverse(tree)
    return bit_vector


def traverse_using_bit_vector(bit_vector, values):
    result = []

    for i in range(len(bit_vector)):
        if bit_vector[i] == 1:
            result.append(values.pop(0))
        else:
            result.append("L")

    return result

collatz_sequence = collatz(17)

tree = Tree()
for value in collatz_sequence:
    tree.insert(value)

bit_vector = create_bit_vector(tree)
print("\nBit-vector:", bit_vector)

traversal_result = traverse_using_bit_vector(bit_vector, collatz_sequence)
print("\nBreadth-first traversal using bit-vector:", traversal_result)
