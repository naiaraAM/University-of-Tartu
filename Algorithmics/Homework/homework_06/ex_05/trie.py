class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node.children:
                current_node.children[letter] = TrieNode()
            current_node = current_node.children[letter]
        current_node.is_end_of_word = True


def parenthesize_trie(node, prefix=""):
    print(f"(", end="")

    if node.is_end_of_word:
        print(prefix, end="")

    for letter, child in node.children.items():
        parenthesize_trie(child, prefix + letter)

    print(f")", end="")

def calculate_subtree_size(node):
    size = 1
    for child in node.children.values():
        size += calculate_subtree_size(child)
    return size

def find_node_by_prefix(node, prefix):
    current_node = node
    for letter in prefix:
        if letter not in current_node.children:
            return None
        current_node = current_node.children[letter]
    return current_node

words_small = ["abab", "abacus", "taco", "tactic", "aba"]
words_large = ["action", "activate", "actor", "active", "activity", "actual", "actress", "actionable", "activist", "actuate",
               "act", "acting", "activator", "actuation", "actively", "actin", "actinium", "actinoid", "actinosphere", "actomyosin"]

trie = Trie()
for word in words_large:
    trie.insert(word)

print("Parenthesis-based representation for small dataset:")
parenthesize_trie(trie.root)
print()

node_ab = find_node_by_prefix(trie.root, "ab")
if node_ab:
    size_of_ab = calculate_subtree_size(node_ab)
    print(f"Size of the subtree rooted at 'ab': {size_of_ab}")
else:
    print("Node 'ab' not found.")

