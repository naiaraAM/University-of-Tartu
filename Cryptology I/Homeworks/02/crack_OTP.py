def load_word_list():
    with open('wordlist.txt', 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def xor_strings(s, t):
    return bytes([a ^ b for a, b in zip(s, t)])

def main():
    word_list = load_word_list()

    c1 = bytes.fromhex('4A5C45492449552A')
    c2 = bytes.fromhex('5A47534D35525F20')

    c1_xor_c2 = xor_strings(c1, c2)

    # Filter out words with non-ASCII characters and ensure they're length 8
    potential_words = [word for word in word_list
                      if len(word) == 8 and all(ord(c) < 128 for c in word)]

    results = []

    for m1 in potential_words:
        m1_bytes = m1.encode('ascii')  # This should now be safe
        potential_m2_bytes = xor_strings(m1_bytes, c1_xor_c2)

        if all(32 <= b <= 126 for b in potential_m2_bytes):
            try:
                potential_m2 = potential_m2_bytes.decode('ascii')

                if potential_m2 in potential_words:
                    results.append((m1, potential_m2))

                    key = xor_strings(m1_bytes, c1)
                    print(f"Found potential match: {m1} -> {potential_m2}")
                    print(f"Key (hex): {key.hex().upper()}")
            except UnicodeDecodeError:
                continue

    print(f"Total matches found: {len(results)}")

if __name__ == '__main__':
    main()