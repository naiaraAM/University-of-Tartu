class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_sequence = False

class CollatzTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, sequence):
        node = self.root
        for digit in sequence:
            if digit not in node.children:
                node.children[digit] = TrieNode()
            node = node.children[digit]
        node.is_end_of_sequence = True

    def search(self, sequence):
        node = self.root
        for digit in sequence:
            if digit not in node.children:
                return False
            node = node.children[digit]
        return node.is_end_of_sequence

    def insert_collatz_sequence(self, start):
        sequence = []
        while start != 1:
            sequence.append(str(start))
            if start % 2 == 0:
                start = start // 2
            else:
                start = 3 * start + 1
        sequence.append("1")
        for num_str in sequence:
            self.insert(num_str)

# Initialize Collatz Trie
collatz_trie = CollatzTrie()

# Insert the Collatz sequence for 51
collatz_trie.insert_collatz_sequence(51)

# Check if certain numbers are in the trie
test_numbers = ['51', '25', '531', '2', '45']
search_results = {num: collatz_trie.search(num) for num in test_numbers}


print(search_results)  # Expected: {'51': True, '25': False, '531': False, '2': True, '45': False}
