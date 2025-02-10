import numpy as np
import matplotlib.pyplot as plt

def edit_distance_with_transposition(s1, s2):
    m, n = len(s1), len(s2)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,  # Deletion
                           dp[i][j - 1] + 1,  # Insertion
                           dp[i - 1][j - 1] + cost)  # Substitution
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)  # Transposition

    return dp[m][n]

# Function to find the most common character changes
def find_common_changes(medicines, spellings):
    changes = {}
    transpositions = {}

    for correct, misspelled in zip(medicines, spellings):
        m, n = len(correct), len(misspelled)
        dp = np.zeros((m + 1, n + 1), dtype=int)

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if correct[i - 1] == misspelled[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1,  # Deletion
                               dp[i][j - 1] + 1,  # Insertion
                               dp[i - 1][j - 1] + cost)  # Substitution
                if i > 1 and j > 1 and correct[i - 1] == misspelled[j - 2] and correct[i - 2] == misspelled[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)  # Transposition

        i, j = m, n
        while i > 0 or j > 0:
            if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                i -= 1
            elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
                j -= 1
            elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (0 if correct[i - 1] == misspelled[j - 1] else 1):
                if correct[i - 1] != misspelled[j - 1]:
                    change = (correct[i - 1], misspelled[j - 1])
                    changes[change] = changes.get(change, 0) + 1
                i -= 1
                j -= 1
            elif i > 1 and j > 1 and dp[i][j] == dp[i - 2][j - 2] + 1:
                transposition = (correct[i - 2:i], misspelled[j - 2:j])
                transpositions[transposition] = transpositions.get(transposition, 0) + 1
                i -= 2
                j -= 2

    return changes, transpositions

# Read medicines and spellings from files
def read_list_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]

medicines = read_list_from_file("../ex_03/medicine_list.txt")
spellings = read_list_from_file("../ex_03/spellings_list.txt")

# Find the most common changes and transpositions
changes, transpositions = find_common_changes(medicines, spellings)

# Sort from most common to least common
changes = dict(sorted(changes.items(), key=lambda x: x[1], reverse=True))
transpositions = dict(sorted(transpositions.items(), key=lambda x: x[1], reverse=True))
print(f"Number of character changes: {len(changes)}")
print(f"Number of transpositions: {len(transpositions)}")

top_changes = dict(list(changes.items())[:10])
# Get the top 10 most common transpositions
top_transpositions = dict(list(transpositions.items())[:10])

# Plotting the top 10 most common character changes
plt.figure(figsize=(12, 7))
plt.bar([f"{change[0]} -> {change[1]}" for change in top_changes.keys()], top_changes.values(), color='blue')
plt.xlabel('Character Changes')
plt.ylabel('Frequency')
plt.title('Top 10 Most Common Character Changes')
plt.xticks(rotation=90)
plt.savefig('top_10_character_changes.png')
plt.show()
plt.close()

# Plotting the top 10 most common transpositions
plt.figure(figsize=(12, 6))
plt.bar([f"{transposition[0]} -> {transposition[1]}" for transposition in top_transpositions.keys()], top_transpositions.values(), color='green')
plt.xlabel('Transpositions')
plt.ylabel('Frequency')
plt.title('Top 10 Most Common Transpositions')
plt.xticks(rotation=90)
plt.savefig('top_10_transpositions.png')
plt.show()
plt.close()