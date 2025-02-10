class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.indexes = []

    def insert_suffix(self, suffix, index):
        self.indexes.append(index)
        if suffix:
            first_char = suffix[0]
            if first_char not in self.children:
                self.children[first_char] = SuffixTreeNode()
            self.children[first_char].insert_suffix(suffix[1:], index + 1)

    def search(self, pat):
        if not pat:
            return self.indexes
        first_char = pat[0]
        if first_char in self.children:
            return self.children[first_char].search(pat[1:])
        return None
class SuffixTree:
    def __init__(self, txt):
        self.root = SuffixTreeNode()
        for i in range(len(txt)):
            self.root.insert_suffix(txt[i:], i)

    def search(self, pat):
        result = self.root.search(pat)
        if not result:
            print("Pattern not found")
        else:
            pat_len = len(pat)
            for i in result:
                print(f"Pattern found at position {i - pat_len}")

if __name__ == "__main__":
    txt = "bananabanaba"
    st = SuffixTree(txt)

    # Let us search for different patterns
    pat = "aba"
    print(f"Search for '{pat}'")
    st.search(pat)
    print()