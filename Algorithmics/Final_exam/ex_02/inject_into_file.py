import random

def inject_lines(source_file, lines_file, output_file):
    with open(source_file, 'r') as src:
        source_content = src.read().replace('\n', '')

    with open(lines_file, 'r') as lines:
        lines_to_inject = lines.read().splitlines()

    for line in lines_to_inject:
        insert_position = random.randint(0, len(source_content))
        print(f'Inserting line: "{line}" at position: {insert_position}')
        source_content = source_content[:insert_position] + line + source_content[insert_position:]

    with open(output_file, 'w') as out:
        out.write(source_content)  # Write the content as one continuous string

# Example usage
source_file = 'random_chars.txt'
lines_file = 'sequences_regex_2.txt'
output_file = 'injected_output_2.txt'
inject_lines(source_file, lines_file, output_file)
