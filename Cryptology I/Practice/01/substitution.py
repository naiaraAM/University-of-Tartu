from collections import Counter

cypher_text = "IJETVPJMFRMJOIUPEFPUUFELTVBPUFYBUMFDEUTIULFPUBFEUWVNEJGORUETFTJETJMETIUMJOIUPEKUKJRRRVVYFTJNTIJEMVDPEUKJRRNVTBUBPUFYFBRUBLIFNWVPFTFRR"

most_frequent = "ETAONRISHDLFCMUGYPWBVKJXZQ"

letter_pairs = "TH HE AN RE ER IN ON AT ND ST ES EN OF TE ED OR TI HI AS TO"

doubles_pairs = "LL EE SS OO TT FF RR NN PP CC"

def count_frequency(text):
    freq = {}
    for c in text:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq

def count_bigrams(text):
    bigrams = zip(text, text[1:])
    freq = {}
    for b in bigrams:
        if b in freq:
            freq[b] += 1
        else:
            freq[b] = 1
    return freq

def count_trigrams(text):
    trigrams = {}
    for i in range(len(text)-2):
        trigram = text[i:i+3]
        trigrams[trigram] = trigrams.get(trigram, 0) + 1
    return trigrams

def decode(frec_dict, most_frequent, original_text):
    mapped_letters = {}
    for i, letter in enumerate(frec_dict):
        # mapped_letters[most_frequent[i]
        mapped_letters[letter[0]] = most_frequent[i]

    return mapped_letters, "".join([mapped_letters[c] for c in original_text])


def main():
    freq_single = count_frequency(cypher_text)
    freq_bigrams = count_bigrams(cypher_text)
    freq_trigrams = count_trigrams(cypher_text)
    sorted_freq_single = sorted(freq_single.items(), key=lambda x: x[1], reverse=True)
    sorted_freq_bigrams = sorted(freq_bigrams.items(), key=lambda x: x[1], reverse=True)
    sorted_freq_trigrams = sorted(freq_trigrams.items(), key=lambda x: x[1], reverse=True)
    print(sorted_freq_single)
    print(sorted_freq_bigrams)
    print(sorted_freq_trigrams)
    mapped_letters, text = decode(sorted_freq_single, most_frequent, cypher_text)
    print(mapped_letters)

    # substitue U for lower case e in text
    text = cypher_text.replace("U", "e")
    text = text.replace("I", "h")
    text = text.replace("R", "l")
    text = text.replace("V", "o")
    text = text.replace("Y", "k")
    text = text.replace("J", "i")
    text = text.replace("T", "t")
    text = text.replace("E", "s")
    text = text.replace("F", "a")
    text = text.replace("P", "r")
    text = text.replace("M", "c")
    text = text.replace("O", "p")
    text = text.replace("L", "y")
    text = text.replace("B", "b")
    text = text.replace("D", "u")
    text = text.replace("W", "d")
    text = text.replace("G", "m")
    text = text.replace("N", "n")
    text = text.replace("K", "w")
    print(text)


main()